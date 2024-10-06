#!/bin/sh
python manage.py makemigrations items
python manage.py migrate &&
python manage.py createsuperuser --noinput &&
python manage.py loaddata initial_data.json &&
python manage.py runserver 0.0.0.0:8000