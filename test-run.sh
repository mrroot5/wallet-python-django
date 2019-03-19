#!/usr/bin/env bash
# Activate env
. venv/bin/activate
python3 manage.py test -v 2 --failfast --traceback --exclude-tag=no-test api
