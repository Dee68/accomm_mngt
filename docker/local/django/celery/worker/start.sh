#!/bin/bash

set -o errexit  # Exit immediately on command error
set -o pipefail # Fail pipeline if any command fails
set -o nounset  # Treat unset variables as errors

exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app worker -l INFO' || {
    echo "Celery worker crashed. Restarting..."
    exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app worker -l INFO'
}