#!/bin/sh


if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgress..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        sleep 0.1
    done

    echo "Postgres starter"
fi

echo "**************************************"
python manage.py migrate
# python manage.py makemigrations
# python manage.py migrate
echo "**************************************"

echo "(----------------DB work!----------------)"

exec "$@"