#!/bin/bash

python manage.py migrate
python manage.py collectstatic --no-input
gunicorn config.wsgi:application --bind 0:8000
