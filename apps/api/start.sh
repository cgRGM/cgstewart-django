#!/bin/bash

# Exit on any error
set -e

echo "Starting Django application..."

# Run migrations
echo "Running database migrations..."
uv run python manage.py migrate --noinput

# Create admin user
echo "Creating admin user..."
uv run python manage.py create_admin_user

# Start gunicorn
echo "Starting gunicorn server..."
exec uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2
