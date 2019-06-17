#!/usr/bin/env bash

CONTAINER_PASSWD_PATH=/var/passwd
CONTAINER_GROUP_PATH=/var/group

PASSWD_LN=/tmp/passwd_ln
GROUP_LN=/tmp/group_ln

if [ "$1" != "" ]; then
    PASSWD_FILE=$1
else 
    PASSWD_FILE=/etc/passwd
fi
if [ "$2" != "" ]; then
  GROUP_FILE=$2
else 
  GROUP_FILE=/etc/group
fi

if test -f "$PASSWD_LN"; then
  rm "$PASSWD_LN"
fi

if test -f "$GROUP_LN"; then
  rm "$GROUP_LN"
fi

ln -s $PASSWD_FILE $PASSWD_LN
ln -s $GROUP_FILE $GROUP_LN
docker run -v $PASSWD_LN:$CONTAINER_PASSWD_PATH -v $GROUP_LN:$CONTAINER_GROUP_PATH -d -p 5000:5000 flaskwrd
