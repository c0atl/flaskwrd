# flaskwrd
Flask based webservice for querying from your /etc/passwd and /etc/group files. Seriously. 

## Requirements
* python3.7 or later
* Docker 18.09 or later
* Unix/Linux (Tested only on MacOS 10.14.5)

## Quickstart Guide
1. Clone this repo to your machine
2. To build the service, run build.sh
3. To start, run start.sh
4. Query your local machine on port 5000, (e.g., curl http://127.0.0.1:5000/)
5. (Cleanup) Shutdown/remove your docker container once you're through.

For information on how to stop and remove docker containers, visit the following:
https://docs.docker.com/engine/reference/commandline/stop/
https://docs.docker.com/engine/reference/commandline/rm/

# Config Options
You may change the path of the passwd/group files the server queries from by passing them as arguments to the start script in the format "./start.sh $PASSWD_FILE $GROUP_FILE". For example, to change the passwd file to "/var/passwd/" and the group file to "/var/group" on the host machine, run "./start.sh /var/passwd /var/group". 

Note that because these are positional arguments in bash, you must pass the both arguments in order to edit the group file path.

# Unit test
A simple unit test which tests the various endpoints will return 200 success has been included under "test/unit_test.py". To execute this, you must first prepare your python environment.

1. Source the setup script (e.g., "source setup.sh").

This will automatically create a virtual environment and install all necessary packages, as well as activate the environment.

2. Make sure the docker container has been built and is running (see above Quickstart guide)
3. Run the unit test script (E.g, ./tests/unit_test.py)

## API endpoints
- /users
Returns a list of users from the passwd file.

- /users/query[?name=<nq>][&uid=<uq>][&gid=<gq>][&comment=<cq>][&home=<hq>][&shell=<sq>]
Returns a list of users matching the query arguments passed.

- /users/<uid>
Returns a single user matching the uid. Will return 404 if no such user exists.

- /users/<uid>/groups
Returns a list of the groups the user with matching the uid is a member of. Will return 404 if no such user exists.

- /groups
Returns a list of groups from the group file.

- /groups/query[?name=<nq>][&gid=<gq>][&member=<mq1>][&member=<mq2>][&...]
Returns a list of the groups matching the query arguments passed. Multiple member fields may be passed.

- /groups/<gid>
Returns a single group matching the gid. Will return 404 if no such group exists.
