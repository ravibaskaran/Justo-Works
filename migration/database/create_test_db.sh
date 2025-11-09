#!/bin/bash
# Create Test Database for Odoo Migration
# Creates empty PostgreSQL database for testing migration

set -e  # Exit on any error

# Configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5434}"
DB_USER="${DB_USER:-odoo15_new}"
DB_PASSWORD="${DB_PASSWORD:-odoo15_new}"

# Usage function
usage() {
    echo "Usage: $0 <database_name>"
    echo ""
    echo "Creates a new PostgreSQL database for Odoo migration testing"
    echo ""
    echo "Examples:"
    echo "  $0 odoo18_test           # Create test database"
    echo "  $0 odoo15_to_16_test     # Create migration test database"
    echo "  $0 odoo18_prod           # Create production database"
    exit 1
}

# Check arguments
if [ $# -eq 0 ]; then
    echo "✗ ERROR: Database name required"
    echo ""
    usage
fi

DB_NAME="$1"

echo "========================================="
echo "Create Test Database"
echo "========================================="
echo "Database: $DB_NAME"
echo "Host:     $DB_HOST:$DB_PORT"
echo "User:     $DB_USER"
echo "========================================="

# Export password
export PGPASSWORD="$DB_PASSWORD"

# Check if database already exists
if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo ""
    echo "⚠ WARNING: Database '$DB_NAME' already exists!"
    read -p "Drop and recreate? (yes/no): " CONFIRM

    if [ "$CONFIRM" != "yes" ]; then
        echo "Operation cancelled."
        exit 0
    fi

    echo "Dropping existing database..."
    dropdb -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME"
    echo "✓ Existing database dropped"
fi

echo ""
echo "Creating database..."
createdb -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
    -O "$DB_USER" \
    -E UTF8 \
    -T template0 \
    "$DB_NAME"

echo "✓ Database created"

# Create required extensions
echo ""
echo "Creating PostgreSQL extensions..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" << EOF
-- Required for Odoo
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;

-- Optional: useful for debugging
-- CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Verify extensions
\dx
EOF

echo "✓ Extensions created"

# Verify database
echo ""
echo "Verifying database..."
DB_SIZE=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME'))")

echo "========================================="
echo "✓ Database created successfully!"
echo "========================================="
echo "Name:       $DB_NAME"
echo "Size:       $(echo $DB_SIZE | xargs)"
echo "Connection: psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME"
echo "========================================="

# List all databases
echo ""
echo "Available databases:"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -l | grep -E "odoo|Name"

exit 0
