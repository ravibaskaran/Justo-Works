# Database Migration

## Purpose

Execute the migration of the Odoo 15 database schema and data to Odoo 18 format using the OpenUpgrade framework. This phase transforms the database structure, migrates all records, applies custom mapping scripts for renamed or deleted fields, and validates data integrity after migration.

## Scope

**Included:**
- Database restore from Odoo 15 backup
- Filestore copying and validation
- OpenUpgrade configuration and execution
- Schema migration (tables, columns, constraints)
- Data migration (all records across ~660 models)
- Custom mapping scripts for field renames/deletions
- Post-migration data validation
- Migration log review and error resolution

**Excluded:**
- Module code changes (completed in Phases 2-3)
- Business logic testing (covered in Phase 5-6)
- Production deployment (covered in Phase 6)

---

## Requirements

### Requirement: Database Restore

Odoo 15 production database SHALL be restored to test instance for migration.

#### Scenario: Backup restoration
- **WHEN** restoring Odoo 15 database backup
- **THEN** full database is restored to test PostgreSQL instance with all tables, data, and schema intact

#### Scenario: Database connectivity
- **WHEN** database restore is complete
- **THEN** connection can be established using configured credentials

#### Scenario: Data completeness
- **WHEN** validating restored database
- **THEN** record counts match source database for key tables (partners, products, orders, invoices)

#### Scenario: Database user permissions
- **WHEN** testing database access
- **THEN** Odoo database user has necessary permissions (CREATEDB, CREATEROLE) for migration operations

---

### Requirement: Filestore Migration

Odoo 15 filestore (attachments) SHALL be copied to Odoo 18 directory structure.

#### Scenario: Filestore copy
- **WHEN** copying filestore directory
- **THEN** all files and subdirectories are copied from Odoo 15 filestore to new Odoo 18 filestore location

#### Scenario: File integrity
- **WHEN** validating copied files
- **THEN** file count and total size match source filestore

#### Scenario: Directory structure
- **WHEN** reviewing filestore structure
- **THEN** directory hierarchy is preserved with correct permissions

#### Scenario: Attachment accessibility
- **WHEN** Odoo 18 accesses attachments
- **THEN** files are readable and can be retrieved without errors

---

### Requirement: OpenUpgrade Configuration

OpenUpgrade SHALL be configured correctly for the migration.

#### Scenario: Configuration file
- **WHEN** creating OpenUpgrade configuration (odoo18_migrate.conf)
- **THEN** configuration includes:
  - Database connection details (host, port, username, password, database name)
  - Odoo 18 source code path
  - Addons paths (core and custom)
  - OpenUpgrade migration script paths

#### Scenario: Migration script availability
- **WHEN** validating OpenUpgrade setup
- **THEN** migration scripts for Odoo 1518 are present and accessible

#### Scenario: Configuration validation
- **WHEN** testing configuration
- **THEN** OpenUpgrade can read configuration and connect to database without errors

---

### Requirement: Migration Execution

OpenUpgrade migration SHALL execute and complete successfully.

#### Scenario: Migration command
- **WHEN** running migration command
  ```
  python3 migrate.py --config=odoo18_migrate.conf --database=<db_name>
  ```
- **THEN** migration process starts and runs through all migration steps

#### Scenario: Migration progress
- **WHEN** migration is executing
- **THEN** progress is visible in console output or logs showing:
  - Modules being migrated
  - Tables being updated
  - Records being transformed

#### Scenario: Migration completion
- **WHEN** migration finishes
- **THEN** process exits with success status (exit code 0) and displays completion message

#### Scenario: No unhandled errors
- **WHEN** reviewing migration execution
- **THEN** no critical or unhandled errors prevent migration completion

---

### Requirement: Custom Mapping Scripts

Custom mapping scripts SHALL be applied for renamed or deleted fields.

