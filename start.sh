#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $BACKEND_POSTGRES_HOST $BACKEND_POSTGRES_CONTAINER_PORT; do
      sleep 1
    done

    echo "PostgreSQL started"
fi


echo "Running migrations..."
python manage.py makemigrations --noinput \
    && python manage.py migrate --noinput \
    && echo "Migrations complited"

echo "Downloading data..."
python manage.py makemigrations --noinput \
    && python manage.py migrate --noinput \
    && echo "Download complited"


echo "Collecting static files..."
python manage.py collectstatic --noinput \
    && echo "Static files collected"


echo "Creating superuser..."
echo "from users.models import User; \
      User.objects.filter(email='$EMAIL').delete(); \
      User.objects.create_superuser('$LOGIN', '$EMAIL', '$PASSWORD')" \
      | python manage.py shell \
      && echo "Superuser created"

echo "Starting gunicorn..." \
    && gunicorn mvp_crm.wsgi:application --bind 0.0.0.0:8000 --reload

exec "$@"
