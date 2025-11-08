# Odoo Architecture and Patterns

## Purpose

Document the core architecture patterns, MVC structure, ORM conventions, and framework patterns used across the Odoo 15 real estate management system. This specification serves as the technical foundation for understanding how custom modules integrate with Odoo's framework.

## Scope

**Included:**
- Odoo MVC architecture and module structure
- ORM patterns and recordset operations
- Model inheritance patterns (classical, extension, delegation)
- View architecture (Form, Tree, Kanban, Search, etc.)
- Controller patterns and HTTP routing
- Security model (access rights, record rules, groups)
- Workflow and automation patterns
- Data files and CSV imports
- Report generation (QWeb, wkhtmltopdf)

**Excluded:**
- Migration-specific patterns (see migration specs in openspec/specs/odoo/)
- API-specific authentication (see openspec/specs/authentication/)
- Business logic for specific modules

---

## Requirements

### Requirement: Module Structure

All Odoo custom modules SHALL follow the standard Odoo module directory structure.

#### Scenario: Module directory layout
- **WHEN** creating or reviewing a custom module
- **THEN** the following structure is present:
  ```
  module_name/
  ├── __init__.py
  ├── __manifest__.py
  ├── models/
  │   ├── __init__.py
  │   └── *.py
  ├── views/
  │   └── *.xml
  ├── controllers/
  │   ├── __init__.py
  │   └── *.py
  ├── security/
  │   ├── ir.model.access.csv
  │   └── security.xml
  ├── data/
  │   └── *.xml
  ├── static/
  │   └── description/
  │       └── icon.png
  └── README.md
  ```

#### Scenario: Manifest file validity
- **WHEN** loading a module
- **THEN** `__manifest__.py` contains required fields: name, version, depends, data, installable, application

#### Scenario: Python imports
- **WHEN** reviewing module initialization
- **THEN** all submodules (models, controllers) are imported in respective `__init__.py` files

---

### Requirement: Model Layer (ORM)

All Odoo models SHALL use the Odoo ORM API correctly following recordset patterns.

#### Scenario: Model definition
- **WHEN** defining an Odoo model
- **THEN** class inherits from `models.Model`, `models.TransientModel`, or `models.AbstractModel`
- **AND** `_name` attribute is defined with dot notation (e.g., 'res.partner')
- **AND** `_description` attribute provides human-readable description

#### Scenario: Field definitions
- **WHEN** defining model fields
- **THEN** fields use appropriate types: `fields.Char`, `fields.Integer`, `fields.Many2one`, `fields.One2many`, `fields.Selection`, etc.
- **AND** required fields have `required=True`
- **AND** relational fields specify correct `comodel_name`

#### Scenario: Recordset operations
- **WHEN** performing ORM operations
- **THEN** methods operate on recordsets (self is always a recordset)
- **AND** iteration over recordsets uses `for record in self:`
- **AND** single record access uses `self.ensure_one()` when required

#### Scenario: CRUD operations
- **WHEN** creating records
- **THEN** use `self.env['model.name'].create(vals_dict)`
- **WHEN** searching records
- **THEN** use `self.env['model.name'].search(domain)`
- **WHEN** updating records
- **THEN** use `record.write(vals_dict)` or direct field assignment
- **WHEN** deleting records
- **THEN** use `records.unlink()`

#### Scenario: Computed fields
- **WHEN** defining computed fields
- **THEN** field has `compute` parameter pointing to method name
- **AND** compute method is decorated with `@api.depends('field1', 'field2')`
- **AND** method sets value for all records in recordset

#### Scenario: Onchange methods
- **WHEN** defining onchange methods
- **THEN** method is decorated with `@api.onchange('field_name')`
- **AND** method modifies `self.field_name` directly
- **AND** warnings use `return {'warning': {'title': ..., 'message': ...}}`

---

### Requirement: View Layer (XML)

All Odoo views SHALL be defined in XML data files and follow proper inheritance patterns.

#### Scenario: View definition
- **WHEN** defining a view
- **THEN** view uses `<record>` with `model="ir.ui.view"`
- **AND** view has unique `id` (module_name.view_id_suffix)
- **AND** view specifies `name`, `model`, `arch` fields

#### Scenario: Form view structure
- **WHEN** creating form views
- **THEN** structure follows: `<form> → <sheet> → <group> → <field>`
- **AND** buttons are placed in header or sheet
- **AND** required fields are marked properly

#### Scenario: Tree view structure
- **WHEN** creating tree/list views
- **THEN** structure is: `<tree> → <field>` elements
- **AND** tree can be editable with `editable="top"` or `editable="bottom"`

#### Scenario: View inheritance
- **WHEN** inheriting/extending a view
- **THEN** use `inherit_id` with reference to parent view
- **AND** use xpath expressions to locate elements: `position="after|before|inside|replace|attributes"`
- **AND** xpath expressions use valid selectors: `//field[@name='...']`, `//group[@name='...']`

---

### Requirement: Controller Layer (HTTP)

All HTTP controllers SHALL use Odoo's routing decorators and follow REST-like patterns where applicable.

#### Scenario: Controller definition
- **WHEN** defining a controller
- **THEN** class inherits from `http.Controller`
- **AND** methods are decorated with `@http.route()`
- **AND** route decorator specifies path, type (http/json), auth (user/public/none), methods

