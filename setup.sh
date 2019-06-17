#!/usr/bin/env bash
# filename: setup.sh
# Author: joseph clements
# Descrip: sets up a python virtual environment necessary for building the flask docker app
python3 -m venv venv3
source venv3/bin/activate
pip install -r requirements.txt
