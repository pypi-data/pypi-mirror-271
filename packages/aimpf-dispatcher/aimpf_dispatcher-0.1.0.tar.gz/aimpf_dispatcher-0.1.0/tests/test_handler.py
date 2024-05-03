import os
import sys
sys.path.append(os.path.abspath("../_userland/handler"))

import json
import logging
import requests
from auth import AuthorizationAgent
from getpass import getpass
from pprint import pprint
from urllib import parse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# It can be convenient during development to enter a default username and
# password. When done, change default username and password to None.
username = "user1.root" or input("Enter your Carta username: ")
password = None or getpass(f"Enter the Carta password for {username}: ")


AUTH = AuthorizationAgent(username, password, url="https://api.sandbox.carta.contextualize.us.com")
print("Generated Authorization Agent.")
TOKEN = AUTH.token
print(f"Token: {TOKEN[:24]}...")
# When run as a Carta Service, X_CARTA_AUTH will replace Authorization
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "X_CARTA_TOKEN": f"Bearer {TOKEN}"
}
HOST = "t58bbyh0wg.execute-api.us-east-2.amazonaws.com/prod/"
# URL = lambda endpoint: "/".join(["https://" + HOST.strip("/"), parse.quote(endpoint.strip("/"))])
URL = lambda endpoint: "/".join(["https://" + HOST.strip("/"), endpoint.strip("/")])

# ##### Tests ##### #
# Check
print(f"Checking service is live at {URL('check')}")
response = requests.get(
    url=URL("/check"),
    headers=HEADERS
)
try:
    response.raise_for_status()
except requests.HTTPError as e:
    print(f"Response {e.response.status_code}: {e.response.reason}")
    sys.exit(1)
else:
    pprint(response.json())
# ########## Resources ########## #
# list
print(f"Listing resources at {URL('resources/list')}")
response = requests.get(
    url=URL("/resources/list"),
    headers=HEADERS
)
try:
    response.raise_for_status()
except requests.HTTPError as e:
    print(f"Response {e.response.status_code}: {e.response.reason}")
    sys.exit(1)
else:
    pprint(response.json())
# columns
RESOURCE = "db41"
print(f"List columns from db41 tables at {URL(f'/resources/{RESOURCE}/columns')}")
response = requests.get(
    url=URL(f"/resources/{RESOURCE}/columns"),
    headers=HEADERS
)
try:
    response.raise_for_status()
except requests.HTTPError as e:
    print(f"Response {e.response.status_code}: {e.response.reason}")
    sys.exit(1)
else:
    pprint(response.json())
    
# # assets
# RESOURCE = "db41"
# print(f"List assets from db41.Messages at {URL(f'/resources/{RESOURCE}/assets/list')}")
# response = requests.get(
#     url=URL(f"/resources/{RESOURCE}/assets/list"),
#     headers=HEADERS
# )
# try:
#     response.raise_for_status()
# except requests.HTTPError as e:
#     print(f"Response {e.response.status_code}: {e.response.reason}")
#     sys.exit(1)
# else:
#     pprint(response.json())
#     print(f"List assets from db41.Messages at {URL(f'/resources/{RESOURCE}/assets/list')}")

# assets, with limit
response = requests.get(
    url=URL(f"/resources/{RESOURCE}/assets/list?limit=10"),
    headers=HEADERS
)
try:
    response.raise_for_status()
except requests.HTTPError as e:
    print(f"Response {e.response.status_code}: {e.response.reason}")
    sys.exit(1)
else:
    pprint(response.json())

# # assets, in range
# response = requests.get(
#     url=URL(f"/resources/{RESOURCE}/assets/list?from=2023-04-03T00:00:00Z&to=2023-04-05T00:00:00Z"),
#     headers=HEADERS
# )
# try:
#     response.raise_for_status()
# except requests.HTTPError as e:
#     print(f"Response {e.response.status_code}: {e.response.reason}")
#     sys.exit(1)
# else:
#     pprint(response.json())

