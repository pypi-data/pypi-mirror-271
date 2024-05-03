import os
import sys
import logging
import pytest
import requests

from getpass import getpass
from pprint import pprint
from urllib import parse

sys.path.append(os.path.abspath("../_userland/handler"))
from _userland.handler.auth import AuthorizationAgent

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set up test fixtures
@pytest.fixture
def headers():
    """
    Returns the headers required for authentication.

    It can be convenient during development to enter a default username and
    password. When done, change default username and password to None.

    Returns:
        dict: The authentication headers.
    """
    username = "user1.root" or input("Enter your Carta username: ")
    try:
        password = os.environ["USER1_ROOT_PASSWORD"]
    except IndexError:
        raise Exception("Please set the USER1_ROOT_PASSWORD environment variable.")
    # password = None or getpass(f"Enter the Carta password for {username}: ")

    auth_url = "https://api.sandbox.carta.contextualize.us.com"
    auth = AuthorizationAgent(username, password, url=auth_url)
    token = auth.token

    # When run as a Carta Service, X_CARTA_AUTH will replace Authorization
    auth_headers = {
        "Authorization": f"Bearer {token}",
        "X_CARTA_TOKEN": f"Bearer {token}"
    }

    return auth_headers

@pytest.fixture
def url():
    """
    Returns a lambda function that constructs a URL based on the given endpoint.

    Args:
        endpoint (str): The endpoint to append to the base URL.

    Returns:
        str: The constructed URL.
    """
    host = "t58bbyh0wg.execute-api.us-east-2.amazonaws.com/prod/"
    return lambda endpoint: "/".join(["https://" + host.strip("/"), endpoint.strip("/")])

# Test functions
# --------------

# NOTE: All the test functions constructed below share the same fixtures, and the ``Args`` and ``Returns`` sections are exactly the same. For brevity, only the first test function has the full documentation, and the rest of them only has the description.

# Database information
# ^^^^^^^^^^^^^^^^^^^^

def test_keywords(url, headers):
    """
    Test case for checking the keywords parsed from the endpoint.
    """
    # endpoint = "keywords?where=Id>=5415302"  # {'where': 'Id>=5415302'}
    endpoint = "keywords?where=Id>=5415302&where=dataItemId=Mp1MacManPanelHistory&limit=10"  # {'limit': '10', 'where': 'dataItemId=Mp1MacManPanelHistory'}
    # endpoint = "keywords?where[]=Id>=5415302&where[]=dataItemId=Mp1MacManPanelHistory" # {'where': 'dataItemId=Mp1MacManPanelHistory'}
    response = requests.get(url(endpoint), headers=headers, timeout=10)
    pprint(response.json())
    assert response.status_code == 200

def test_check_service_is_live(url, headers):
    """
    Test case for checking if the service is live.

    Args:
        url (function): The function that constructs the URL.
        headers (dict): The authentication headers.

    Returns:
        None
    """
    endpoint = "check"
    response = requests.get(url(endpoint), headers=headers, timeout=10)
    pprint(response.json())
    assert response.status_code == 200
    assert response.json()["health"] == "alive"

def test_list_resources(url, headers):
    """
    Test case for listing the available databases.
    """
    endpoint = "resources/list"
    response = requests.get(url(endpoint), headers=headers, timeout=10)
    pprint(response.json())
    assert response.status_code == 200
    assert "ctxt" in response.json()["resources"]

def test_list_columns(url, headers):
    """
    Test case for listing the columns of the database.
    """
    endpoint = "resources/ctxt/columns"
    response = requests.get(url(endpoint), headers=headers, timeout=10)
    pprint(response.json())
    assert response.status_code == 200
    assert len(response.json()["Messages"]) > 1

# List distinct values of a column
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

def test_listdistinct_column(url, headers):
    """
    Test case for listing the distinct values of a column.

    Note: 
        This test fails some times probably due to the timeout on the server side, because we've already set the timeout to as long as 200 seconds.
    """
    endpoint = "resources/ctxt/distinct/assetId"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok, f"{response.status_code}: {response.text!r}"
    pprint(response.json())
    assert len(response.json()) > 0

def test_listdistinct_column_with_limit(url, headers):
    """
    Test case for listing the distinct values of a column, with limit.
    """
    endpoint = "resources/ctxt/distinct/assetId?limit=3"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok, response.text
    pprint(response.json())
    assert len(response.json()) <= 3

