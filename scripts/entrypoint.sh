#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run python -m core.manage'

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

exec poetry run gunicorn core.main.wsgi:application --bind 0.0.0.0:8000