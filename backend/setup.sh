#!/bin/sh
python manage.py makemigrations api
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py loaddata initial_data.json
python manage.py collectstatic --noinput
nginx && gunicorn --bind 0.0.0.0:8000 reviveit_backend.wsgi:application