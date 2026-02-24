#!/bin/bash

# Run migrations
python manage.py migrate --noinput

# Start gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application