def test_listdistinct_column_with_range(url, headers):
    """
    Test case for listing the distinct values of a column, within a from-to range.
    """
    endpoint = "resources/ctxt/distinct/assetId?from=2020-01-01&to=2024-04-14"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok, response.text
    pprint(response.json())
    assert len(response.json()) > 0

def test_listdistinct_column_with_range_limit(url, headers):
    """
    Test case for listing the distinct values of a column, within a from-to range.
    """
    endpoint = "resources/ctxt/distinct/assetId?from=2020-01-01&to=2022-12-31&limit=5"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok, response.text
    pprint(response.json())
    assert len(response.json()) > 0

def test_listdistinct_columns_with_assetid(url, headers):
    """
    Test case for listing the distinct values of column(s), for a specific assetId, with limit.
    """
    endpoint = "resources/ctxt/distinct/dataItemId,dateTime?where=assetId=Okuma-4020&limit=10"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok, response.text
    pprint(response.json())
    assert len(response.json()) <= 10

# Count records
# ^^^^^^^^^^^^^

def test_count(url, headers):
    """
    Test case for counting the records in the database.
    """
    endpoint = "resources/ctxt/count"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok
    pprint(response.json())
    assert response.json()[0][0] == 2731  # Size of test db

def test_count_with_assetid(url, headers):
    """
    Test case for counting the records in the database for a specific assetId.
    """
    endpoint = "resources/ctxt/count?where=assetId=Okuma-4020"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok
    pprint(response.json())
    assert response.json()[0][0] == 200  # Grabbed 200 records from each column

def test_count_with_assetid_range(url, headers):
    """
    Test case for counting the records in the database for a specific assetId within a from-to range.
    """
    endpoint = "resources/ctxt/count?where=assetId=Okuma-4020&from=2020-01-01&to=2022-12-31"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok
    pprint(response.json())
    assert response.json()[0][0] == 200

# List records
# ^^^^^^^^^^^^

def test_list_with_limit(url, headers):
    """
    Test case for listing the records in the database, with limit.
    """
    endpoint = "resources/ctxt/list?limit=50"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok
    pprint(response.json())
    assert len(response.json()) == 50  # Should equal 50

def test_list_with_from_limit(url, headers):
    """
    Test case for listing the records in the database, with limit, for a specific assetId within a from-to range.
    """
    endpoint = "resources/ctxt/list?from=2022-09-30T17:53:00&limit=15"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok
    pprint(response.json())
    assert len(response.json()) == 15  # Should equal 15

def test_list_with_to_limit(url, headers):
    """
    Test case for listing the records in the database, with limit, for a specific assetId within a from-to range.
    """
    endpoint = "resources/ctxt/list?to=2022-12-31&limit=15"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok
    pprint(response.json())
    assert len(response.json()) == 15  # Should equal 15

def test_list_with_assetid_limit(url, headers):
    """
    Test case for listing the records in the database, with limit, for a specific assetId.
    """
    endpoint = "resources/ctxt/list?where=assetId=Okuma-4020&limit=20"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok
    pprint(response.json())
    assert len(response.json()) == 20  # Should equal 20

def test_list_with_assetid_range_limit(url, headers):
    """
    Test case for listing the records in the database, with limit, for a specific assetId within a from-to range.
    """
    endpoint = "resources/ctxt/list?where=assetId=Okuma-4020&from=2022-08-16&to=2022-12-31&limit=10"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok
    pprint(response.json())
    assert len(response.json()) == 10  # Should equal 10

def test_list_with_id_dataitemid_limit(url, headers):
    """
    Test case for listing the records in the database, for a specific dataItemId, Id falling in some range, with limit.
    """
    endpoint = "resources/ctxt/list?where=Id<=1024,dataItemId=Heartbeat&limit=10"
    response = requests.get(url(endpoint), headers=headers, timeout=50)
    assert response.ok, f"{response.text!r}"
    pprint(response.json())
    # assert len(response.json()) == 10  # Should equal 10

# TODO: Test case for listing the records in the database, for a specific dataItemId, value like some pattern, with limit.
# def test_list_with_dataitemid_value_like_limit(url, headers):
#     """
#     """
#     endpoint = "resources/ctxt/list?dataItemId=Mp1MacManPanelHistory&value_like='%2023/04/04 16:59%'&limit=10"
#     response = requests.get(url(endpoint), headers=headers, timeout=50)
#     pprint(response.json())
#     assert response.status_code == 200
#     assert len(response.json()) > 0