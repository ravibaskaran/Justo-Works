#!/bin/bash
# Odoo Database Restore Script
# Restores PostgreSQL database from backup

set -e  # Exit on any error

# Configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5434}"
DB_USER="${DB_USER:-odoo15_new}"
DB_PASSWORD="${DB_PASSWORD:-odoo15_new}"
BACKUP_DIR="${BACKUP_DIR:-$(dirname "$0")/../../backups/database}"

# Usage function
usage() {
    echo "Usage: $0 [backup_file.backup] [target_database_name]"
    echo ""
    echo "If no backup file specified, will use latest.backup"
    echo "If no database name specified, will use odoo15_restored"
    echo ""
    echo "Available backups:"
    ls -1 "$BACKUP_DIR"/*.backup 2>/dev/null || echo "  No backups found in $BACKUP_DIR"
    exit 1
}

# Parse arguments
BACKUP_FILE="${1:-$BACKUP_DIR/latest.backup}"
TARGET_DB="${2:-odoo15_restored}"

# Show usage if requested
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    usage
fi

echo "========================================="
echo "Odoo Database Restore"
echo "========================================="
echo "Backup File: $BACKUP_FILE"
echo "Target DB:   $TARGET_DB"
echo "Host:        $DB_HOST:$DB_PORT"
echo "User:        $DB_USER"
echo "========================================="

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "✗ ERROR: Backup file not found: $BACKUP_FILE"
    echo ""
    usage
fi

# Confirm restore
echo ""
read -p "⚠ This will DROP and recreate database '$TARGET_DB'. Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

# Export password
export PGPASSWORD="$DB_PASSWORD"

echo ""
echo "Step 1: Dropping existing database (if exists)..."
dropdb -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" --if-exists "$TARGET_DB"
echo "✓ Database dropped"

echo ""
echo "Step 2: Creating new database..."
createdb -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -O "$DB_USER" "$TARGET_DB"
echo "✓ Database created"

echo ""
echo "Step 3: Restoring from backup..."
echo "This may take several minutes..."
pg_restore -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
    -d "$TARGET_DB" -v "$BACKUP_FILE"

echo ""
echo "========================================="
echo "✓ Database restore completed!"
echo "========================================="
echo "Database '$TARGET_DB' is ready to use"
echo ""
echo "To connect:"
echo "  psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $TARGET_DB"
echo "========================================="

exit 0
