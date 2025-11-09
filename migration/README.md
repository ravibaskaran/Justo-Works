# Odoo 15→18 Migration Guide

Complete migration framework for upgrading Justo-Works from Odoo 15 to Odoo 18.

## Quick Navigation

- [Project Overview](#project-overview)
- [Migration Phases](#migration-phases)
- [Directory Structure](#directory-structure)
- [Quick Start](#quick-start)
- [Documentation](#documentation)

## Project Overview

**Current State:** Odoo 15 with:
- 40 Core modules
- 112 Custom modules (addons_custom, common, reports15, themes15)
- 387 Third-party modules
- 12 Theme modules
- **Total: 551 modules**

**Target State:** Odoo 18 with:
- All modules migrated and validated
- Complete data migration via OpenUpgrade
- Clean technical foundation (Python 3.11+, modern APIs)

## Migration Phases

### ✅ Phase 0: Security & Validation Fixes (COMPLETE)
Pre-migration security and validation fixes.

**Branch:** `claude/openspec-ai-branch-policy-011CUvg4v8NQhY1UST4u22fR`

### 🔄 Phase 1: Odoo 18 Environment Setup (IN PROGRESS)
Establish migration environment and backup infrastructure.

**Branch:** `claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM`

**Key Deliverables:**
- ✅ Module inventory (551 modules documented)
- ✅ Backup scripts (database, filestore, modules, config)
- ✅ Odoo 18 Docker environment
- ✅ OpenUpgrade framework setup
- ✅ Database management scripts
- ✅ Complete documentation

**Status:** Ready to proceed to Phase 2

### ⏳ Phase 2: Core Module Validation (PENDING)
Validate all 40 core Odoo modules on Odoo 18.

**Goals:**
- Test core module functionality
- Verify workflows (Sale→Delivery→Invoice→Payment)
- Validate reports and scheduled actions
- Ensure data integrity

### ⏳ Phase 3: Custom Module Migration (PENDING)
Migrate 112 custom modules to Odoo 18.

**Goals:**
- Update manifests to 18.0
- Modernize Python code (decorators, ORM)
- Update XML views and templates
- Migrate JavaScript to OWL 2
- Test all custom functionality

### ⏳ Phase 4: Database Migration (PENDING)
Execute OpenUpgrade migration: 15.0→16.0→17.0→18.0

**Goals:**
- Migrate database schema and data
- Apply custom migration scripts
- Validate data integrity
- Verify all records migrated

### ⏳ Phase 5: Automation, Security & Performance (PENDING)
Validate system automation, security, and performance.

**Goals:**
- Test scheduled jobs
- Verify user permissions
- Validate integrations
- Performance benchmarking

### ⏳ Phase 6: Post-Migration Validation & UAT (PENDING)
Final validation and user acceptance testing.

**Goals:**
- Comprehensive data validation
- User acceptance testing
- Production migration
- Client sign-off

## Directory Structure

```
migration/
├── README.md                   # This file - main migration guide
│
├── inventory/                  # Module inventory
│   ├── generate_module_list.py
│   ├── MODULE_INVENTORY.md
│   ├── odoo15_modules.csv
│   └── odoo15_modules.json
│
├── backup/                     # Backup and restore scripts
│   ├── README.md
│   ├── backup_all.sh          # Master backup script
│   ├── backup_database.sh
│   ├── backup_filestore.sh
│   ├── backup_custom_modules.sh
│   ├── backup_config.sh
│   ├── restore_database.sh
│   └── restore_filestore.sh
│
├── odoo18/                     # Odoo 18 environment
│   ├── README.md
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── odoo18.conf
│   └── requirements.txt
│
├── database/                   # Database management
│   ├── README.md
│   ├── create_test_db.sh
│   └── reset_test_db.sh
│
└── openupgrade/                # OpenUpgrade migration
    ├── README.md
    └── custom_scripts/         # Custom module migration scripts
        ├── 15.0/               # Odoo 15→16 migrations
        ├── 16.0/               # Odoo 16→17 migrations
        └── 17.0/               # Odoo 17→18 migrations
```

## Quick Start

### 1. Create Complete Backup

```bash
cd migration/backup
./backup_all.sh
```

This creates backups of:
- PostgreSQL database
- Filestore (attachments, images)
- Custom modules source code
- Configuration files

### 2. Start Odoo 18 Environment

```bash
cd migration/odoo18

# Build and start containers
docker-compose build
docker-compose up -d

# Verify Odoo 18 running
docker-compose exec odoo18 ./odoo-bin --version
# Output: Odoo Server 18.0

# Access: http://localhost:8069
```

### 3. Create Test Database

```bash
cd migration/database

# Create test database
./create_test_db.sh odoo18_test

# Verify
psql -h localhost -p 5434 -U odoo15_new -l | grep odoo18_test
```

### 4. Review Module Inventory

```bash
cd migration/inventory

# View inventory report
cat MODULE_INVENTORY.md

# Or open CSV in spreadsheet
open odoo15_modules.csv
```

### 5. Prepare for Migration

Review documentation:
- `migration/backup/README.md` - Backup procedures
- `migration/odoo18/README.md` - Odoo 18 setup
- `migration/openupgrade/README.md` - Migration process
- `migration/database/README.md` - Database management

## Migration Workflow

### Pre-Migration Checklist

- [ ] Full backup created and verified
- [ ] Module inventory reviewed (551 modules)
- [ ] Odoo 18 environment tested
- [ ] Test databases created
- [ ] OpenUpgrade cloned (16.0, 17.0, 18.0 branches)
- [ ] Sufficient disk space (3x database size)
- [ ] All documentation reviewed

### Migration Execution

1. **Backup Everything**
   ```bash
   cd migration/backup && ./backup_all.sh
   ```

2. **Create Test Database**
   ```bash
   cd migration/database && ./create_test_db.sh odoo15_to_16_test
   ```

3. **Restore Backup**
   ```bash
   cd migration/backup
   ./restore_database.sh latest.backup odoo15_to_16_test
   ```

4. **Run Migration 15→16**
   ```bash
   cd migration/openupgrade/OpenUpgrade
   python3 odoo-bin -d odoo15_to_16_test --upgrade-path=15.0,16.0 --update=all --stop-after-init
   ```

5. **Run Migration 16→17**
   ```bash
   cd ../OpenUpgrade-17.0
   python3 odoo-bin -d odoo15_to_16_test --upgrade-path=16.0,17.0 --update=all --stop-after-init
   ```

6. **Run Migration 17→18**
   ```bash
   cd ../OpenUpgrade-18.0
   python3 odoo-bin -d odoo15_to_16_test --upgrade-path=17.0,18.0 --update=all --stop-after-init
   ```

7. **Validate Results**
   ```bash
   cd migration/database
   # Connect and verify data
   psql -h localhost -p 5434 -U odoo15_new -d odoo15_to_16_test
   ```

### Post-Migration Validation

- [ ] Database migrated without errors
- [ ] All 551 modules installed
- [ ] Record counts match Odoo 15
- [ ] Workflows tested end-to-end
- [ ] Reports generate correctly
- [ ] Scheduled actions run
- [ ] Custom modules functional
- [ ] Performance acceptable
- [ ] User acceptance testing passed

## Key Documentation

### Module Inventory
- **Report:** `migration/inventory/MODULE_INVENTORY.md`
- **CSV:** `migration/inventory/odoo15_modules.csv`
- **JSON:** `migration/inventory/odoo15_modules.json`

### Backup Procedures
- **Guide:** `migration/backup/README.md`
- **Scripts:** `migration/backup/*.sh`

### Odoo 18 Setup
- **Guide:** `migration/odoo18/README.md`
- **Docker:** `migration/odoo18/docker-compose.yml`

### OpenUpgrade Migration
- **Guide:** `migration/openupgrade/README.md`

### Database Management
- **Guide:** `migration/database/README.md`
- **Scripts:** `migration/database/*.sh`

## Common Issues

### Backup Failed

**Issue:** Backup script fails with connection error

**Solution:**
```bash
# Check PostgreSQL running
systemctl status postgresql

# Verify credentials in odoo.conf
cat ../../odoo.conf

# Test connection
psql -h localhost -p 5434 -U odoo15_new -d odoo15
```

### Docker Build Failed

**Issue:** Docker build fails with network error

**Solution:**
```bash
# Check internet connectivity
ping github.com

# Use Docker cache
docker-compose build --no-cache

# Check Docker logs
docker-compose logs odoo18
```

### Migration Failed

**Issue:** OpenUpgrade migration fails

**Solution:**
```bash
# Check migration logs
cat /tmp/openupgrade_15_to_16.log

# Reset and retry
cd migration/database
./reset_test_db.sh odoo15_to_16_test
cd ../backup
./restore_database.sh latest.backup odoo15_to_16_test
```

## Security Notes

### Production Deployment

Before production migration:

1. **Change default passwords:**
   - PostgreSQL: Update in `docker-compose.yml`
   - Odoo admin: Update in `odoo18.conf`

2. **Secure database access:**
   - Don't expose PostgreSQL port externally
   - Use SSL connections
   - Implement firewall rules

3. **Backup strategy:**
   - Automated daily backups
   - Off-site backup storage
   - Test restore procedures

4. **Access control:**
   - Review user permissions
   - Audit access logs
   - Implement 2FA

## Performance Optimization

### Database

```sql
-- Vacuum and analyze
VACUUM ANALYZE;

-- Reindex
REINDEX DATABASE odoo18;

-- Update statistics
ANALYZE;
```

### Odoo Configuration

```ini
# In odoo18.conf
workers = 8                    # Based on CPU cores
max_cron_threads = 2
limit_memory_hard = 4294967296 # 4 GB
db_maxconn = 128
```

## Support & Resources

### Documentation
- [Odoo 18 Documentation](https://www.odoo.com/documentation/18.0/)
- [OpenUpgrade Wiki](https://github.com/OCA/OpenUpgrade/wiki)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

### Community
- [Odoo Forum](https://www.odoo.com/forum)
- [OCA Mailing List](https://odoo-community.org/)
- [GitHub Issues](https://github.com/OCA/OpenUpgrade/issues)

### Project Documentation
- Main project plan: `openspec/project.md`
- Phase 1 proposal: `openspec/changes/phase-1-odoo-18-environment-setup/proposal.md`
- Phase 1 tasks: `openspec/changes/phase-1-odoo-18-environment-setup/tasks.md`

## Next Steps

### Immediate (Phase 1 Complete)
- ✅ Environment setup complete
- ✅ Backup infrastructure ready
- ✅ Module inventory documented
- → **Commit and push Phase 1 changes**

### Phase 2 (Next)
- Start Odoo 18 environment
- Install core Odoo modules
- Test core functionality
- Validate against Odoo 15 baseline

### Future Phases
- Phase 3: Custom module migration
- Phase 4: OpenUpgrade database migration
- Phase 5: Security and performance validation
- Phase 6: UAT and production deployment

## Migration Timeline

Estimated timeline:
- ✅ Phase 0: Security fixes (Complete)
- ✅ Phase 1: Environment setup (Complete - 1 day)
- Phase 2: Core validation (2-3 days)
- Phase 3: Custom migration (5-7 days)
- Phase 4: Database migration (2-3 days)
- Phase 5: Validation (2-3 days)
- Phase 6: UAT & deployment (3-5 days)

**Total estimated: 15-22 days**

## Success Criteria

Phase 1 (Environment Setup) - ✅ COMPLETE:
- [x] Module inventory: 551 modules documented
- [x] Backup scripts: Database, filestore, modules, config
- [x] Odoo 18 environment: Docker setup complete
- [x] OpenUpgrade: Framework documented and ready
- [x] Database scripts: Test database creation ready
- [x] Documentation: Complete and comprehensive

**Phase 1 Status: ✅ READY FOR PHASE 2**
