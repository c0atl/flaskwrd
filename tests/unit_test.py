#!/usr/bin/env python
import requests

# query data for the test data
user1 = "root"
user2 = "shoo"
uid = "0"
gid = "0"

# Metrics for which endpoint tests passed/failed
successes = []
failures = []
# GET users
response = requests.get("http://127.0.0.1:5000/users")
if response.status_code == 200:
    successes.append("/users")
else:
    failures.append("/users")

# GET users/query
response = requests.get("http://127.0.0.1:5000/users/query?name={}".format(user1))
if response.status_code == 200:
    successes.append("/users/query")
else:
    failures.append("/users/query")

# GET users/<uid>
response = requests.get("http://127.0.0.1:5000/users/{}".format(uid))
if response.status_code == 200:
    successes.append("/users/<uid>")
else:
    failures.append("/users/<uid>")

# GET users/<uid>/groups
response = requests.get("http://127.0.0.1:5000/users/{}/groups".format(uid))
if response.status_code == 200:
    successes.append("/users/<uid>/groups")
else:
    failures.append("/users/<uid>/groups")

# GET groups
response = requests.get("http://127.0.0.1:5000/groups")
if response.status_code == 200:
    successes.append("/groups")
else:
    failures.append("/groups")

# GET groups/query
response = requests.get("http://127.0.0.1:5000/groups/query")
if response.status_code == 200:
    successes.append("/groups/query")
else:
    failures.append("/groups/query")

# GET groups/<gid>
response = requests.get("http://127.0.0.1:5000/groups/{}".format(gid))
if response.status_code == 200:
    successes.append("/groups/<gid>")
else:
    failures.append("/groups/<gid>")

# Print report
print("SUCCESSFUL (200) ENDPOINT QUERIES:")
print(successes)

print("FAILED (NOT 200) ENDPOINT QUERIES:")
print(failures)
