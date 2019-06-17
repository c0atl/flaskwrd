#!/usr/bin/env bash

CONTAINER_PASSWD_PATH=/var/passwd
CONTAINER_GROUP_PATH=/var/group

PASSWD_LN=/tmp/passwd_ln
GROUP_LN=/tmp/group_ln

echo $0
echo $1
echo $2

if [ "$1" != "" ]; then
    PASSWD_FILE=$1
    echo "Passwd from cmd line"
else 
    PASSWD_FILE=/etc/passwd
    echo "passwd from default"
fi
if [ "$2" != "" ]; then
  GROUP_FILE=$2
  echo "Group from cmd line"
else 
  GROUP_FILE=/etc/group
  echo "group from default"
fi

if test -f "$PASSWD_LN"; then
  rm "$PASSWD_LN"
  echo "removed old passwd file link"
fi

if test -f "$GROUP_LN"; then
  rm "$GROUP_LN"
  echo "removed old group file link"
fi

echo "Password file: $PASSWD_FILE"
echo "Group file: $GROUP_FILE"
ln -s $PASSWD_FILE $PASSWD_LN
ln -s $GROUP_FILE $GROUP_LN
docker run -v $PASSWD_LN:$CONTAINER_PASSWD_PATH -v $GROUP_LN:$CONTAINER_GROUP_PATH -d -p 5000:5000 flaskwrd
