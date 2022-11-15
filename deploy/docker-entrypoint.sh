#!/bin/sh
set -e ${DEBUG:+-x}

echo >&1 "=> Do database migrations..."
python3 /app/midi_tracker/manage.py migrate >&2
echo >&1 "=> Migrations completed."
exec "$@"