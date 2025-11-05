# Custom Module Migration

## Purpose

Migrate all 79 custom modules to Odoo 18 compatibility by updating manifests, modernizing Python code, fixing XML views, updating JavaScript, and validating security and business logic. This phase ensures custom business logic functions correctly on Odoo 18 while eliminating technical debt from deprecated APIs and patterns.

## Scope

**Included:**
- All 79 custom modules (~660 models)
- Manifest updates (version, dependencies)
- Python code modernization (decorators, imports, ORM patterns)
- XML view fixes (xpaths, inheritance, attributes)
- JavaScript/Frontend updates (OWL 2, ES6)
- Security (access rights, record rules)
- Business logic validation
- Custom reports and dashboards
- Cron jobs and automation
- Module documentation

**Excluded:**
- Core Odoo modules (validated in Phase 2)
- Database migration (covered in Phase 4)
- Production deployment (covered in Phase 6)

---

## Requirements

### Requirement: Manifest Update

Each custom module's `__manifest__.py` SHALL be updated for Odoo 18 compatibility.

#### Scenario: Version updated
- **WHEN** updating manifest version field
- **THEN** version is set to "18.0.x.x" format

#### Scenario: Dependencies reviewed
- **WHEN** reviewing depends field
- **THEN** all module dependencies are validated for Odoo 18 compatibility and updated as needed

#### Scenario: Metadata corrected
- **WHEN** reviewing manifest metadata
- **THEN** `application`, `auto_install`, `installable`, and other flags are set correctly

#### Scenario: Manifest loads without warnings
- **WHEN** loading module with updated manifest
- **THEN** Odoo reads manifest without warnings or deprecation notices

---

### Requirement: Python Code Modernization

All Python model files SHALL be updated to use Odoo 18 patterns and APIs.

#### Scenario: Deprecated decorators replaced
- **WHEN** reviewing model methods
- **THEN** the following replacements are made:
  - `@api.one` replaced with appropriate `@api.depends` or removed
  - `@api.multi` removed (default behavior in modern Odoo)
  - `@api.returns` updated to new signatures

#### Scenario: Import paths updated
- **WHEN** reviewing import statements
- **THEN** imports follow Odoo 18 structure:
  - `from odoo import api, fields, models, _`
  - Correct paths for exceptions, tools, and utilities

#### Scenario: ORM patterns modernized
- **WHEN** reviewing ORM method calls
- **THEN** patterns match Odoo 18 conventions:
  - Recordset operations (no loops where not needed)
  - Proper `self.env['model.name']` usage
  - Modern search/read patterns

#### Scenario: Compute methods updated
- **WHEN** reviewing compute methods
- **THEN** methods use correct decorator patterns:
  - `@api.depends()` with proper dependencies
  - Correct handling of empty recordsets
  - Store and compute logic separated appropriately

#### Scenario: Onchange methods updated
- **WHEN** reviewing onchange methods
- **THEN** methods follow Odoo 18 patterns:
  - Proper `@api.onchange()` decorator usage
  - Return values structured correctly
  - Warning and domain logic properly implemented

---

### Requirement: XML View Updates

All XML view files SHALL render correctly in Odoo 18.

#### Scenario: XPath expressions fixed
- **WHEN** reviewing inherited views
- **THEN** xpath expressions locate target elements correctly and use valid syntax

#### Scenario: View inheritance updated
- **WHEN** reviewing view inheritance
- **THEN** deprecated inheritance patterns are replaced with current syntax

#### Scenario: Field attributes updated
- **WHEN** reviewing field definitions
- **THEN** attributes match Odoo 18 schema:
  - `options` attribute uses correct JSON format
  - Widget names are valid for Odoo 18
  - Deprecated attributes removed or replaced

#### Scenario: Views render correctly
- **WHEN** opening views in Odoo 18
- **THEN** all menus, tree views, kanban views, and form views render without errors

#### Scenario: No XML parse errors
- **WHEN** loading module
- **THEN** no XMLParseError or ViewValidationError appears in logs

---

### Requirement: JavaScript and Frontend Updates

All custom JavaScript SHALL be compatible with Odoo 18 frontend framework.

#### Scenario: OWL 2 syntax
- **WHEN** reviewing JavaScript components
- **THEN** components use OWL 2 syntax (if using OWL):
  - Proper component structure
  - Correct lifecycle hooks
  - Template syntax updated

#### Scenario: ES6 patterns
- **WHEN** reviewing JavaScript code
- **THEN** code uses modern ES6 syntax:
  - Arrow functions, const/let, template literals
  - Classes instead of prototypes
  - Modern module imports/exports

#### Scenario: Event bindings updated
- **WHEN** reviewing event handling
- **THEN** event binding patterns match Odoo 18 conventions

#### Scenario: Web client compatibility
- **WHEN** testing in browser
- **THEN** custom JavaScript executes without console errors and functionality works as expected

#### Scenario: Website/Portal templates
- **WHEN** custom website or portal templates exist
- **THEN** templates render correctly with Odoo 18 frontend assets

