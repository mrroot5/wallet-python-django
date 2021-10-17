#!/bin/ash -e

if [ "$1" = 'uvicorn' ]; then
    echo 'Launching web'
    exec uvicorn django_atomic_transactions.asgi:application --host 0.0.0.0 --port "$PORT" --workers 2
fi

if [ "$1" = 'dev' ]; then
    echo 'Launching runserver'
    exec python manage.py runserver 0.0.0.0:"$PORT"
fi

if [ "$1" = 'migrate' ]; then
    echo 'Applying migrations'
    python manage.py makemigrations commons api
    exec python manage.py migrate
fi

if [ "$1" = 'loaddata' ]; then
    exec python manage.py loaddata initial_data.json
fi

if [ "$1" = 'graph_models' ]; then
    exec echo 'Under development...'
#    exec python manage.py graph_models --pydot commons api -g -o graph-models.png
fi

if [ "$1" = 'test' ]; then
    exec python manage.py test --failfast
fi

exec "$@"
