# Core Module Validation

## Purpose

Validate that all 67 Odoo base modules function correctly on Odoo 18 before proceeding to custom module migration. This phase ensures the foundation Odoo platform is stable and all standard business processes work as expected on the new version.

## Scope

**Included:**
- All 67 core Odoo modules (Sales, Inventory, Purchase, Accounting, HR, Manufacturing, etc.)
- Menu navigation and form rendering
- End-to-end workflow validation
- Report generation (PDF, Excel)
- Scheduled actions (cron jobs)
- Sequences and data integrity
- Access rights and permissions

**Excluded:**
- Custom modules (covered in Phase 3)
- Third-party addons (assessed case-by-case)
- Database migration (covered in Phase 4)
- Production data validation (covered in Phase 6)

---

## Requirements

### Requirement: Menu Navigation

All core module menus SHALL appear and function correctly in Odoo 18.

#### Scenario: All menus visible
- **WHEN** user logs into Odoo 18 system
- **THEN** all installed core module menus are visible in the navigation bar

#### Scenario: Menu items open correctly
- **WHEN** user clicks any menu item
- **THEN** corresponding view opens without errors (no crashes, no "View not found" errors)

#### Scenario: Submenu navigation
- **WHEN** navigating through nested submenus
- **THEN** all submenu items are accessible and lead to correct views

---

### Requirement: Form Loading and Data Entry

Core module forms SHALL load, accept data entry, and save records successfully.

#### Scenario: Form rendering
- **WHEN** opening a form view (create or edit)
- **THEN** form renders completely with all fields visible and properly formatted

#### Scenario: Create new records
- **WHEN** creating new records in core modules (Sales Order, Purchase Order, Product, Partner, etc.)
- **THEN** all required and optional fields accept input and validation rules apply correctly

#### Scenario: Save records
- **WHEN** saving a record
- **THEN** record saves successfully without errors and can be retrieved

#### Scenario: Edit existing records
- **WHEN** editing an existing record
- **THEN** changes are saved and reflected in the database

---

### Requirement: End-to-End Workflow Validation

Key business workflows SHALL complete successfully from start to finish.

#### Scenario: Sales to Invoice workflow
- **WHEN** executing Sales ’ Delivery ’ Invoice ’ Payment workflow
- **THEN** each step completes without errors:
  - Sales Order created and confirmed
  - Delivery Order generated and validated
  - Invoice created from delivery
  - Payment registered and reconciled

#### Scenario: Purchase workflow
- **WHEN** executing Purchase ’ Receipt ’ Bill workflow
- **THEN** each step completes:
  - Purchase Order created and confirmed
  - Receipt processed and stock updated
  - Vendor Bill created and posted

#### Scenario: Inventory workflow
- **WHEN** processing inventory movements
- **THEN** stock levels update correctly, transfers complete, and inventory adjustments are recorded

#### Scenario: Manufacturing workflow (if applicable)
- **WHEN** creating and processing Manufacturing Orders
- **THEN** BOM consumption, production, and finished goods receipt complete successfully

---

### Requirement: Report Generation

All core module reports SHALL generate correctly in required formats.

#### Scenario: PDF reports
- **WHEN** generating PDF reports (Quotations, Invoices, Delivery Orders, etc.)
- **THEN** reports generate using wkhtmltopdf without errors and display correct data

#### Scenario: Excel reports
- **WHEN** generating Excel exports
- **THEN** data exports correctly to Excel format with proper formatting

#### Scenario: Report data accuracy
- **WHEN** reviewing generated reports
- **THEN** data matches source records (amounts, quantities, dates, names)

#### Scenario: Report templates
- **WHEN** reports are generated
- **THEN** standard Odoo templates render correctly without missing sections or formatting issues

---

### Requirement: Scheduled Actions (Cron Jobs)

Default scheduled actions SHALL execute successfully without errors.

#### Scenario: Cron jobs active
- **WHEN** checking Settings > Technical > Scheduled Actions
- **THEN** all default cron jobs are active and show next scheduled run time

#### Scenario: Cron execution
- **WHEN** cron jobs execute (either manually triggered or by scheduler)
- **THEN** jobs complete successfully with "Success" status and no exceptions in logs

#### Scenario: Scheduled task functions
- **WHEN** reviewing cron job results
- **THEN** expected actions are performed:
  - Email reminders sent
  - Recurring records created
  - Background processes completed
  - Scheduled reports generated

---

### Requirement: Data Integrity and Access Rights

Data integrity and access controls SHALL function correctly across core modules.

#### Scenario: Data visible to correct users
- **WHEN** users with different roles log in
- **THEN** each user sees only data they have permission to access

#### Scenario: Edit permissions
- **WHEN** users attempt to modify records
- **THEN** only users with edit rights can save changes; others see read-only views

#### Scenario: Record rules
- **WHEN** record-level security rules apply
- **THEN** users in specific groups see only records matching their rules (e.g., salespeople see only their own leads)

#### Scenario: Multi-company rules
- **WHEN** multi-company setup is active
- **THEN** users see only records for companies they have access to

---

### Requirement: Sequences

All system sequences SHALL continue correctly from their last number.

#### Scenario: Sales Order sequences
- **WHEN** creating new Sales Orders
- **THEN** sequence continues from last Odoo 15 number without gaps or duplicates

#### Scenario: Invoice sequences
- **WHEN** generating new invoices
- **THEN** invoice numbering follows regulatory requirements and continues properly

#### Scenario: Other document sequences
- **WHEN** creating Purchase Orders, Deliveries, Receipts, etc.
- **THEN** all sequences continue correctly and maintain expected format

#### Scenario: Sequence reset validation
- **WHEN** sequence reset is required (e.g., annual reset for invoices)
- **THEN** reset logic functions correctly per configuration

---

### Requirement: Models and API Compatibility

Core models and APIs SHALL function correctly on Odoo 18.

#### Scenario: Model methods
- **WHEN** calling standard model methods (create, write, search, read)
- **THEN** methods execute without errors and return expected results

#### Scenario: Compute fields
- **WHEN** viewing records with computed fields
- **THEN** computed values calculate correctly based on dependent fields

#### Scenario: Onchange methods
- **WHEN** changing field values in forms
- **THEN** onchange methods trigger and update dependent fields as expected

#### Scenario: Constraints
- **WHEN** attempting to violate field or model constraints
- **THEN** appropriate validation errors are raised and prevent invalid data

---

## Success Criteria

Core module validation is complete when:
-  All 67 core module menus open without errors
-  Forms load, save, and validate correctly for all core modules
-  Key workflows tested and verified (Sales, Purchase, Inventory, Accounting)
-  All PDF and Excel reports generate correctly
-  All default cron jobs execute successfully
-  Sequences continue from last numbers without gaps
-  Access rights and record rules function correctly
-  Models, APIs, compute fields, and constraints work as expected
-  No critical errors in Odoo logs during validation testing
-  Core validation report documenting all tests and results is complete
