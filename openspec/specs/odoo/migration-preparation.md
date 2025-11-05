# Migration Preparation

## Purpose

Establish a safe foundation for the Odoo 15 ’ Odoo 18 migration by setting up the development environment, creating comprehensive backups, inventorying all modules, and preparing the migration tooling. This phase ensures rollback capability and provides a clean testing environment before any migration work begins.

## Scope

**Included:**
- Module inventory and classification
- Complete backup of production data (database, filestore, custom modules)
- Odoo 18 environment setup on local/test infrastructure
- OpenUpgrade framework installation and configuration
- Test database creation

**Excluded:**
- Any modifications to production Odoo 15 system
- Code changes to modules
- Data migration execution (covered in Phase 4)

---

## Requirements

### Requirement: Module Inventory and Classification

All installed Odoo modules SHALL be inventoried and classified before migration begins.

#### Scenario: Export module list
- **WHEN** exporting from `ir_module_module` table
- **THEN** complete list of all installed modules is captured with names, versions, and states

#### Scenario: Classify modules
- **WHEN** reviewing module inventory
- **THEN** each module is categorized as:
  - **Core** (Odoo S.A. base modules)
  - **Third-Party** (OCA or other external addons)
  - **Custom** (business-specific modules)

#### Scenario: Module inventory output
- **WHEN** classification is complete
- **THEN** inventory is exported in structured format (Excel/CSV) with columns: module name, category, version, dependencies

---

### Requirement: Complete Backup Strategy

Complete backups of all production data SHALL be created and verified before migration work begins.

#### Scenario: Database backup
- **WHEN** creating database backup
- **THEN** full PostgreSQL dump is created using `pg_dump` with all data and schema intact

#### Scenario: Filestore backup
- **WHEN** backing up attachments
- **THEN** entire Odoo 15 filestore directory is copied with all files and directory structure preserved

#### Scenario: Custom module backup
- **WHEN** backing up custom code
- **THEN** all custom module source code is copied from addons directories with complete file history

#### Scenario: Backup verification
- **WHEN** backups are complete
- **THEN** backup files are verified for integrity and stored in secure location with clear labels (date, environment, version)

---

### Requirement: Odoo 18 Environment Setup

A complete Odoo 18 development environment SHALL be configured on local/test infrastructure.

#### Scenario: Runtime dependencies installed
- **WHEN** setting up environment
- **THEN** the following are installed and verified:
  - Python 3.11 or higher
  - PostgreSQL 13, 14, or 15
  - wkhtmltopdf (for PDF report generation)
  - Required system dependencies (python3-dev, build-essential, libxml2-dev, libxslt1-dev, libldap2-dev, libsasl2-dev, etc.)

#### Scenario: Odoo 18 source code
- **WHEN** cloning Odoo source
- **THEN** official Odoo 18 source code is cloned from Odoo repository and Python dependencies are installed via `requirements.txt`

#### Scenario: Environment validation
- **WHEN** environment setup is complete
- **THEN** Odoo 18 starts successfully in development mode with no missing dependencies

---

### Requirement: OpenUpgrade Framework Installation

OpenUpgrade migration framework SHALL be installed and ready for database migration.

#### Scenario: Clone OpenUpgrade
- **WHEN** installing OpenUpgrade
- **THEN** OCA's OpenUpgrade repository is cloned with the 18.0 branch checked out

#### Scenario: OpenUpgrade dependencies
- **WHEN** preparing OpenUpgrade
- **THEN** all required Python packages for OpenUpgrade are installed and migration scripts are accessible

#### Scenario: Framework verification
- **WHEN** validating OpenUpgrade installation
- **THEN** migration framework executes help/info commands successfully without errors

---

### Requirement: Test Database Creation

An empty PostgreSQL test database SHALL be created for migration testing.

#### Scenario: Create test database
- **WHEN** creating test database
- **THEN** new PostgreSQL database is created with appropriate name (e.g., `odoo18_migration_test`)

#### Scenario: Database user and permissions
- **WHEN** configuring database access
- **THEN** PostgreSQL user has full permissions (CREATEDB, CREATEROLE) for migration operations

#### Scenario: Database validation
- **WHEN** test database is ready
- **THEN** connection can be established and database is empty with no existing tables

---

### Requirement: Rollback Capability

Rollback capability SHALL be maintained throughout the preparation phase.

#### Scenario: Production system unchanged
- **WHEN** preparation phase is complete
- **THEN** production Odoo 15 system remains untouched and fully operational

#### Scenario: Backup restore test
- **WHEN** testing rollback capability
- **THEN** database backup can be successfully restored to a test instance and system is functional

#### Scenario: Backup documentation
- **WHEN** backups are complete
- **THEN** documentation includes:
  - Backup locations
  - Backup timestamps
  - Restore procedures
  - Verification steps

---

## Success Criteria

Preparation phase is complete when:
-  Module inventory exported with 67 core + 79 custom modules classified
-  Database, filestore, and custom module backups created and verified
-  Odoo 18 environment installed with Python 3.11+, PostgreSQL, and dependencies
-  OpenUpgrade framework cloned and functional
-  Empty test database created with proper permissions
-  All documentation updated with backup locations and restore procedures
-  Production system remains unchanged and operational
