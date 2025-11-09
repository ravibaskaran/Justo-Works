#!/bin/bash
# Odoo 15 Database Backup Script
# Creates timestamped backup of PostgreSQL database

set -e  # Exit on any error

# Configuration from odoo.conf
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5434}"
DB_USER="${DB_USER:-odoo15_new}"
DB_NAME="${DB_NAME:-odoo15}"
DB_PASSWORD="${DB_PASSWORD:-odoo15_new}"

# Backup directory
BACKUP_DIR="${BACKUP_DIR:-$(dirname "$0")/../../backups/database}"
mkdir -p "$BACKUP_DIR"

# Timestamp for backup file
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="odoo15_db_${TIMESTAMP}.backup"
BACKUP_SQL="odoo15_db_${TIMESTAMP}.sql"

echo "========================================="
echo "Odoo 15 Database Backup"
echo "========================================="
echo "Database: $DB_NAME"
echo "Host: $DB_HOST:$DB_PORT"
echo "User: $DB_USER"
echo "Backup Directory: $BACKUP_DIR"
echo "========================================="

# Export password for pg_dump
export PGPASSWORD="$DB_PASSWORD"

# Create custom format backup (recommended for large databases)
echo "Creating custom format backup..."
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
    -F c -b -v -f "$BACKUP_DIR/$BACKUP_FILE" "$DB_NAME"

echo "✓ Custom format backup created: $BACKUP_FILE"

# Create SQL format backup (human-readable, for inspection)
echo "Creating SQL format backup..."
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
    -F p -b -v -f "$BACKUP_DIR/$BACKUP_SQL" "$DB_NAME"

echo "✓ SQL format backup created: $BACKUP_SQL"

# Compress SQL backup to save space
echo "Compressing SQL backup..."
gzip "$BACKUP_DIR/$BACKUP_SQL"

echo "✓ SQL backup compressed: ${BACKUP_SQL}.gz"

# Create a symlink to latest backup
ln -sf "$BACKUP_FILE" "$BACKUP_DIR/latest.backup"
ln -sf "${BACKUP_SQL}.gz" "$BACKUP_DIR/latest.sql.gz"

# Get backup size
BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
SQL_SIZE=$(du -h "$BACKUP_DIR/${BACKUP_SQL}.gz" | cut -f1)

echo "========================================="
echo "Backup Summary:"
echo "  Custom format: $BACKUP_SIZE ($BACKUP_FILE)"
echo "  SQL format:    $SQL_SIZE (${BACKUP_SQL}.gz)"
echo "  Location:      $BACKUP_DIR"
echo "========================================="
echo "✓ Database backup completed successfully!"

# List all backups in directory
echo ""
echo "Available backups:"
ls -lh "$BACKUP_DIR" | grep -E "\.backup$|\.sql\.gz$"

# Cleanup: Remove backups older than 30 days (optional, uncomment to enable)
# find "$BACKUP_DIR" -name "odoo15_db_*.backup" -mtime +30 -delete
# find "$BACKUP_DIR" -name "odoo15_db_*.sql.gz" -mtime +30 -delete

exit 0
