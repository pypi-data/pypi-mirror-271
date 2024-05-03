# TODO: This is designed around the specifics of the AIMPF IoTfM (Internet of
# TODO: Things for Manufacturing deployment. At the time of development, these
# TODO: all store to a MySQL database with a common layout.
from __future__ import annotations

import os, sys
import datetime
import json
import logging
import requests
from configparser import ConfigParser
from event import EventHandler
from functools import cache
from pprint import pformat
from sqlalchemy import create_engine, text

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("DEBUG_LEVEL", "INFO"))

def serialize_datetime(obj): 
    if isinstance(obj, datetime.datetime): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 

def lambda_response(status, body=None):
    if isinstance(body, (dict, list, str, int, float, datetime.datetime)):
        body = json.dumps(body, default=serialize_datetime)
    
    return {
        "isBase64Encoded": False,
        "statusCode": status,
        "body": body
    }

# TODO: Create a query context that allows the calling function to reuse a
# TODO: connection to the database.
def query(cfg: dict, q: str, **kwds):
    """
    Query the database.
    
    Note: Only pymysql is supported for MySQL/MariaDB

    Parameters
    ----------
    cfg : dict
        Configuration dictionary containing dialect, user,
        password, host, database, and optionally, dialect and port.
    q : str
        Query string
    kwds : dict
        Parameters passed to the query.

    Returns
    -------
    list
        List of records.
    """
    # Handle optional driver
    dialect = cfg["dialect"]
    driver = cfg.get("driver", "")
    if dialect.lower() in ("mysql", "mariadb"):
        # force the use of pymysql
        logger.info("Using pymysql driver. Other MySQL drivers are not currently supported.")
        driver = "pymysql"
    if driver:
        dialect = f"{dialect}+{driver}"
    logger.debug(f"Dialect: {dialect}")
    # Handle optional port
    host = cfg["host"]
    port = cfg.get("port", "")
    if port:
        host = f"{host}:{port}"
    logger.debug(f"Host: {host}")
    # Create the engine
    engine = create_engine(
        f"{dialect}://{cfg['user']}:{cfg['password']}@{host}/{cfg['database']}"
    )
    logger.info(f"Created engine: {dialect}://{cfg['user']}:<password>@{host}/{cfg['database']}")
    q_ = q
    logger.info(f"Query: {q_}")
    # Execute the query
    try:
        with engine.connect() as conn:
            return conn.execute(text(q_), kwds).fetchall()
    except Exception as e:
        logger.error(f"Error executing query: {q_!r}")
        raise requests.HTTPError(500, f"Error executing query: {str(e)}") from e

