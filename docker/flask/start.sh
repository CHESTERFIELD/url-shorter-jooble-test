#!/bin/sh

##!/bin/bash
#
#flask db init
#flask db migrate
#flask db upgrade
#
#flask run -h '0.0.0.0' -p '8000'

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "$FLASK_ENV" = "development" ]
then
    echo "Creating the database tables..."
    python src/main.py create_db
    echo "Tables created"
fi

exec "$@"