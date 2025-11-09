# Project Context

## Migration Overview

This is a grayfield Odoo migration project: migrating an existing production Odoo 15 instance with 67 core modules and 20 custom modules (~660 models total) to Odoo 18. The migration preserves all critical business flows while modernizing the technical foundation and eliminating technical debt accumulated from deprecated APIs and frameworks.

## Context

**Current State:** Odoo 15 production instance with:
- 67 core Odoo modules (Sales, Inventory, Purchase, Accounting, etc.)
- 20 custom modules built for business-specific requirements (Real Estate, Accounting, Dashboards, APIs)
- Approximately 660 models across all modules (200+ custom models)
- Production data including master data, transactions, and attachments

**Target State:** Odoo 18 with:
- All core modules validated and functional on Odoo 18
- All custom modules migrated and compatible with Odoo 18 conventions
- Complete data migration via OpenUpgrade
- Same business behavior plus approved improvements
- Clean technical foundation (Python 3.11+, modern APIs, no deprecated patterns)

## Goals

- Preserve all critical business flows during migration
- Validate core Odoo modules work correctly on version 18
- Migrate custom modules to Odoo 18 conventions (manifests, Python code, XML views, JS)
- Execute database migration using OpenUpgrade framework
- Clean up technical debt: deprecated decorators, old APIs, framework issues
- Validate security (access rights, roles), automation (cron jobs), and performance
- Ensure data integrity across all master and transactional records

## Constraints

- Must maintain rollback capability at each phase
- Regulatory and audit constraints for finance modules must be preserved
- All migrations tested in local/test environment before production
- No data loss during database migration
- User roles and permissions must remain consistent
- Business-critical workflows must remain functional throughout

## Tech Stack

- **Source:** Odoo 15
- **Target:** Odoo 18
- **Runtime:** Python 3.11+, PostgreSQL 13-15
- **Migration Tool:** OpenUpgrade (OCA's OpenUpgrade 18.0 branch)
- **Reporting:** wkhtmltopdf for PDF generation
- **Modules:** 67 core, 20 custom, ~660 models total (200+ custom models)

## Principles

- No code change without an OpenSpec change ID
- Specs must be green (openspec validate) before merging PRs
- Specs always win over code if they disagree; code must be brought back in line
- Migration follows the six-phase approach defined in migration specs
- **Single Branch Policy:** ALL AI coding work must be done on ONE designated branch (`claude/openspec-ai-branch-policy-011CUvg4v8NQhY1UST4u22fR`) independent of session - ensures single source of truth other than main

## Spec-Driven Rules

- Always read `openspec/project.md` before proposing major changes
- For any change, check `openspec/changes/<change-id>/proposal.md`, `tasks.md`, and `specs/*`
- Do NOT modify Odoo code (core or custom) without checking relevant specs first
- Read domain-specific specs under `openspec/specs/odoo/*.md` before making migration-related changes
- If requirements are unclear, update the spec or propose edits there instead of guessing in code

## Migration Phases

### Phase 1: Preparation
**Purpose:** Establish safe foundation for migration including environment setup, module inventory, and backups.

**Key Outputs:**
- Complete module inventory exported and categorized (Core/Third-Party/Custom)
- Full backups: database (pg_dump), filestore, and custom modules
- Odoo 18 environment configured (Python 3.11+, PostgreSQL, dependencies)
- OpenUpgrade framework cloned and ready
- Empty test database created in PostgreSQL

### Phase 2: Core Module Validation
**Purpose:** Validate that all 67 Odoo base modules function correctly on Odoo 18 before custom module migration.

**Key Outputs:**
- All core module menus appear and open correctly
- Forms load, save, and validate without errors
- Key workflows complete end-to-end (Sale → Delivery → Invoice → Payment)
- Reports generate correctly (PDF/Excel)
- Scheduled actions (cron jobs) execute successfully
- Sequences continue from last number
- Access rights and data integrity validated

### Phase 3: Custom Module Migration
**Purpose:** Adapt all 20 custom modules to Odoo 18 compatibility including code, views, and security.

**Key Outputs:**
- All manifests updated (version "18.0.x.x", dependencies corrected)
- Python code modernized (decorators, imports, ORM patterns)
- XML views fixed (xpaths, inheritance, attributes)
- JS/Frontend updated (OWL 2, ES6 syntax)
- All modules reinstall successfully without errors
- Access rights and security validated per module
- Business logic tested with sample records
- Custom reports and dashboards functional
- Cron jobs validated

### Phase 4: Database Migration (OpenUpgrade)
**Purpose:** Execute migration of Odoo 15 database schema and data to Odoo 18 format.

**Key Outputs:**
- Odoo 15 database backup restored to test instance
- Filestore copied to new Odoo 18 directory
- OpenUpgrade configured with correct paths and credentials
- Migration executed without unhandled errors
- Custom mapping scripts applied for renamed/deleted fields
- All migrated data validated across models
- Post-migration cleanup scripts executed
- Records, attachments, workflows verified consistent

### Phase 5: Automation, Security & Performance
**Purpose:** Validate system automation, security controls, and performance meet requirements.

**Key Outputs:**
- All scheduled jobs run successfully with correct frequency
- User roles grant appropriate permissions per group
- Integrations validated (API endpoints, webhooks, connectors)
- Performance benchmarks met (page load times, workflow speed)

### Phase 6: Post-Migration Validation & UAT
**Purpose:** Comprehensive validation and user acceptance testing before production deployment.

**Key Outputs:**
- Master data validated (Partners, Products, Stock)
- Transactional data compared to Odoo 15 baseline (Orders, Invoices)
- Attachments verified in filestore
- Relational integrity confirmed (Many2One, One2Many relationships)
- Computed fields and workflows tested
- UAT conducted with stakeholders
- Issues identified and resolved
- Production migration executed
- Client sign-off obtained
