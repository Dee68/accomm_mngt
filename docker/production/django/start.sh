#!/bin/bash

set -o errexit  # Exit immediately on command error
set -o pipefail # Fail pipeline if any command fails
set -o nounset  # Treat unset variables as errors

# Ensure the database is ready before running migrations
#echo "Checking database readiness..."
#python manage.py check --database default

#echo "Applying database migrations..."
#python manage.py migrate --no-input

echo "Collecting static files..."
python /app/manage.py collectstatic --noinput
echo "Applying database migrations..."
python /app/manage.py migrate 

NUM_WORKERS=${GUNICORN_WORKERS:-3}
echo "Starting  server..."
exec /usr/local/bin/gunicorn config.wsgi --bind 0.0.0.0:8000 --chdir=/app --workers $NUM_WORKERS