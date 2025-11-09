# Odoo 15 Backup & Restore Scripts

Complete backup and restoration system for Odoo 15→18 migration.

## Quick Start

### Create Complete Backup

```bash
cd migration/backup
./backup_all.sh
```

This runs all backup scripts and creates:
- Database backup (PostgreSQL dump)
- Filestore backup (attachments, images)
- Custom modules backup (source code)
- Configuration backup (odoo.conf, requirements.txt)

### Restore from Backup

```bash
# Restore database
./restore_database.sh [backup_file] [target_db_name]

# Restore filestore
./restore_filestore.sh [backup_file] [target_dir] [db_name]
```

## Individual Backup Scripts

### 1. Database Backup

```bash
./backup_database.sh
```

Creates two formats:
- **Custom format** (`.backup`) - Binary, optimized for pg_restore
- **SQL format** (`.sql.gz`) - Text, human-readable, compressed

**Environment Variables:**
```bash
export DB_HOST=localhost
export DB_PORT=5434
export DB_USER=odoo15_new
export DB_PASSWORD=odoo15_new
export DB_NAME=odoo15
export BACKUP_DIR=../../backups/database
```

**Output:**
- `backups/database/odoo15_db_YYYYMMDD_HHMMSS.backup`
- `backups/database/odoo15_db_YYYYMMDD_HHMMSS.sql.gz`
- `backups/database/latest.backup` (symlink)

### 2. Filestore Backup

```bash
./backup_filestore.sh
```

Backs up Odoo filestore directory (attachments, images, documents).

**Environment Variables:**
```bash
export FILESTORE_DIR=~/.local/share/Odoo/filestore/odoo15
export BACKUP_DIR=../../backups/filestore
```

**Output:**
- `backups/filestore/odoo15_filestore_YYYYMMDD_HHMMSS.tar.gz`
- `backups/filestore/latest.tar.gz` (symlink)

### 3. Custom Modules Backup

```bash
./backup_custom_modules.sh
```

Backs up all custom module source code from:
- `addons_custom/` (20 modules)
- `common/` (shared modules)
- `reports15/` (custom reports)
- `themes15/` (custom themes)

**Output:**
- `backups/modules/odoo15_custom_modules_YYYYMMDD_HHMMSS.tar.gz`
- `backups/modules/latest.tar.gz` (symlink)

### 4. Configuration Backup

```bash
./backup_config.sh
```

Backs up configuration files:
- `odoo.conf`
- `requirements.txt`
- `.gitignore`
- `setup.py`, `setup.cfg`

**Output:**
- `backups/config/odoo15_config_YYYYMMDD_HHMMSS.tar.gz`

## Restore Scripts

### Restore Database

```bash
./restore_database.sh [backup_file] [target_db_name]
```

**Examples:**
```bash
# Restore latest backup to default database (odoo15_restored)
./restore_database.sh

# Restore specific backup
./restore_database.sh ../../backups/database/odoo15_db_20231109_143022.backup

# Restore to custom database name
./restore_database.sh ../../backups/database/latest.backup odoo18_test
```

**Actions:**
1. Drops target database if exists
2. Creates new empty database
3. Restores from backup file
4. Verifies restoration

### Restore Filestore

```bash
./restore_filestore.sh [backup_file] [target_dir] [db_name]
```

**Examples:**
```bash
# Restore latest backup
./restore_filestore.sh

# Restore to custom location
./restore_filestore.sh ../../backups/filestore/latest.tar.gz ~/.local/share/Odoo/filestore odoo18_test

# Restore specific backup
./restore_filestore.sh ../../backups/filestore/odoo15_filestore_20231109_143022.tar.gz
```

## Backup Storage

All backups are stored in `../../backups/` relative to script location:

```
Justo-Works/
├── backups/
│   ├── database/       # PostgreSQL dumps
│   ├── filestore/      # Attachment archives
│   ├── modules/        # Custom module code
│   └── config/         # Configuration files
└── migration/
    └── backup/         # ← Scripts location
```

## Before Migration Checklist

- [ ] Run `./backup_all.sh` to create complete backup
- [ ] Verify all backup files created successfully
- [ ] Test restoration on separate database
- [ ] Document backup sizes and locations
- [ ] Ensure sufficient disk space (3x database size recommended)
- [ ] Store backups on separate storage/server
- [ ] Test backup restoration procedure

## Backup Retention

By default, backups are retained indefinitely. To enable automatic cleanup (30-day retention), uncomment the cleanup lines at the end of each backup script:

```bash
# Cleanup: Remove backups older than 30 days
find "$BACKUP_DIR" -name "odoo15_db_*.backup" -mtime +30 -delete
```

## Troubleshooting

### Database Backup Fails

**Issue:** `pg_dump: error: connection to database failed`

**Solutions:**
1. Check PostgreSQL is running: `systemctl status postgresql`
2. Verify connection settings (host, port, user, password)
3. Test connection: `psql -h localhost -p 5434 -U odoo15_new -d odoo15`
4. Check pg_hba.conf allows local connections

### Filestore Not Found

**Issue:** `WARNING: Filestore directory not found`

**Solutions:**
1. Check odoo.conf for data_dir setting
2. Look for filestore in common locations:
   - `~/.local/share/Odoo/filestore/<db_name>`
   - `/var/lib/odoo/filestore/<db_name>`
   - Custom path from data_dir
3. Run `find / -name filestore -type d 2>/dev/null`

### Insufficient Disk Space

**Issue:** `No space left on device`

**Solutions:**
1. Check disk space: `df -h`
2. Clean up old backups
3. Use external storage for backups
4. Compress SQL backups (already done automatically)

## Security Notes

- Backup files contain sensitive data (database credentials, customer data)
- Store backups securely with appropriate permissions (chmod 600)
- Never commit backups to version control (already in .gitignore)
- Consider encrypting backup files for production systems
- Use secure transfer methods (scp, rsync over SSH) when moving backups

## Next Steps

After successful backup:
1. Proceed to Phase 1: Odoo 18 Environment Setup
2. Keep backups accessible for restoration during migration
3. Create additional backup before each major migration step
4. Document restoration procedure for production deployment
