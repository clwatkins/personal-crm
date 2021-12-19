#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "$BACKEND_ENV" = "development" ]
then
    echo "Creating the database tables..."
    python manage.py create-db
    echo "Seeding database..."
    python manage.py seed-db
fi

exec "$@"