#!/usr/bin/env bash
set -e
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn django_clientes.wsgi:application --bind "0.0.0.0:${PORT:-8000}" --workers 1 --timeout 120