#### Scenario: Field rename mappings
- **WHEN** fields have been renamed between Odoo 15 and 18
- **THEN** custom mapping scripts map old field names to new field names and data is transferred

#### Scenario: Deleted field handling
- **WHEN** fields have been removed in Odoo 18
- **THEN** deleted fields are documented and data is archived or migrated to alternative fields

#### Scenario: Model rename mappings
- **WHEN** models have been renamed
- **THEN** model mapping scripts ensure data moves to correct new model names

#### Scenario: Custom migration scripts
- **WHEN** business-specific data transformations are needed
- **THEN** custom scripts execute during migration and transform data correctly

---

### Requirement: Migration Log Review

Migration logs SHALL be reviewed and all issues SHALL be documented.

#### Scenario: Log file generation
- **WHEN** migration executes
- **THEN** detailed log file is generated with timestamps and operation details

#### Scenario: Warning review
- **WHEN** reviewing logs
- **THEN** all warnings are documented and assessed for impact (critical vs. informational)

#### Scenario: Error identification
- **WHEN** errors occur during migration
- **THEN** errors are logged with:
  - Error type and message
  - Module or model affected
  - Stack trace (if applicable)
  - Resolution steps

#### Scenario: Critical issue resolution
- **WHEN** critical issues are identified
- **THEN** issues are resolved and migration is re-run until successful

---

### Requirement: Post-Migration Data Validation

All migrated data SHALL be validated for completeness and integrity.

#### Scenario: Record count validation
- **WHEN** comparing Odoo 15 and Odoo 18 databases
- **THEN** record counts match for all core tables (partners, products, orders, invoices, etc.)

#### Scenario: Key data spot checks
- **WHEN** reviewing migrated records
- **THEN** sample records from each major module contain correct data (names, amounts, dates, status)

#### Scenario: Foreign key integrity
- **WHEN** checking relational data
- **THEN** all foreign key relationships are intact (Many2One, One2Many fields reference valid records)

#### Scenario: Computed field validation
- **WHEN** checking computed fields
- **THEN** computed values recalculate correctly after migration

---

### Requirement: Post-Migration Cleanup

Post-migration cleanup tasks SHALL be executed.

#### Scenario: Obsolete data cleanup
- **WHEN** running post-migration scripts
- **THEN** obsolete or deprecated data is cleaned up per cleanup scripts

#### Scenario: Orphaned records
- **WHEN** checking for orphaned records
- **THEN** orphaned records are identified and handled (deleted or linked to appropriate parents)

#### Scenario: Database optimization
- **WHEN** migration is complete
- **THEN** database vacuum and analyze operations are run to optimize performance

#### Scenario: Index rebuilding
- **WHEN** validating database performance
- **THEN** all indexes are present and functional

---

### Requirement: Rollback Capability

Rollback capability SHALL be maintained throughout database migration.

#### Scenario: Pre-migration backup
- **WHEN** before starting migration
- **THEN** fresh backup of Odoo 15 database and filestore is created

#### Scenario: Rollback procedure documented
- **WHEN** migration fails or issues are found
- **THEN** documented rollback procedure allows restoration to Odoo 15 state

#### Scenario: Test environment isolation
- **WHEN** migration is executed
- **THEN** production Odoo 15 system remains untouched and operational

---

## Success Criteria

Database migration is complete when:
-  Odoo 15 database backup restored successfully to test instance
-  Filestore copied with all files intact and accessible
-  OpenUpgrade configured correctly with all paths and credentials
-  Migration executes to completion without unhandled errors
-  Custom mapping scripts applied for renamed/deleted fields
-  Migration logs reviewed and all critical issues resolved
-  Record counts match between Odoo 15 and Odoo 18 for key tables
-  Foreign key relationships intact across all models
-  Post-migration cleanup scripts executed successfully
-  Database optimized (vacuum, analyze) and indexes functional
-  Rollback capability tested and documented
-  Migrated database ready for validation testing (Phases 5-6)
