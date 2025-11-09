#!/bin/bash
# Odoo Filestore Restore Script
# Restores filestore from backup

set -e  # Exit on any error

# Configuration
BACKUP_DIR="${BACKUP_DIR:-$(dirname "$0")/../../backups/filestore}"
RESTORE_DIR="${RESTORE_DIR:-$HOME/.local/share/Odoo/filestore}"

# Usage function
usage() {
    echo "Usage: $0 [backup_file.tar.gz] [target_directory] [database_name]"
    echo ""
    echo "If no backup file specified, will use latest.tar.gz"
    echo "If no target directory specified, will use: $RESTORE_DIR"
    echo "If no database name specified, will use: odoo15_restored"
    echo ""
    echo "Available backups:"
    ls -1 "$BACKUP_DIR"/*.tar.gz 2>/dev/null || echo "  No backups found in $BACKUP_DIR"
    exit 1
}

# Parse arguments
BACKUP_FILE="${1:-$BACKUP_DIR/latest.tar.gz}"
TARGET_DIR="${2:-$RESTORE_DIR}"
DB_NAME="${3:-odoo15_restored}"

# Show usage if requested
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    usage
fi

# Final restore path
FINAL_PATH="$TARGET_DIR/$DB_NAME"

echo "========================================="
echo "Odoo Filestore Restore"
echo "========================================="
echo "Backup File:   $BACKUP_FILE"
echo "Restore To:    $FINAL_PATH"
echo "========================================="

# Check if backup exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "✗ ERROR: Backup file not found: $BACKUP_FILE"
    echo ""
    usage
fi

# Create target directory if needed
mkdir -p "$TARGET_DIR"

# Confirm restore
if [ -d "$FINAL_PATH" ]; then
    echo ""
    echo "⚠ WARNING: Target directory already exists: $FINAL_PATH"
    read -p "Delete existing filestore and restore from backup? (yes/no): " CONFIRM

    if [ "$CONFIRM" != "yes" ]; then
        echo "Restore cancelled."
        exit 0
    fi

    echo "Removing existing filestore..."
    rm -rf "$FINAL_PATH"
    echo "✓ Existing filestore removed"
fi

echo ""
echo "Extracting backup..."
tar -xzf "$BACKUP_FILE" -C "$TARGET_DIR" --verbose 2>&1 | tail -n 20

# The backup contains "odoo15" directory, rename if needed
if [ -d "$TARGET_DIR/odoo15" ] && [ "$DB_NAME" != "odoo15" ]; then
    mv "$TARGET_DIR/odoo15" "$FINAL_PATH"
fi

# Count restored files
FILE_COUNT=$(find "$FINAL_PATH" -type f 2>/dev/null | wc -l)
FILESTORE_SIZE=$(du -sh "$FINAL_PATH" 2>/dev/null | cut -f1)

echo ""
echo "========================================="
echo "✓ Filestore restore completed!"
echo "========================================="
echo "Restored: $FILE_COUNT files ($FILESTORE_SIZE)"
echo "Location: $FINAL_PATH"
echo ""
echo "Update odoo.conf data_dir to point to: $TARGET_DIR"
echo "========================================="

exit 0
