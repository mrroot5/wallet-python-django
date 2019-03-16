#!/bin/sh
# Activate en
. venv/bin/activate
# Migrations
python3 manage.py makemigrations api
python3 manage.py migrate
# Start server
python3 manage.py runserver 0.0.0.0:8000
