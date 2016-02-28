#!/bin/bash

# Wait until postgres is ready
until nc -z db 5432; do
    echo "$(date) - waiting for postgres..."
    sleep 1
done

echo Running migrations
python manage.py migrate
# cd /src && python manage.py collectstatic --noinput  # Collect static files

if [ "$RUN_TYPE" = "runserver" ]
then
    echo Starting using manage.py runserver
    python manage.py runserver 0.0.0.0:8080
fi

if [ "$RUN_TYPE" = "wsgi" ]
then
    echo Starting using uwsg
    uwsgi --ini uwsgi.ini
fi

if [ "$RUN_TYPE" = "test" ]
then
    echo Running tests
    python manage.py test
fi