# # Projects
# print(f"Testing 'list' at {URL('projects')}")
# response = requests.get(
#     url=URL("projects"),
#     headers=HEADERS
# )
# try:
#     response.raise_for_status()
# except requests.HTTPError as e:
#     print(f"Response {e.response.status_code}: {e.response.reason}")
#     sys.exit(1)
# else:
#     pprint(response.json())
# # List schema
# url = URL("schema/list")
# print(f"Testing {url}")
# response = requests.get(
#     url=url,
#     params={"project": "Colorado Digital"},
#     headers=HEADERS
# )
# try:
#     response.raise_for_status()
# except requests.HTTPError as e:
#     print(f"Response {e.response.status_code}: {e.response.reason}")
#     sys.exit(1)
# else:
#     pprint(response.json())
# # List schema: invalid project
# url = URL("schema/list")
# print(f"Testing {url}")
# response = requests.get(
#     url=url,
#     params={"project": "ThisProjectDoesNotExist"},
#     headers=HEADERS
# )
# try:
#     response.raise_for_status()
# except requests.HTTPError as e:
#     print("Invalid project raises an error, as expected.")
# else:
#     print(f"Response {response.status_code}: {response.reason}")
#     print("Invalid project should raise an error, but didn't.")
#     sys.exit(1)
# # Create schema
# if len(sys.argv) < 2:
#     url = URL("schema/create")
#     content = json.dumps({"hello": "world"}).encode()
#     print(f"Testing {url}")
#     response = requests.post(
#         url=url,
#         params={"project": "Colorado Digital"},
#         files={"file": ("/json_schemas/delme2.json", content)},
#         headers=HEADERS
#     )
#     try:
#         response.raise_for_status()
#     except requests.HTTPError as e:
#         print(f"Response {e.response.status_code}: {e.response.reason}")
#         sys.exit(1)
#     else:
#         pprint(response.json())
# else:
#     # Test file operations
#     fileId = sys.argv[1]
#     print(f"Testing file operations on {fileId!r}")
#     # Set file permissions
#     group = "coloradodigital:All"
#     url = URL(f"schema/{fileId}/permissions/{group}")
#     print(f"Testing {url}")
#     response = requests.put(url, headers=HEADERS)
#     try:
#         response.raise_for_status()
#     except requests.HTTPError as e:
#         print(f"Response {e.response.status_code}: {e.response.reason}")
#         sys.exit(1)
#     else:
#         print(response.text)
#     # Retrieve file
#     url = URL(f"schema/{fileId}")
#     print(f"GET {url}")
#     response = requests.get(url, headers=HEADERS)
#     try:
#         response.raise_for_status()
#     except requests.HTTPError as e:
#         print(f"Response {e.response.status_code}: {e.response.reason}")
#         sys.exit(1)
#     else:
#         pprint(response.json())
#     # Update a file
#     content = json.dumps({"goodbye": "universe"}).encode()
#     url = URL(f"schema/{fileId}")
#     print(f"PATCH {url}")
#     response = requests.patch(url,
#         headers=HEADERS,
#         files={"file": ("/json_schemas/delme.json", content)})
#     try:
#         response.raise_for_status()
#     except requests.HTTPError as e:
#         print(f"Response {e.response.status_code}: {e.response.reason}")
#         sys.exit(1)
#     else:
#         pprint(response.text)
#     # Confirm updated file
#     url = URL(f"schema/{fileId}")
#     print(f"GET {url}")
#     response = requests.get(url, headers=HEADERS)
#     try:
#         response.raise_for_status()
#     except requests.HTTPError as e:
#         print(f"Response {e.response.status_code}: {e.response.reason}")
#         sys.exit(1)
#     else:
#         print(f"Files match: {response.content == content}")
#     # Delete a file
#     url = URL(f"schema/{fileId}")
#     print(f"DELETE {url}")
#     response = requests.delete(url, headers=HEADERS)
#     try:
#         assert response.status_code == 403, \
#             "Delete should return status code 403"
#         print("Response:", response.content)
#     except AssertionError:
#         print(f"Response {response.status_code}: {response.reason}")
#         sys.exit(1)
#     else:
#         print("Delete successful.")
