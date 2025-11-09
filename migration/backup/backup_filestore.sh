#!/bin/bash
# Odoo 15 Filestore Backup Script
# Creates timestamped backup of Odoo filestore (attachments, images, documents)

set -e  # Exit on any error

# Configuration
# Default filestore location (can be overridden by odoo.conf data_dir)
FILESTORE_DIR="${FILESTORE_DIR:-$HOME/.local/share/Odoo/filestore/odoo15}"

# Alternative: Check odoo.conf for data_dir setting
# If your odoo.conf has data_dir set, update this path accordingly
# Example: FILESTORE_DIR="/path/to/data_dir/filestore/odoo15"

# Backup directory
BACKUP_DIR="${BACKUP_DIR:-$(dirname "$0")/../../backups/filestore}"
mkdir -p "$BACKUP_DIR"

# Timestamp for backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="odoo15_filestore_${TIMESTAMP}.tar.gz"

echo "========================================="
echo "Odoo 15 Filestore Backup"
echo "========================================="
echo "Filestore Path: $FILESTORE_DIR"
echo "Backup Directory: $BACKUP_DIR"
echo "========================================="

# Check if filestore directory exists
if [ ! -d "$FILESTORE_DIR" ]; then
    echo "⚠ WARNING: Filestore directory not found: $FILESTORE_DIR"
    echo "Please check your Odoo data_dir configuration"
    echo ""
    echo "Possible locations:"
    echo "  - ~/.local/share/Odoo/filestore/<db_name>"
    echo "  - /var/lib/odoo/filestore/<db_name>"
    echo "  - Custom path from odoo.conf data_dir setting"
    echo ""
    read -p "Enter correct filestore path (or press Ctrl+C to exit): " FILESTORE_DIR

    if [ ! -d "$FILESTORE_DIR" ]; then
        echo "✗ Directory still not found. Exiting."
        exit 1
    fi
fi

# Count files and calculate size
FILE_COUNT=$(find "$FILESTORE_DIR" -type f 2>/dev/null | wc -l)
FILESTORE_SIZE=$(du -sh "$FILESTORE_DIR" 2>/dev/null | cut -f1)

echo "Filestore contains: $FILE_COUNT files ($FILESTORE_SIZE)"
echo ""
echo "Creating compressed backup..."

# Create compressed tar archive with progress
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    -C "$(dirname "$FILESTORE_DIR")" \
    "$(basename "$FILESTORE_DIR")" \
    --verbose 2>&1 | tail -n 20  # Show last 20 files

echo ""
echo "✓ Filestore backup created: $BACKUP_FILE"

# Create symlink to latest backup
ln -sf "$BACKUP_FILE" "$BACKUP_DIR/latest.tar.gz"

# Get backup size
BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)

echo "========================================="
echo "Backup Summary:"
echo "  Source:       $FILESTORE_DIR"
echo "  Files:        $FILE_COUNT files"
echo "  Backup Size:  $BACKUP_SIZE"
echo "  Backup File:  $BACKUP_FILE"
echo "  Location:     $BACKUP_DIR"
echo "========================================="
echo "✓ Filestore backup completed successfully!"

# List all backups
echo ""
echo "Available backups:"
ls -lh "$BACKUP_DIR" | grep "\.tar\.gz$"

# Cleanup: Remove backups older than 30 days (optional, uncomment to enable)
# find "$BACKUP_DIR" -name "odoo15_filestore_*.tar.gz" -mtime +30 -delete

exit 0
