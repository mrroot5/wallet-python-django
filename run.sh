#!/bin/sh
# Activate en
. env/bin/activate
# Migrations
python3 manage.py makemigrations api
python3 manage.py migrate
# Start server
python3 manage.py runserver 0.0.0.0:8000
