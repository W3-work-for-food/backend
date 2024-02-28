#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $BACKEND_POSTGRES_HOST $BACKEND_POSTGRES_CONTAINER_PORT; do
      sleep 1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate --noinput

gunicorn mvp_crm.wsgi:application --bind 0.0.0.0:8000 --reload

exec "$@"