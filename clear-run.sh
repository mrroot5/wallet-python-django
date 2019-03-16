#!/usr/bin/env bash
echo "Delete old database and migrations. . ."
rm db.sqlite3
rm -rf api/migrations
rm -rf api/__pycache__
rm -rf _autofixture
echo -e "Done\n"
echo "Create migrations and database. . ."
. venv/bin/activate
./manage.py makemigrations api
./manage.py migrate
echo -e "Done\n"
#echo "Create superuser. . ."
#./manage.py createsuperuser --username admin --email admin@dev.com
# python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'P@ssw0rd!')"
#echo -e "Done\n"
echo "Create plot graph model. . ."
./manage.py graph_models api -g -o graph-models.jpeg
echo -e "Done\n"