#### Scenario: JSON endpoints
- **WHEN** creating JSON API endpoints
- **THEN** route uses `type='json'`
- **AND** method receives parameters from `request.jsonrequest`
- **AND** returns Python dict (auto-serialized to JSON)

#### Scenario: HTTP endpoints
- **WHEN** creating HTML/HTTP endpoints
- **THEN** route uses `type='http'`
- **AND** method returns werkzeug.Response or renders QWeb template
- **AND** uses `request.render('template_id', context)`

---

### Requirement: Security Model

All models and operations SHALL respect Odoo's security framework including access rights and record rules.

#### Scenario: Access rights (ir.model.access.csv)
- **WHEN** defining model access
- **THEN** CSV file contains columns: id, name, model_id:id, group_id:id, perm_read, perm_write, perm_create, perm_unlink
- **AND** at minimum, one access rule exists per model
- **AND** access rules reference security groups

#### Scenario: Record rules
- **WHEN** defining row-level security
- **THEN** use `<record model="ir.rule">`
- **AND** rule includes domain filter
- **AND** rule specifies applicable groups
- **AND** rule sets permissions: perm_read, perm_write, perm_create, perm_unlink

#### Scenario: Field-level security
- **WHEN** restricting field access
- **THEN** use `groups` attribute on field definition
- **AND** field is hidden/readonly for users not in specified groups

---

### Requirement: Database Schema and Migrations

All model changes SHALL be reflected in database schema with proper migration handling when needed.

#### Scenario: Automatic schema updates
- **WHEN** adding new fields to models
- **THEN** Odoo creates corresponding database columns on module upgrade
- **WHEN** removing fields from models
- **THEN** columns remain in database but are no longer accessible via ORM

#### Scenario: Module dependencies
- **WHEN** module depends on other modules
- **THEN** dependencies are listed in `__manifest__.py` depends field
- **AND** dependent modules are loaded before current module

---

### Requirement: Business Logic Patterns

All business logic SHALL be placed in appropriate model methods, not in views or controllers.

#### Scenario: Action methods
- **WHEN** implementing button actions
- **THEN** method is defined in model class
- **AND** method operates on `self` recordset
- **AND** method returns action dictionary if navigation is needed

#### Scenario: Constraints
- **WHEN** enforcing data validation
- **THEN** use Python constraints with `@api.constrains('field1', 'field2')`
- **OR** use SQL constraints in `_sql_constraints` class attribute
- **AND** raise `ValidationError` with user-friendly message

#### Scenario: Default values
- **WHEN** setting field defaults
- **THEN** use `default=value` in field definition
- **OR** define `_defaults` dictionary (deprecated)
- **OR** implement method `_default_field_name()` and set `default=_default_field_name`

---

### Requirement: Automation and Scheduled Actions

Scheduled actions (cron jobs) SHALL be defined via XML data and execute model methods.

#### Scenario: Cron job definition
- **WHEN** creating scheduled action
- **THEN** use `<record model="ir.cron">`
- **AND** specify: name, model_id, state, code, interval_number, interval_type, numbercall

#### Scenario: Cron job execution
- **WHEN** cron job runs
- **THEN** executes code field content (usually method call)
- **AND** logs errors to Odoo logging system
- **AND** respects numbercall limit (infinite if -1)

---

### Requirement: Reporting (QWeb)

Reports SHALL use QWeb templates and wkhtmltopdf for PDF generation.

#### Scenario: Report definition
- **WHEN** defining a report
- **THEN** use `<report>` tag with id, name, model, report_type, file, string
- **AND** report template uses QWeb syntax
- **AND** template iterates over `docs` variable containing records

#### Scenario: Report generation
- **WHEN** generating PDF report
- **THEN** use `report_type="qweb-pdf"`
- **AND** wkhtmltopdf converts QWeb HTML to PDF
- **AND** report is downloadable from UI or API

---

### Requirement: Odoo Environment and Context

All operations SHALL properly use `self.env` for database access and context for state passing.

#### Scenario: Environment access
- **WHEN** accessing other models
- **THEN** use `self.env['model.name']`
- **AND** environment provides access to: user, company, lang, tz

#### Scenario: Context manipulation
- **WHEN** passing context data
- **THEN** use `record.with_context(key=value)`
- **AND** context values accessed via `self.env.context.get('key')`

#### Scenario: Superuser access
- **WHEN** bypassing access rights for system operations
- **THEN** use `self.sudo()` to escalate privileges
- **AND** use sparingly and document security implications

---

## Design Patterns

### MVC Separation
- **Models**: Business logic, data structure, validations, computed fields
- **Views**: UI definition, layout, field visibility, buttons
- **Controllers**: HTTP routing, session management, external API endpoints

### Inheritance Patterns
- **Classical Inheritance** (`_inherit`): Extend existing model
- **Extension** (same `_name` and `_inherit`): Modify in-place
- **Delegation** (`_inherits`): Embed another model's fields

### Data Flow
1. User action in View
2. Controller receives request
3. Controller calls Model method
4. Model performs business logic and ORM operations
5. Model returns result
6. Controller formats response
7. View renders updated data

---

## External References

- Odoo Official Documentation: https://www.odoo.com/documentation/15.0/
- Odoo ORM API: https://www.odoo.com/documentation/15.0/developer/reference/backend/orm.html
- Odoo Web Controllers: https://www.odoo.com/documentation/15.0/developer/reference/backend/http.html
