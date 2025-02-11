#!/bin/bash

set -o errexit  # Exit immediately on command error
set -o pipefail # Fail pipeline if any command fails
set -o nounset  # Treat unset variables as errors

# Ensure the database is ready before running migrations
echo "Checking database readiness..."
python manage.py check --database default

echo "Applying database migrations..."
python manage.py migrate --no-input

echo "Collecting static files..."
mkdir -p /app/staticfiles
chmod 775 /app/staticfiles
python manage.py collectstatic --no-input

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
