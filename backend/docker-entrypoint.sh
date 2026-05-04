#!/bin/sh
set -e

# Run migrations for main database
alembic upgrade head

# If command is "test", setup test db and run pytest
if [ "$1" = "test" ]; then
    shift
    # Create test database if not exists
    echo "Creating test database if not exists..."
    psql "$DATABASE_URL_TEST" -c "SELECT 1;" 2>/dev/null || \
        psql "postgresql://${POSTGRES_USER:-musicapp}:${POSTGRES_PASSWORD:-musicapp123}@db:5432/postgres" \
            -c "CREATE DATABASE musicdb_test;" 2>/dev/null || true

    # Run migrations on test database
    export DATABASE_URL="$DATABASE_URL_TEST"
    alembic upgrade head

    # Run tests
    exec python -m pytest "$@"
fi

# If command is "server", run seed + uvicorn
if [ "$1" = "server" ]; then
    python -m app.db.seed
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi

# Otherwise, run whatever command is provided
exec "$@"