def handle_request(event, context):
    """
    Handle an API event, e.g. GET, POST, etc.

    Parameters
    ----------
    event : str
        String representation of the event JSON.
    context :  LambdaContext
        A LambdaContext object providing details on the instance executing this
        request.
    
    Returns
    -------
    JSON
        Response to the API request.
    """
    def now():
        return datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    logger.debug(f"Event: {pformat(event)}")
    logger.debug(f"Context: {str(context)}")

    # Object definitions
    eventHandler = EventHandler(event)
    logger.debug("Created EventHandler")

    # Read in global configuration
    # NOTE: This gives anyone with access to the service access to the
    # configured resource(s). As-is, this limits access to the configured
    # resource(s) to those with access to the service.
    # TODO: Add user-level authentication to each resource. For example,
    # TODO: Option 1. Store in the config file the hash of a secondary password
    # TODO: that the user must provide, e.g. "pwd = a591a6d40bf420404..."
    # TODO: for the secondary password "Hello World" (using an SHA256 hash).
    # TODO: Option 2. Provide in the config file a field that stores the name
    # TODO: that would be used by a "/resources/{resource}/secret" endpoint
    # TODO: that the user would use to store their authentication credentials.
    client = boto3.client("ssm")
    config = ConfigParser()
    config.read_string(
        client.get_parameter(
            Name="/CartaDispatch/GA-AIM/iotfm.ini",
            WithDecryption=True
        )["Parameter"]["Value"]
    )
    logger.debug("Read configuration")

    # Utility functions to condition SQL queries
    @cache
    def table_columns(resource: str) -> tuple:
        """
        Get the columns for a resource.

        Parameters
        ----------
        resource : str
            Resource name.

        Returns
        -------
        tuple
            Tuple of column names.
        """
        response = query(config[resource], f"SHOW COLUMNS FROM Messages;")
        columns = tuple(
            dict(zip(("Field", "Type", "Null", "Key", "Default", "Extra"), r))["Field"]
            for r in response
        )
        logger.debug(f"Columns: {columns}")
        return columns
    
    @cache
    def column_values(resource: str, column: str) -> tuple:
        """
        Get the unique values for a column.

        Parameters
        ----------
        resource : str
            Resource name.
        column : str
            Column name.

        Returns
        -------
        tuple
            Tuple of values.
        """
        columns = table_columns(resource)
        for col in columns:
            if col.lower() == column.lower():
                break
        else:
            raise ValueError(f"No such column: {column}") # Successful process, but no such column exists.
        response = query(config[resource], f"SELECT DISTINCT {column} FROM Messages;")
        values = tuple(r[0] for r in response if len(r))
        logger.debug(f"Values for {column}: {values[:7]}{'...' if len(values) > 7 else ''}")
        return values
    
    def sanitize_condition(resource: str, condition: str) -> str:
        """
        Sanitize a condition string.

        Parameters
        ----------
        resource : str
            Resource name.
        condition : str
            Condition string.

        Returns
        -------
        str
            Sanitized condition string.
        """
        condition = condition.strip()
        logger.debug(f"Condition: {condition}")
        # get available columns
        columns = table_columns(resource)
        logger.debug(f"Available columns: {columns}")
        # check that the column is valid
        col = None
        for c in columns:
            if condition.startswith(c):
                col = c
                break
        else:
            raise ValueError(f"No valid column found.") # Successful process, but no columns match.
        condition = condition[len(col):].strip()
        # check that the operator is supported
        op = None
        for o in ("<=", ">=", "=", "<", ">"):
            if condition.startswith(o):
                op = o
                break
        else:
            raise ValueError("Invalid operator.") # Successful process, but no such operator exists.
        condition = condition[len(op):].strip()
        # check that the value is valid
        value = None
        for v in column_values(resource, col):
            if condition.strip('"').strip("'").startswith(str(v)):
                value = f"'{v}'" if isinstance(v, str) else v
                break
        else:
            raise ValueError(f"Value not found in {col}") # Successful process, but no such value exists.
        # Done: generate conditioned response
        logger.debug(f"Sanitized condition: {col} {op} {value}")
        return f"{col} {op} {value}"

    def configure_query_conditions(q, resource, kwds):
        """
        Build the SQL query string based on the provided parameters.

        Parameters
        ----------
        q : str
            SQL query string without conditions.
        resource : str
            Resource name.
        kwds : dict
            Dictionary of keyword arguments.

        Returns
        -------
        q : str
            SQL query string with conditions.
        kwds : dict
            Dictionary of keyword arguments.
        """
        # WHERE: query conditions
        where = []
        
        # Check if a time range has been specified
        if "from" in kwds and "to" in kwds:
            kwds["from"] = datetime.datetime.fromisoformat(kwds["from"])
            kwds["to"] = datetime.datetime.fromisoformat(kwds["to"])
            where.append("dateTime BETWEEN :from AND :to")
        elif "from" in kwds:
            kwds["from"] = datetime.datetime.fromisoformat(kwds["from"])
            where.append("dateTime >= :from")
        elif "to" in kwds:
            kwds["to"] = datetime.datetime.fromisoformat(kwds["to"])
            where.append("dateTime <= :to")
        
        # Additional conditions
        conditions = [_.strip() for _ in kwds.get("where", "").split(",") if _.strip()]
        for condition in conditions:
            # These may be slow as the contents of the database are used to
            # sanitize the query condition.
            try:
                where.append(sanitize_condition(resource, condition))
            except ValueError as e:
                logger.error(f"No matching condition matching {condition} found in {resource}: {str(e)}")
                raise
        
        # Finalize WHERE clause
        where_clause = (" WHERE " + " AND ".join(where)) if where else ""
        
        # LIMIT: limit command
        limit_clause = ""
        if "limit" in kwds:
            limit_clause = f" LIMIT {kwds['limit']}"

        # Compose query
        q = f"{q}{where_clause}{limit_clause}"

        # Need to return the kwds to keep the changes on data types
        return q

    # Set up event handlers
    # This endpoint is used to test how the keywords are parsed from the
    # URL.
    @eventHandler.route("/keywords")
    def check_keywords(body, **kwds):
        """
        Check how the keywords are parsed from the endpoint.
        """
        logger.info("Calling '/keywords'")
        return lambda_response(200, kwds)

    @eventHandler.route("/check")
    def check_health(body, **kwds):
        """
        Health check endpoint.
        
        Returns
        -------
        JSON
            Verifies that the server is running and accepting API requests.
        
        Raises
        ------
        requests.HTTPError
            If the request fails.
        
        Notes
        -----
        This endpoint is used by the AWS Lambda health check.
        """
        logger.info("Calling '/check'")
        return lambda_response(200, {
            "health": "alive",
            "time": now()
        })
    
    @eventHandler.route("/resources/list")
    def list_resources(body, **kwds):
        """
        List resources.

        Returns
        -------
        JSON
            List of resources.

        Raises
        ------
        requests.HTTPError
            If the request fails.
        """
        logger.info("Calling '/resources/list'")
        return lambda_response(200, {
            "resources": [_ for _ in config.keys() if _ != "DEFAULT"]
        })
    
    @eventHandler.route("/resources/{resource}/columns")
    def list_columns(*args, resource, **kwds):
        """
        List columns for a resource.

        Returns
        -------
        JSON
            List of columns keyed by table name.

        Raises
        ------
        requests.HTTPError
            If the request fails.
        """
        logger.info(f"Calling '/resources/{resource}/columns'")
        results = dict()
        for table in config[resource]["tables"].split(","):
            response = query(config[resource], f"SHOW COLUMNS FROM {table}")
            results[table] = [
                dict(zip(("Field", "Type", "Null", "Key", "Default", "Extra"), r))
                for r in response
            ]
        return lambda_response(200, results)
    
    # TODO: Add parameter that allows the user to specify additional columns
    # TODO: to be included in the query results, e.g.
    # TODO: "SELECT dataItemId,value,dateTime FROM Messages WHERE assetId = 'Okuma-4020'"
    # TODO: would be "/resources/ctxt/list/dataItemId?where=assetId=Okuma-4020&include=value,dateTime"

    # SELECT DISTINCT assetId FROM Messages;
    # SELECT DISTINCT dataItemId FROM Messages;
    # SELECT DISTINCT topic FROM Messages;
    # SELECT DISTINCT dataItemId FROM Messages WHERE assetId = "Optomec";
    # SELECT DISTINCT dataItemId FROM Messages WHERE assetId = "Okuma-4020";
    # SELECT DISTINCT value FROM Messages WHERE assetId = "Okuma-4020" AND dataItemId = "Heartbeat" LIMIT 10;
    # SELECT DISTINCT dataItemId,value FROM Messages WHERE assetId = "Okuma-4020";
    @eventHandler.route("/resources/{resource}/distinct/{column}")
    def distinct(*args, resource, column, **kwds):
        """
        List unique elements from a column for a resource.

        Parameters
        ----------
        limit : int, optional
            Limit the number of results.
        from : dateTime, optional
            Define the lower bound time for matching results.
        to: dateTime, optional
            Define the upper bound time for matching results.
        where: str
            Comma-separated list of conditions. Each must match
            <col><op><value> where <col> is a column name in the table, <op>
            is a comparison operator ("=", "<", ">", "<=", ">="), and <value>
            is present in the database. WARNING: This can be quite slow as
            query sanitation can take a very long time.

        Returns
        -------
        JSON
            List of unique assets.

        Raises
        ------
        requests.HTTPError
            If the request fails.
        """
        logger.info(f"Calling '/resources/{resource}/distinct/{column}'")
        # Validate column
        for c in column.split(","):
            col = c.strip()
            if col not in table_columns(resource):
                return lambda_response(400, {"message": f"No such column: {col}"})
        # Construct query
        q = f"SELECT DISTINCT {column} FROM Messages"
        try:
            q = configure_query_conditions(q, resource, kwds)
        except ValueError as e:
            logger.debug(f"Distinct failed with message {str(e)!r}.")
            return lambda_response(400, {"message": str(e)})
        logger.info(f"Query: {q}")
        results = query(config[resource], q, **kwds)
        results = [list(r) for r in results]
        # logger.info(f"Response: {results}")
        
        return lambda_response(200, results)

    # SELECT COUNT(*) FROM Messages;
    # SELECT COUNT(*) FROM Messages WHERE assetId = "Okuma-4020";
    @eventHandler.route("/resources/{resource}/count")
    def count(*args, resource, **kwds):
        """
        Count the number of rows in a resource.

        Parameters
        ----------
        limit : int, optional
            Limit the number of results.
        from : dateTime, optional
            Define the lower bound time for matching results.
        to: dateTime, optional
            Define the upper bound time for matching results.
        where: str
            Comma-separated list of conditions. Each must match
            <col><op><value> where <col> is a column name in the table, <op>
            is a comparison operator ("=", "<", ">", "<=", ">="), and <value>
            is present in the database. WARNING: This can be quite slow as
            query sanitation can take a very long time.

        Returns
        -------
        JSON
            List of unique assets.

        Raises
        ------
        requests.HTTPError
            If the request fails.
        """
        logger.info(f"Calling '/resources/{resource}/count'")
        q = "SELECT COUNT(*) FROM Messages"
        try:
            q = configure_query_conditions(q, resource, kwds)
        except ValueError as e:
            logger.debug(f"Count failed with message {str(e)!r}.")
            return lambda_response(400, {"message": str(e)})
        logger.info(f"Query: {q}")
        results = query(config[resource], q, **kwds)
        results = [list(r) for r in results]
        # logger.info(f"Response: {results}")
        
        return lambda_response(200, results)

    # SELECT * FROM Messages WHERE assetId = "Okuma-4020" LIMIT 10;
    # SELECT * FROM Messages WHERE dataItemId = "execution " LIMIT 10;
    # SELECT * FROM Messages WHERE dataItemId = "Mp1MacManPanelHistory" AND dateTime BETWEEN "2023-04-04 16:59:00" AND "2023-04-04 17:00:00" LIMIT 10;
    # SELECT * FROM Messages WHERE Id >= 5415302 AND dataItemId = "Mp1MacManPanelHistory" LIMIT 10;
    @eventHandler.route("/resources/{resource}/list")
    def list_records(*args, resource, **kwds):
        """
        List records for a resource.

        Parameters
        ----------
        limit : int, optional
            Limit the number of results.
        from : dateTime, optional
            Define the lower bound time for matching results.
        to: dateTime, optional
            Define the upper bound time for matching results.
        where: str
            Comma-separated list of conditions. Each must match
            <col><op><value> where <col> is a column name in the table, <op>
            is a comparison operator ("=", "<", ">", "<=", ">="), and <value>
            is present in the database. WARNING: This can be quite slow as
            query sanitation can take a very long time.

        Returns
        -------
        JSON
            List of unique assets.

        Raises
        ------
        requests.HTTPError
            If the request fails.
        """
        logger.info(f"Calling '/resources/{resource}/list'")
        q = "SELECT * FROM Messages"
        try:
            q = configure_query_conditions(q, resource, kwds)
        except ValueError as e:
            logger.debug(f"List failed with message {str(e)!r}.")
            return lambda_response(400, {"message": str(e)})
        logger.info(f"Query: {q}")
        results = query(config[resource], q, **kwds)
        results = [list(r) for r in results]
        # logger.info(f"Response: {results}")
        
        return lambda_response(200, results)

    # TODO: Add a route for the following queries:
    # SELECT * FROM Messages WHERE dataItemId = "Mp1MacManPanelHistory" AND (value LIKE "%2023/04/04 16:59%") LIMIT 10;

    # Execute the event
    return eventHandler()


if __name__ == "__main__":
    print("Run 'tests/test_handler.py' to test.")
