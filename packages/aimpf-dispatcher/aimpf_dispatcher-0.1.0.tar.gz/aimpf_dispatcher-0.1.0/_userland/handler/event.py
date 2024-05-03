import json
import logging
import os
import re
from auth import AuthorizationAgent
from pprint import pformat


logger = logging.getLogger()
logger.setLevel(os.environ.get("DEBUG_LEVEL", "INFO"))


class EventHandler:
    def __init__(self, event:dict):
        """Handle an HTTP event."""
        self.event = event
        self.routes = dict()
        self.carta_agent = AuthorizationAgent(
            token=self.authorization_token,
            url=os.environ.get("CARTA_AUTH_URL", None))

    def __call__(self):
        for k,v in self.routes.items():
            if re.match(k, self.path):
                logger.debug(f"Found function matching {self.path!r}")
                try:
                    result = v()
                except Exception as e:
                    logging.debug(f"Failed Event: {pformat(self.event)}")
                    raise
                # logger.debug(f"Event result: {pformat(result)}")
                return result
        msg = f"Did not find a route that matches {self.path!r}"
        logger.debug(msg)
        raise ValueError(msg)

    def route(self, endpoint):
        """
        Wraps a function to use data from an HTTP event.

        Parameters
        ----------
        endpoint : str
            Description of the endpoint/route after the base URL. Route
            parameters surrounded in curly braces will be extracted from the
            route and passed as keywords into the wrapped function, e.g.
            
                eventHandler.route("/route/{param}")
            
            when called as "{BASE_URL}/route/12345" will call the function with
            param=12345.
        """
        logger.debug(f"Creating route for {endpoint!r}")
        # endpoint = endpoint.strip('/')  # strip the leading forward slash.
        routeParamRe = re.compile(r'^{.+}$')
        fromPath = {
            key.strip("{}"):index
            for index, key in enumerate(endpoint.strip("/").split("/"))
            if re.match(routeParamRe, key)
        }
        logger.debug(f"Path parameters: {pformat(fromPath)}")
        pattern = "^" + re.sub('{.+?}', '[^/]+', endpoint) + "$"
        def wrapper(fn):
            def func():
                opts = {
                    **{k:self.path_parameters[i] for k,i in fromPath.items()},
                    **self.params
                }
                if isinstance(self.body, str):
                    try:
                        # Body is a string to be converted to a JSON
                        body = json.loads(self.body)
                    except json.JSONDecodeError:
                        # Body is a string, but not valid JSON
                        body = self.body
                elif isinstance(self.body, dict):
                    # Already a dictionary
                    body = self.body
                elif self.body is None:
                    body = dict()
                else:
                    raise ValueError(f"Invalid type ({type(self.body)}) for body.")
                return fn(body, **opts)
            self.routes[pattern] = func
            logger.debug(f"Added route {pattern!r}")
            return func
        return wrapper

    @property
    def body(self):
        return self.event.get("body", dict())
    
    @property
    def context(self):
        return self.event.get("requestContext", dict())
    
    @property
    def headers(self):
        return self.event.get("headers", dict())
    
    @property
    def method(self):
        return self.context["httpMethod"]
    
    @property
    def path(self):
        return self.event["path"]
    
    @property
    def path_parameters(self):
        return self.path.strip("/").split("/")
    
    @property
    def params(self):
        return self.event.get("queryStringParameters", None) or dict()
    
    @property
    def authorization_token(self):
        token = self.headers.get("X_CARTA_TOKEN", None)
        return token.replace("Bearer ", "") if token else token
    