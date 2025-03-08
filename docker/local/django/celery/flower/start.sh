#!/bin/bash

set -o errexit  # Exit immediately on command error
set -o pipefail # Fail pipeline if any command fails
set -o nounset  # Treat unset variables as errors


exec watchfiles --filter python celery.__main__.main \
    --args \
    "-A config.celery_app -b \"${CELERY_BROKER_URL}\" flower --basic_auth=\"${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}\""
# set -o errexit  # Exit immediately on command error
# set -o pipefail # Fail pipeline if any command fails
# set -o nounset  # Treat unset variables as errors

# trap 'echo "Stopping Celery Flower..."; exit 0' SIGTERM SIGINT

# exec watchfiles --filter python celery.__main__.main --args \
# "-A config.celery_app -b ${CELERY_BROKER_URL} flower --basic_auth=${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}" || {
#     echo "Flower crashed. Restarting..."
#     exec watchfiles --filter python celery.__main__.main --args \
#     "-A config.celery_app -b ${CELERY_BROKER_URL} flower --basic_auth=${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"
# }