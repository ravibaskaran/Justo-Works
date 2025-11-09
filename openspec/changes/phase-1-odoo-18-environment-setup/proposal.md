# Change: Phase 1 - Odoo 18 Environment Setup & Preparation

## Why

Before migrating Odoo 15 to Odoo 18, we need a complete, tested environment where migration can be safely executed and validated. This phase establishes the foundation for all subsequent migration work by:

1. **Inventory Current State** - Document all 67 core modules and 20 custom modules to ensure nothing is missed during migration
2. **Protect Production Data** - Create comprehensive backups of database, filestore, and custom code before any changes
3. **Establish Target Environment** - Set up Odoo 18 with correct Python 3.11+, PostgreSQL, and dependencies
4. **Prepare Migration Tools** - Clone and configure OpenUpgrade framework for automated migration
5. **Enable Safe Testing** - Create isolated test environments to validate migration without production risk

## What Changes

### 1. Module Inventory & Documentation
- Generate complete module list with versions, dependencies, and categorization
- Identify Core Odoo modules (67 modules)
- Identify Custom modules (20 modules in `addons_custom/`)
- Document third-party dependencies
- Create module compatibility matrix for Odoo 18
- Export installed module list from current Odoo 15

### 2. Backup Infrastructure
- Create automated backup scripts for:
  - PostgreSQL database dump (pg_dump with custom format)
  - Filestore directory (all attachments, images, documents)
  - Custom module source code (addons_custom/)
  - Configuration files (odoo.conf, requirements.txt)
- Document backup restoration procedures
- Verify backup integrity before proceeding

### 3. Odoo 18 Environment Setup
- **Python Environment**: Python 3.11+ with venv
- **Database**: PostgreSQL 13+ configured for Odoo 18
- **System Dependencies**: wkhtmltopdf, fonts, libraries per Odoo 18 requirements
- **Odoo 18 Installation**: Clone Odoo 18.0 branch from official repository
- **Configuration**: Create odoo18.conf with appropriate settings
- **Docker Configuration** (optional but recommended): docker-compose.yml for reproducible environments

### 4. OpenUpgrade Framework Setup
- Clone OCA OpenUpgrade repository (18.0 branch)
- Configure migration scripts for Odoo 15→18 path
- Set up custom migration scripts directory for custom modules
- Document OpenUpgrade execution procedure
- Test OpenUpgrade with empty database

### 5. Test Database Infrastructure
- Create empty test database in PostgreSQL
- Configure database roles and permissions
- Set up database restore scripts for testing migration iterations
- Document database naming conventions (prod, test, dev)

### 6. Documentation & Validation
- Document environment setup procedures
- Create Phase 1 validation checklist
- Document rollback procedures
- Create migration environment diagram
- Document all Python dependencies and versions

## Files Created/Modified

### New Files
```
openspec/changes/phase-1-odoo-18-environment-setup/
├── proposal.md (this file)
├── tasks.md (task breakdown)
└── specs/
    ├── module-inventory.md
    └── environment-setup.md

migration/
├── README.md (migration guide)
├── backup/
│   ├── backup_database.sh
│   ├── backup_filestore.sh
│   └── restore_all.sh
├── inventory/
│   ├── generate_module_list.py
│   └── odoo15_modules.csv (generated)
├── odoo18/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── odoo18.conf
│   └── requirements.txt
└── openupgrade/
    └── README.md (OpenUpgrade setup guide)
```

### Modified Files
```
.gitignore (add migration/, odoo18/, backups/)
README.md (add migration section)
```

## Impact

- **Affected systems**: None yet (preparation only)
- **Production impact**: NONE (all work in isolated environments)
- **Risk level**: LOW (read-only inventory and environment setup)
- **Rollback capability**: Full (no changes to production)
- **Time estimate**: 2-4 hours

## Dependencies

- PostgreSQL 13+ installed and running
- Python 3.11+ available
- Docker (optional but recommended)
- Git access to Odoo and OpenUpgrade repositories
- Sufficient disk space for backups (estimate 3x current database size)

## Priority

**CRITICAL** - Must be completed BEFORE any migration work begins

## Implementation Branch

All work will be done on: `claude/odoo-18-environment-setup-011CUwiCv28Akz6ATWc3JqTM`

## Success Criteria

- [ ] Complete module inventory generated (67 core + 20 custom modules documented)
- [ ] All backups created and verified (database, filestore, custom code)
- [ ] Odoo 18 environment successfully starts with `./odoo-bin --version` showing 18.0
- [ ] PostgreSQL test database created and accessible
- [ ] OpenUpgrade framework cloned and configured
- [ ] Docker environment (if used) successfully launches Odoo 18
- [ ] All documentation complete and procedures validated
- [ ] Environment validation checklist 100% complete
- [ ] No production systems modified or affected

## Next Phase

After Phase 1 completion, proceed to **Phase 2: Core Module Validation** where all 67 Odoo base modules will be validated on Odoo 18.
