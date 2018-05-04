#!/bin/bash

# this script presumes you have installed a VirtualEnv in 'venv' and 
# run 'pip install -r requirements'.
#
source venv/bin/activate
export FLASK_APP=app.py
export FLASK_DEBUG=1
export SQL_URI=postgresql+psycopg2://username:password@localhost/track_usage_test
export FREEGEOIP_API_KEY=REAL_KEY_GOES_HERE
flask run
