#!/bin/bash
# Master Backup Script - Backs up everything
# Runs all backup scripts in sequence

set -e  # Exit on any error

SCRIPT_DIR="$(dirname "$0")"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "========================================="
echo "Odoo 15 Complete Backup"
echo "Started: $(date)"
echo "========================================="
echo ""

# Track success/failure
BACKUP_STATUS=()

# Function to run backup and track status
run_backup() {
    local script=$1
    local name=$2

    echo "========================================="
    echo "Running: $name"
    echo "========================================="

    if bash "$SCRIPT_DIR/$script"; then
        BACKUP_STATUS+=("✓ $name")
        echo ""
        echo "✓ $name completed successfully"
    else
        BACKUP_STATUS+=("✗ $name FAILED")
        echo ""
        echo "✗ $name failed!"
        return 1
    fi

    echo ""
}

# Run all backup scripts
run_backup "backup_database.sh" "Database Backup" || true
run_backup "backup_filestore.sh" "Filestore Backup" || true
run_backup "backup_custom_modules.sh" "Custom Modules Backup" || true
run_backup "backup_config.sh" "Configuration Backup" || true

# Summary
echo "========================================="
echo "Backup Summary"
echo "========================================="
for status in "${BACKUP_STATUS[@]}"; do
    echo "$status"
done

echo ""
echo "Completed: $(date)"
echo "========================================="

# Check if all succeeded
if [[ " ${BACKUP_STATUS[@]} " =~ " ✗ " ]]; then
    echo "⚠ Some backups failed! Please check the output above."
    exit 1
else
    echo "✓ All backups completed successfully!"
    echo ""
    echo "Backup locations:"
    echo "  Database:      $(dirname "$0")/../../backups/database/"
    echo "  Filestore:     $(dirname "$0")/../../backups/filestore/"
    echo "  Modules:       $(dirname "$0")/../../backups/modules/"
    echo "  Configuration: $(dirname "$0")/../../backups/config/"
    exit 0
fi
