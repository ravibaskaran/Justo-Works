# OpenUpgrade - Odoo 15→18 Migration Framework

OpenUpgrade provides migration scripts to upgrade Odoo databases across versions.

## Overview

OpenUpgrade handles:
- Database schema migrations
- Model field renames and removals
- XML ID updates
- Data transformations
- Module dependency changes

## Installation

### 1. Clone OpenUpgrade

```bash
cd migration/openupgrade

# Clone OpenUpgrade 18.0 branch
git clone --branch 18.0 --depth 1 https://github.com/OCA/OpenUpgrade.git
cd OpenUpgrade

# Verify branch
git branch
```

### 2. Install Dependencies

```bash
# Install OpenUpgrade requirements
pip3 install -r requirements.txt
```

## Migration Path: 15.0 → 18.0

Odoo doesn't support direct migration from 15.0 to 18.0. You must migrate through intermediate versions:

```
15.0 → 16.0 → 17.0 → 18.0
```

Each step requires:
1. OpenUpgrade branch for target version
2. Database backup before migration
3. Migration execution
4. Data validation after migration

## Directory Structure

```
migration/openupgrade/
├── OpenUpgrade/              # Cloned OCA repository
│   ├── odoo/                 # Odoo core with migration scripts
│   ├── addons/               # Standard addons
│   └── openupgrade_scripts/  # Migration scripts
├── custom_scripts/           # Custom module migration scripts
│   ├── 15.0/                 # Odoo 15 → 16 migrations
│   ├── 16.0/                 # Odoo 16 → 17 migrations
│   └── 17.0/                 # Odoo 17 → 18 migrations
├── run_migration.sh          # Migration execution script
└── README.md                 # This file
```

## Migration Execution

### Step 1: Prepare Database

```bash
# Backup Odoo 15 database
cd ../../backup
./backup_database.sh

# Create test database for migration
cd ../database
./create_test_db.sh odoo15_to_16_test
```

### Step 2: Restore Odoo 15 Backup

```bash
# Restore to test database
cd ../backup
./restore_database.sh latest.backup odoo15_to_16_test
```

### Step 3: Run 15.0 → 16.0 Migration

```bash
cd ../openupgrade/OpenUpgrade

# Set database configuration
export PGHOST=localhost
export PGPORT=5434
export PGUSER=odoo15_new
export PGPASSWORD=odoo15_new
export PGDATABASE=odoo15_to_16_test

# Run migration to 16.0
python3 odoo-bin -d odoo15_to_16_test \
  --upgrade-path=15.0,16.0 \
  --update=all \
  --stop-after-init \
  --log-level=debug \
  --logfile=/tmp/openupgrade_15_to_16.log
```

### Step 4: Run 16.0 → 17.0 Migration

```bash
# Checkout OpenUpgrade 17.0 branch
cd ../
git clone --branch 17.0 --depth 1 https://github.com/OCA/OpenUpgrade.git OpenUpgrade-17.0
cd OpenUpgrade-17.0

# Run migration to 17.0
python3 odoo-bin -d odoo15_to_16_test \
  --upgrade-path=16.0,17.0 \
  --update=all \
  --stop-after-init \
  --log-level=debug \
  --logfile=/tmp/openupgrade_16_to_17.log
```

### Step 5: Run 17.0 → 18.0 Migration

```bash
# Checkout OpenUpgrade 18.0 branch
cd ../
git clone --branch 18.0 --depth 1 https://github.com/OCA/OpenUpgrade.git OpenUpgrade-18.0
cd OpenUpgrade-18.0

# Run migration to 18.0
python3 odoo-bin -d odoo15_to_16_test \
  --upgrade-path=17.0,18.0 \
  --update=all \
  --stop-after-init \
  --log-level=debug \
  --logfile=/tmp/openupgrade_17_to_18.log
```

## Custom Module Migration

Custom modules require migration scripts for each version transition.

### Create Custom Migration Scripts

```bash
cd ../custom_scripts

# Create migration directory for custom module
mkdir -p 15.0/itsys_real_estate/migrations/15.0.1.0.0
```

### Migration Script Template

Create `pre-migration.py`:

```python
# -*- coding: utf-8 -*-
# Migration script for itsys_real_estate: 15.0 → 16.0

def migrate(cr, version):
    """Pre-migration script"""
    # Rename fields
    cr.execute("""
        ALTER TABLE real_estate_property
        RENAME COLUMN old_field TO new_field
    """)

    # Update XML IDs
    cr.execute("""
        UPDATE ir_model_data
        SET name = 'new_view_id'
        WHERE name = 'old_view_id'
        AND module = 'itsys_real_estate'
    """)

    # Add new required fields with default values
    cr.execute("""
        ALTER TABLE real_estate_property
        ADD COLUMN new_required_field VARCHAR(255) DEFAULT 'default_value'
    """)
```

