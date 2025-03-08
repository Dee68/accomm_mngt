#!/bin/bash

set -o errexit  # Exit immediately on command error
set -o pipefail # Fail pipeline if any command fails
set -o nounset  # Treat unset variables as errors

APP_HOME="/app"  # Set working directory path

rm -f '${APP_HOME}/celerybeat.pid' # Remove stale pid

trap 'echo "Stopping Celery Beat..."; exit 0' SIGTERM SIGINT  # Handle shutdown signals
exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app beat -l INFO'

# exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app beat -l INFO' || {
#     echo "$(date) - Celery Beat crashed. Restarting..." >> /var/log/celery_beat.log
#     exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app beat -l INFO'
# }