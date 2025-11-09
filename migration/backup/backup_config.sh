#!/bin/bash
# Odoo 15 Configuration Backup Script
# Backs up configuration files and environment setup

set -e  # Exit on any error

# Configuration
ODOO_ROOT="${ODOO_ROOT:-$(dirname "$0")/../..}"
BACKUP_DIR="${BACKUP_DIR:-$(dirname "$0")/../../backups/config}"
mkdir -p "$BACKUP_DIR"

# Timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="odoo15_config_${TIMESTAMP}.tar.gz"

echo "========================================="
echo "Odoo 15 Configuration Backup"
echo "========================================="
echo "Odoo Root: $ODOO_ROOT"
echo "Backup Directory: $BACKUP_DIR"
echo "========================================="

# Change to Odoo root
cd "$ODOO_ROOT"

# Files to backup
CONFIG_FILES=(
    "odoo.conf"
    "requirements.txt"
    ".gitignore"
    "setup.py"
    "setup.cfg"
    "MANIFEST.in"
)

echo "Backing up configuration files:"
for file in "${CONFIG_FILES[@]}"; do
    if [ -f "$file" ]; then
        FILE_SIZE=$(du -h "$file" | cut -f1)
        echo "  ✓ $file ($FILE_SIZE)"
    else
        echo "  ⚠ $file - NOT FOUND (skipping)"
    fi
done

echo ""
echo "Creating backup archive..."

# Create tar archive
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    --files-from <(for f in "${CONFIG_FILES[@]}"; do [ -f "$f" ] && echo "$f"; done) \
    2>/dev/null || true

echo "✓ Configuration backup created: $BACKUP_FILE"

# Create symlink to latest
ln -sf "$BACKUP_FILE" "$BACKUP_DIR/latest.tar.gz"

# Backup size
BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)

echo "========================================="
echo "Backup Summary:"
echo "  Backup Size:  $BACKUP_SIZE"
echo "  Backup File:  $BACKUP_FILE"
echo "  Location:     $BACKUP_DIR"
echo "========================================="
echo "✓ Configuration backup completed!"

# List all backups
echo ""
echo "Available backups:"
ls -lh "$BACKUP_DIR" | grep "\.tar\.gz$"

exit 0