Create `post-migration.py`:

```python
# -*- coding: utf-8 -*-
# Post-migration script for itsys_real_estate: 15.0 → 16.0

def migrate(cr, version):
    """Post-migration script"""
    # Clean up deprecated data
    cr.execute("""
        DELETE FROM ir_cron
        WHERE model = 'real.estate.property'
        AND function = 'deprecated_method'
    """)

    # Recompute fields
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})

    properties = env['real.estate.property'].search([])
    properties._compute_total_value()
```

## Migration Checklist

### Before Migration

- [ ] Full backup of production database
- [ ] Backup of filestore
- [ ] List of all installed modules
- [ ] List of custom modifications
- [ ] Test database created
- [ ] OpenUpgrade 16.0, 17.0, 18.0 cloned
- [ ] Custom migration scripts prepared
- [ ] Sufficient disk space (3x database size)

### During Migration

- [ ] Monitor logs for errors
- [ ] Note any warnings or deprecated features
- [ ] Track migration time for each version
- [ ] Verify no data loss during migration

### After Migration

- [ ] Database connects successfully
- [ ] All modules listed as installed
- [ ] No errors in server logs
- [ ] All custom modules load correctly
- [ ] Data validation passed
- [ ] Proceed to validation phase

## Common Migration Issues

### 1. Missing Dependencies

**Error**: `Module X depends on module Y which is not installed`

**Solution**:
```bash
# Install missing module before migration
python3 odoo-bin -d database_name -i missing_module --stop-after-init
```

### 2. Deprecated Fields

**Error**: `Unknown field 'old_field' in model 'model.name'`

**Solution**: Create pre-migration script to rename field

### 3. XML ID Conflicts

**Error**: `Duplicate XML ID: module.xml_id`

**Solution**: Update XML IDs in pre-migration script

### 4. Database Constraints

**Error**: `Not null constraint violation on field 'new_field'`

**Solution**: Add default values in pre-migration script

### 5. Custom Module Errors

**Error**: `Module custom_module could not be loaded`

**Solution**: Update manifest, fix imports, update deprecated code

## Migration Scripts Location

OpenUpgrade migration scripts are in:
```
OpenUpgrade/openupgrade_scripts/scripts/module_name/16.0.1.0/
├── pre-migration.py     # Runs before module upgrade
├── post-migration.py    # Runs after module upgrade
└── upgrade_analysis_work.txt  # Analysis notes
```

## Automated Migration Script

Use the provided script for automated migration:

```bash
cd migration/openupgrade
./run_migration.sh odoo15_backup.sql odoo18_migrated
```

This script:
1. Creates test database
2. Restores Odoo 15 backup
3. Runs 15→16→17→18 migration
4. Validates results
5. Generates migration report

## Testing Migration

### 1. Dry Run

```bash
# Test migration without committing
python3 odoo-bin -d test_db --upgrade-path=15.0,16.0 --test-enable --stop-after-init
```

### 2. Validate Data

```bash
# Connect to migrated database
psql -h localhost -p 5434 -U odoo15_new -d odoo18_migrated

# Check record counts
SELECT COUNT(*) FROM res_partner;
SELECT COUNT(*) FROM sale_order;
SELECT COUNT(*) FROM account_move;

# Check module states
SELECT name, state FROM ir_module_module WHERE state != 'uninstalled';
```

### 3. Test Custom Modules

```bash
# Start Odoo 18 with migrated database
python3 odoo-bin -d odoo18_migrated

# Navigate to each custom module
# Test CRUD operations
# Verify reports generate correctly
# Check scheduled actions run
```

## Resources

- [OpenUpgrade Documentation](https://github.com/OCA/OpenUpgrade/)
- [OCA Migration Guide](https://github.com/OCA/OpenUpgrade/wiki)
- [Odoo Migration Best Practices](https://www.odoo.com/documentation/18.0/developer/howtos/upgrade_custom_db.html)

## Support

Common issues and solutions:
- Check OpenUpgrade issue tracker: https://github.com/OCA/OpenUpgrade/issues
- Odoo Community Forum: https://www.odoo.com/forum
- OCA Mailing List: https://odoo-community.org/

## Next Steps

After OpenUpgrade setup:
1. Create custom migration scripts for all 112 custom modules
2. Test migration on copy of production database
3. Validate migrated data
4. Proceed to Phase 4: Database Migration
