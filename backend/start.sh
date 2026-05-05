#!/bin/sh
set -e

echo "Starting backend service..."
echo "PORT: ${PORT:-8000}"
echo "DATABASE_URL set: $(if [ -n "$DATABASE_URL" ]; then echo 'yes'; else echo 'no'; fi)"

# Start server directly (no migrations/seed for debugging)
echo "Starting uvicorn on port ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --log-level debug
