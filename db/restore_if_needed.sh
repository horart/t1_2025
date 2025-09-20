#!/bin/bash
set -e

# Source the original postgres docker functions
. /usr/local/bin/docker-entrypoint.sh

# Export functions and environment for use in gosu subshells
export -f docker_temp_server_start
export -f docker_temp_server_stop
export POSTGRES_USER POSTGRES_DB

# If RESTORE_DUMP is set, restore the dump
if [ -n "$RESTORE_DUMP" ]; then
    echo ">>> [RESTORE MODE] Starting temporary PostgreSQL server as 'postgres' user..."

    # Start PostgreSQL in background as 'postgres' user
    gosu postgres bash -c 'docker_temp_server_start "$@"' -- "$@"

    # Run restore commands inside a postgres user shell
    gosu postgres bash -c '
        echo ">>> Waiting for PostgreSQL to become ready..."
        until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
            sleep 2
        done

        echo ">>> Dropping and recreating database: $POSTGRES_DB"
        psql -U "$POSTGRES_USER" -c "DROP DATABASE IF EXISTS $POSTGRES_DB;" 2>/dev/null || true
        psql -U "$POSTGRES_USER" -c "CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;"

        DUMP_FILE="/docker-entrypoint-restore/dump.sql"
        if [ ! -f "$DUMP_FILE" ]; then
            echo ">>> ❌ ERROR: Dump file not found: $DUMP_FILE" >&2
            exit 1
        fi

        echo ">>> 🚀 Restoring from $DUMP_FILE..."
        psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "$DUMP_FILE"

        echo ">>> ✅ Restore completed successfully."
    '

    # Stop temporary server
    gosu postgres bash -c 'docker_temp_server_stop'
    echo ">>> [RESTORE MODE] Temporary server stopped."
fi

# Start main PostgreSQL server (original entrypoint handles user switch)
exec docker-entrypoint.sh "$@"