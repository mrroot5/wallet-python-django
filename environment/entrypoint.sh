#!/bin/ash -e

if [ "$1" = 'web' ]; then
    echo 'Launching web'
    exec uvicorn django_atomic_transactions.asgi:application --host 0.0.0.0 --port "$PORT" --workers 2
fi

if [ "$1" = 'dev' ]; then
    echo 'Launching runserver'
    exec python manage.py runserver 0.0.0.0:"$PORT"
fi

if [ "$1" = 'migrate' ]; then
    echo 'Applying migrations'
    exec python manage.py migrate
fi

if [ "$1" = 'loaddata' ]; then
    echo 'Do you want to load initial data? CAUTION, this would erase all actual data [y/n]: '
    read -r loadit
    if [ "$loadit" == 'y' ] || [ "$loadit" == 'Y' ] || [ "$loadit" == '1' ]; then
        echo 'Loading initial data...'
        exec python manage.py migrate && python manage.py loaddata initial_data.json
    else
        exec echo 'Bye!'
    fi
fi

if [ "$1" = 'graph_models' ]; then
    exec echo 'Under development...'
#    exec python manage.py graph_models --pydot api -g -o graph-models.png
fi

exec "$@"
