#!/bin/bash
# Reset Test Database
# Drops and recreates a test database

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
    echo "Drops and recreates an empty test database"
    echo ""
    echo "Examples:"
    echo "  $0 odoo18_test"
    exit 1
}

# Check arguments
if [ $# -eq 0 ]; then
    usage
fi

DB_NAME="$1"

echo "========================================="
echo "Reset Test Database"
echo "========================================="
echo "⚠ WARNING: This will DELETE all data in '$DB_NAME'"
echo "========================================="

read -p "Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Operation cancelled."
    exit 0
fi

# Export password
export PGPASSWORD="$DB_PASSWORD"

echo ""
echo "Dropping database..."
dropdb -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" --if-exists "$DB_NAME"
echo "✓ Database dropped"

echo ""
echo "Creating fresh database..."
createdb -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
    -O "$DB_USER" \
    -E UTF8 \
    -T template0 \
    "$DB_NAME"

echo "✓ Database created"

# Create extensions
echo ""
echo "Creating extensions..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" << EOF
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;
EOF

echo "✓ Extensions created"

echo ""
echo "========================================="
echo "✓ Database reset complete!"
echo "========================================="
echo "Database '$DB_NAME' is ready to use"

exit 0
