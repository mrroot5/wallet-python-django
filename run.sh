#!/bin/sh
# Activate en
. venv/bin/activate
# Migrations
python3 manage.py makemigrations
python3 manage.py migrate
# Superuser
#python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'P@ssw0rd!')"

# Start server
python3 manage.py runserver 0.0.0.0:8000
