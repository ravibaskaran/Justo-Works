# Phase 1 Tasks: Odoo 18 Environment Setup

## Task 1: Module Inventory Generation ✅ IN PROGRESS

**Goal:** Document all installed modules in current Odoo 15 system

**Steps:**
1. Create `migration/inventory/` directory
2. Create Python script to generate module list from Odoo 15
3. Export installed modules with: name, version, state, category, dependencies
4. Categorize modules: Core (67), Custom (20), Third-party
5. Generate CSV and JSON formats for easy processing
6. Document each custom module's purpose and business function

**Output:**
- `migration/inventory/generate_module_list.py`
- `migration/inventory/odoo15_modules.csv`
- `migration/inventory/odoo15_modules.json`
- `migration/inventory/custom_modules_overview.md`

**Validation:**
- [ ] 67 core modules identified
- [ ] 20 custom modules identified
- [ ] All dependencies documented
- [ ] Module categories assigned

---

## Task 2: Backup Infrastructure ✅ PENDING

**Goal:** Create automated backup scripts for all critical data

**Steps:**
1. Create `migration/backup/` directory
2. Create database backup script (pg_dump)
3. Create filestore backup script (rsync/tar)
4. Create custom modules backup script
5. Create restoration scripts
6. Test backup and restore cycle
7. Document backup procedures

**Output:**
- `migration/backup/backup_database.sh`
- `migration/backup/backup_filestore.sh`
- `migration/backup/backup_custom_modules.sh`
- `migration/backup/restore_all.sh`
- `migration/backup/README.md`

**Validation:**
- [ ] Database backup created successfully
- [ ] Filestore backup created successfully
- [ ] Custom modules backed up
- [ ] Restore procedure tested and verified
- [ ] Backup size and location documented

---

## Task 3: Odoo 18 Environment Setup ✅ PENDING

**Goal:** Set up complete Odoo 18 environment ready for migration

**Steps:**
1. Create `migration/odoo18/` directory
2. Create Dockerfile for Odoo 18 with Python 3.11+
3. Create docker-compose.yml with PostgreSQL 13+
4. Create odoo18.conf configuration file
5. Create requirements.txt with Odoo 18 dependencies
6. Clone official Odoo 18.0 repository
7. Test Odoo 18 startup with `./odoo-bin --version`
8. Verify all system dependencies installed

**Output:**
- `migration/odoo18/Dockerfile`
- `migration/odoo18/docker-compose.yml`
- `migration/odoo18/odoo18.conf`
- `migration/odoo18/requirements.txt`
- `migration/odoo18/README.md`

**Validation:**
- [ ] Python 3.11+ environment active
- [ ] PostgreSQL 13+ accessible
- [ ] Odoo 18 starts without errors
- [ ] `./odoo-bin --version` shows "Odoo Server 18.0"
- [ ] wkhtmltopdf installed and working
- [ ] All Python dependencies installed

---

## Task 4: OpenUpgrade Framework Setup ✅ PENDING

**Goal:** Configure OpenUpgrade for Odoo 15→18 migration

**Steps:**
1. Create `migration/openupgrade/` directory
2. Clone OCA OpenUpgrade repository (18.0 branch)
3. Configure migration path: 15.0 → 16.0 → 17.0 → 18.0
4. Create custom migration scripts directory structure
5. Document OpenUpgrade execution procedure
6. Test OpenUpgrade with sample database

**Output:**
- `migration/openupgrade/README.md`
- `migration/openupgrade/custom_scripts/` (for custom module migrations)
- `migration/openupgrade/run_migration.sh`
- `migration/openupgrade/migration_config.yaml`

**Validation:**
- [ ] OpenUpgrade 18.0 cloned successfully
- [ ] Migration path configured (15→16→17→18)
- [ ] Custom scripts directory ready
- [ ] Migration procedure documented
- [ ] Test migration on empty database succeeds

---

## Task 5: Test Database Infrastructure ✅ PENDING

**Goal:** Create test database environment for safe migration testing

**Steps:**
1. Create PostgreSQL test database
2. Configure database users and permissions
3. Create database initialization scripts
4. Create database cleanup/reset scripts
5. Document database naming conventions
6. Set up connection pooling if needed

**Output:**
- `migration/database/create_test_db.sh`
- `migration/database/reset_test_db.sh`
- `migration/database/README.md`

**Validation:**
- [ ] Test database created: `odoo18_test`
- [ ] Database user configured with proper permissions
- [ ] Database accessible from Odoo 18
- [ ] Reset script works correctly
- [ ] Connection pooling configured

---

## Task 6: Documentation & Validation ✅ PENDING

**Goal:** Complete documentation and final validation checklist

**Steps:**
1. Create main migration README
2. Document environment setup procedures
3. Create Phase 1 validation checklist
4. Document rollback procedures
5. Create architecture diagram
6. Document troubleshooting guide
7. Run full Phase 1 validation

**Output:**
- `migration/README.md` (main migration guide)
- `migration/ARCHITECTURE.md` (system diagram)
- `migration/TROUBLESHOOTING.md`
- `openspec/changes/phase-1-odoo-18-environment-setup/VALIDATION.md`

**Validation:**
- [ ] All documentation complete
- [ ] Phase 1 checklist 100% complete
- [ ] Environment diagram created
- [ ] Rollback procedures tested
- [ ] Troubleshooting guide covers common issues

---

## Task 7: Git Commit & Push ✅ PENDING

**Goal:** Commit all Phase 1 work to branch

**Steps:**
1. Review all changes
2. Update .gitignore for migration artifacts
3. Stage all new files
4. Create comprehensive commit message
5. Push to branch: `claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM`

**Validation:**
- [ ] All files committed
- [ ] .gitignore updated
- [ ] Push successful
- [ ] Branch ready for Phase 2

---

## Overall Phase 1 Success Criteria

- [ ] Complete module inventory (67 core + 20 custom documented)
- [ ] All backups created and verified
- [ ] Odoo 18 environment running successfully
- [ ] OpenUpgrade framework configured
- [ ] Test database infrastructure ready
- [ ] All documentation complete
- [ ] No production impact
- [ ] All changes committed and pushed
