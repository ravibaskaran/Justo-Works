#!/bin/bash
# Odoo 15 Custom Modules Backup Script
# Creates timestamped backup of all custom module source code

set -e  # Exit on any error

# Configuration
ODOO_ROOT="${ODOO_ROOT:-$(dirname "$0")/../..}"
BACKUP_DIR="${BACKUP_DIR:-$(dirname "$0")/../../backups/modules}"
mkdir -p "$BACKUP_DIR"

# Timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="odoo15_custom_modules_${TIMESTAMP}.tar.gz"

echo "========================================="
echo "Odoo 15 Custom Modules Backup"
echo "========================================="
echo "Odoo Root: $ODOO_ROOT"
echo "Backup Directory: $BACKUP_DIR"
echo "========================================="

# Change to Odoo root directory
cd "$ODOO_ROOT"

# Directories to backup
MODULES_DIRS=(
    "addons_custom"
    "common"
    "reports15"
    "themes15"
)

echo "Backing up custom modules from:"
for dir in "${MODULES_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        MODULE_COUNT=$(find "$dir" -maxdepth 1 -type d | wc -l)
        DIR_SIZE=$(du -sh "$dir" | cut -f1)
        echo "  ✓ $dir - $MODULE_COUNT items ($DIR_SIZE)"
    else
        echo "  ⚠ $dir - NOT FOUND (skipping)"
    fi
done

echo ""
echo "Creating compressed backup..."

# Create tar archive with all custom module directories
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='*.pyo' \
    --exclude='.git' \
    --exclude='node_modules' \
    "${MODULES_DIRS[@]}" \
    2>/dev/null || echo "Some directories may not exist (this is normal)"

echo "✓ Custom modules backup created: $BACKUP_FILE"

# Create symlink to latest backup
ln -sf "$BACKUP_FILE" "$BACKUP_DIR/latest.tar.gz"

# Get backup size
BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)

# Count total files in backup
FILE_COUNT=$(tar -tzf "$BACKUP_DIR/$BACKUP_FILE" | grep -v '/$' | wc -l)

echo "========================================="
echo "Backup Summary:"
echo "  Files backed up: $FILE_COUNT"
echo "  Backup Size:     $BACKUP_SIZE"
echo "  Backup File:     $BACKUP_FILE"
echo "  Location:        $BACKUP_DIR"
echo "========================================="
echo "✓ Custom modules backup completed successfully!"

# List all backups
echo ""
echo "Available backups:"
ls -lh "$BACKUP_DIR" | grep "\.tar\.gz$"

# Cleanup: Remove backups older than 30 days (optional, uncomment to enable)
# find "$BACKUP_DIR" -name "odoo15_custom_modules_*.tar.gz" -mtime +30 -delete

exit 0
