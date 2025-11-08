# Change: Odoo 18 Custom Module Migration

## Why

This change addresses the comprehensive migration of 20 custom Odoo modules from version 15 to version 18. Based on the detailed codebase analysis, the custom modules include:

- **4 Core Accounting Modules** (base_account_budget, base_accounting_kit, payment_adjustment, partner_account_creation)
- **5 Real Estate Modules** (itsys_real_estate, project_transactions, real_estate_extension, real_estate_sheets)
- **4 Dashboard Modules** (jupiter_dashboard, jupiter_dashboard_deux, jupiter_dashboard_tres, jupiter_dashboard_optima)
- **1 Transaction Module** (jupiter_accounts)
- **3 UI Control Modules** (hide_menu_user, kg_hide_menu, disable_quick_create)
- **4 Specialized Modules** (gst_invoice, odoo_de_brand, ms_query, report_pdf_options)

All modules are currently on Odoo 15 (or 13) and require updates to:
- Manifest version strings (15.0.x → 18.0.x)
- Python code (decorators, ORM patterns, imports)
- XML views (xpath syntax, attributes)
- JavaScript (OWL 2, ES6 patterns)
- Dependencies (verify all exist in Odoo 18)

## What Changes

- Update all 20 custom module manifests to version 18.0.x
- Modernize Python code (deprecated decorators, ORM methods)
- Fix XML view inheritance and attributes
- Migrate JavaScript to OWL 2 framework
- Verify and update all module dependencies
- Test all business logic with sample records
- Validate security rules and access rights
- Ensure custom reports and dashboards work correctly

## Impact

- **Affected specs**: `custom-module-migration`, all module-specific specs
- **Affected code**: All 20 custom modules in `addons_custom/`
  - 136 Python model files
  - 142 XML view files
  - Multiple JavaScript assets
- **Breaking changes**: None (backward compatible migration)
- **Migration Priority**: HIGH RISK modules must be done first:
  1. itsys_real_estate (largest, most dependent-upon)
  2. real_estate_extension (heavy API dependencies)
  3. jupiter_accounts (transaction-critical)
  4. base_accounting_kit (production-critical accounting)

## Priority

**CRITICAL** - Core Phase 3 work for Odoo 15→18 migration project