---

### Requirement: Module Installation

Each custom module SHALL install and upgrade successfully in Odoo 18.

#### Scenario: Install command succeeds
- **WHEN** running `./odoo-bin -d <db> -i <module_name>`
- **THEN** module installs without errors

#### Scenario: Dependencies resolved
- **WHEN** installing module with dependencies
- **THEN** all dependencies install first and are available

#### Scenario: Field migrations handled
- **WHEN** module defines new or changed fields
- **THEN** database schema updates correctly without field mismatch errors

#### Scenario: No missing field errors
- **WHEN** module loads
- **THEN** no "Field 'x' does not exist" errors appear in logs

---

### Requirement: Access Rights and Security

Security definitions SHALL function correctly in Odoo 18.

#### Scenario: Access rights defined
- **WHEN** reviewing security/ir.model.access.csv
- **THEN** all models have appropriate access rights defined for relevant groups

#### Scenario: Record rules applied
- **WHEN** record-level security rules exist
- **THEN** rules apply correctly and users see only permitted records

#### Scenario: Group assignments
- **WHEN** groups defined in XML
- **THEN** group definitions load and users can be assigned correctly

#### Scenario: No access errors
- **WHEN** users interact with module
- **THEN** no AccessError or RecordRuleError occurs for valid operations

---

### Requirement: Business Logic Validation

All custom business logic SHALL function correctly with Odoo 18.

#### Scenario: Create and edit records
- **WHEN** creating and editing records in custom modules
- **THEN** records save successfully and data persists correctly

#### Scenario: Computed fields calculate
- **WHEN** viewing records with computed fields
- **THEN** computed values are correct based on dependencies

#### Scenario: Constraints enforced
- **WHEN** violating SQL or Python constraints
- **THEN** appropriate validation errors prevent invalid data

#### Scenario: Automation triggers
- **WHEN** automated actions are configured
- **THEN** actions trigger on correct conditions and execute successfully

#### Scenario: Notifications sent
- **WHEN** notification logic exists
- **THEN** emails, messages, or activities are created as expected

#### Scenario: Button actions work
- **WHEN** custom buttons are clicked
- **THEN** server actions execute successfully and produce expected results

#### Scenario: Workflows and approvals
- **WHEN** custom approval workflows exist
- **THEN** state transitions and approval logic work correctly

---

### Requirement: Custom Reports and Dashboards

All custom reports and dashboards SHALL generate correctly.

#### Scenario: QWeb PDF reports
- **WHEN** generating custom PDF reports
- **THEN** reports render using correct templates without errors

#### Scenario: Excel reports
- **WHEN** generating custom Excel reports (XLSX)
- **THEN** data exports correctly with proper formatting

#### Scenario: Field mappings
- **WHEN** reports reference model fields
- **THEN** all field references are valid (no missing or renamed fields)

#### Scenario: Report templates render
- **WHEN** viewing report output
- **THEN** templates display correct data, formatting, and layout

#### Scenario: Dashboards functional
- **WHEN** custom dashboards or visualizations exist
- **THEN** data displays accurately and interactions work correctly

---

### Requirement: Cron Jobs and Automation

Custom scheduled actions SHALL execute successfully.

#### Scenario: Cron jobs listed
- **WHEN** checking Settings > Technical > Scheduled Actions
- **THEN** custom cron jobs appear with correct frequency and configuration

#### Scenario: Function paths valid
- **WHEN** cron job executes
- **THEN** function path resolves correctly to model method

#### Scenario: Cron execution succeeds
- **WHEN** cron job runs (manually or scheduled)
- **THEN** job completes successfully with expected results and no exceptions

#### Scenario: Scheduled task results
- **WHEN** reviewing cron job outcomes
- **THEN** expected background processing completes (data updates, report generation, notifications)

---

### Requirement: Module Documentation

Each custom module SHALL have documentation of migration status and testing.

#### Scenario: Module checklist
- **WHEN** migration work on module is complete
- **THEN** checklist includes:
  - Install status (success/failure)
  - Testing notes (what was tested, results)
  - Errors encountered and fixes applied
  - Known issues or limitations

#### Scenario: Migration report
- **WHEN** all modules are migrated
- **THEN** migration report includes:
  - Before/after comparison for each module
  - List of all code changes made
  - Validation results
  - Sign-off status

---

## Success Criteria

Custom module migration is complete when:
-  All 79 custom modules have manifests updated to "18.0.x.x"
-  All Python code uses Odoo 18 patterns (no deprecated decorators)
-  All XML views render without errors
-  All JavaScript uses modern syntax and executes without errors
-  All modules install successfully via `-i` command
-  Access rights and security rules function correctly
-  Business logic tested with sample records across all modules
-  Custom reports (PDF/Excel) generate without errors
-  Custom cron jobs execute successfully
-  Module-wise documentation complete with test results
-  No critical errors in logs during module operations
-  All custom modules ready for database migration phase
