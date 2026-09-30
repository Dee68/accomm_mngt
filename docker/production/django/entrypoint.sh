#!/bin/bash

set -o errexit  # Exit immediately on command error
set -o pipefail # Fail pipeline if any command fails
set -o nounset  # Treat unset variables as errors

>&2 echo "Waiting for PostgreSQL to become available..."

suggest_unrecoverable_after=30
start=$(date +%s)

while true; do
    python3 - <<EOF
import os
import sys
import time
import psycopg2

try:
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )
    conn.close()
except psycopg2.OperationalError as error:
    sys.stderr.write("Waiting for PostgreSQL to become available...\n")
    if time.time() - ${start} > ${suggest_unrecoverable_after}:
        sys.stderr.write("This is taking longer than expected. Possible unrecoverable error: '{}'\n".format(error))
        time.sleep(1)
    sys.exit(1)  # Prevent infinite loop
EOF

    # If successful, break the loop
    if [[ $? -eq 0 ]]; then
        break
    fi

    sleep 1
done

>&2 echo "PostgreSQL is available!"

# Execute the command provided as arguments
exec "$@"