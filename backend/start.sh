#!/bin/sh
set -e

echo "Starting backend service..."
echo "PORT: ${PORT:-8000}"
echo "DATABASE_URL set: $(if [ -n "$DATABASE_URL" ]; then echo 'yes'; else echo 'no'; fi)"

# Wait for database to be ready (try for 30 seconds)
if [ -n "$DATABASE_URL" ]; then
  echo "Waiting for database..."
  for i in $(seq 1 30); do
    if pg_isready -d "$DATABASE_URL" 2>/dev/null || \
       python -c "from sqlalchemy import create_engine; from urllib.parse import urlparse; import sys; e=create_engine('$DATABASE_URL'); e.connect().close()" 2>/dev/null; then
      echo "Database is ready!"
      break
    fi
    echo "Waiting for database... attempt $i/30"
    sleep 1
  done
fi

# Run migrations (don't fail if they error)
echo "Running migrations..."
alembic upgrade head || echo "WARNING: Migrations failed, continuing anyway..."

# Run seed (don't fail if it errors)
echo "Running seed..."
python -m app.db.seed || echo "WARNING: Seed failed, continuing anyway..."

# Start server
echo "Starting uvicorn on port ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers
