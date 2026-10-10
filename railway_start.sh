#!/bin/bash
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

celery -A config worker -l info --concurrency=2 &

exec gunicorn config.wsgi