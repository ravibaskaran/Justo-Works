# Phase 2: Module Migration Checklist

## Quick Start Guide

**Status:** Ready to begin after Odoo 18 setup complete
**Estimated Duration:** 3-5 weeks
**Team Size:** 1-2 developers

---

## Week 1: Foundation & Setup

### Day 1: Environment & Quick Wins (8 hours)

#### Morning (4h)
- [ ] **Test Odoo 18 environment**
  ```bash
  sudo systemctl status odoo18
  curl http://localhost:8069
  ```

- [ ] **Create migration branch**
  ```bash
  cd /opt/justo-wrks
  git checkout -b feature/odoo18-module-migration
  ```

- [ ] **Update all manifest files** (2 hours - QUICK WIN)
  ```bash
  # Script to update all manifests
  for manifest in addons_custom/*/__manifest__.py; do
      sed -i "s/'version': '15\.0/'version': '18.0/g" "$manifest"
  done

  # Commit quick wins
  git add addons_custom/*/__manifest__.py
  git commit -m "Update all module versions to 18.0"
  ```

#### Afternoon (4h)
- [ ] **Fix Python deprecated code**
  - Remove `@api.returns` decorators (2 files)
  ```python
  # In kg_hide_menu/models/ir_module.py:17
  # Remove: @api.returns('self')

  # In gst_invoice/models/account_period.py:74
  # Remove: @api.returns('self', lambda value: value.id)
  ```

- [ ] **Fix date/datetime usage** (12 occurrences)
  ```python
  # Replace: fields.Date.today()
  # With: fields.Date.context_today(self)

  # Replace: fields.Datetime.now()
  # With: Datetime.now()  # with proper import
  ```

- [ ] **Test & commit**
  ```bash
  git add -A
  git commit -m "Fix deprecated Python API decorators and date handling"
  git push origin feature/odoo18-module-migration
  ```

---

### Day 2-3: Simple Modules (16 hours)

#### Migrate utility modules (no JavaScript):

**Priority Order:**

1. [ ] **hide_menu_user** (2h)
   - Files: 3 Python, 2 XML
   - Changes: Manifest version only
   - Test: Install, verify menu hiding works

2. [ ] **partner_account_creation** (2h)
   - Files: 2 Python, 1 XML
   - Changes: Manifest version only
   - Test: Create partner, verify account creation

3. [ ] **payment_adjustment** (4h)
   - Files: 5 Python, 4 XML
   - Changes: Manifest + XML view updates
   - Test: Create payment adjustment, reconcile

4. [ ] **base_account_budget** (4h)
   - Files: 6 Python, 6 XML
   - Changes: Manifest + date handling
   - Test: Create budget, verify computations

5. [ ] **project_transactions** (4h)
   - Files: Many Python, XML
   - Changes: Manifest + potential field updates
   - Test: Create project transaction

**Testing Template:**
```bash
# For each module:
sudo -u odoo18 bash -c "
    source /opt/odoo18/odoo18-venv/bin/activate && \
    /opt/odoo18/odoo18/odoo-bin -c /etc/odoo18/odoo18.conf \
    -d test_migration -i MODULE_NAME --stop-after-init --log-level=warn
"

# Check for errors
sudo tail -50 /var/log/odoo18/odoo.log | grep -i error
```

---

### Day 4-5: Preparation for JavaScript Migration (16 hours)

- [ ] **Study OWL documentation**
  - Read: https://github.com/odoo/owl/tree/master/doc
  - Study examples in Odoo 18 source: `/opt/odoo18/odoo18/addons/web/static/src/`

- [ ] **Setup development tools**
  ```bash
  # Install browser extensions
  # - Vue.js devtools (works with OWL)
  # - React Developer Tools
  ```

- [ ] **Create migration templates**
  - Copy template examples from JAVASCRIPT_OWL_MIGRATION_GUIDE.md
  - Set up test environment for JavaScript development

- [ ] **Analyze current JavaScript**
  ```bash
  # Count JavaScript files
  find addons_custom -name "*.js" | wc -l

  # Identify patterns
  grep -r "odoo.define" addons_custom/ | wc -l
  grep -r "AbstractField.extend" addons_custom/
  grep -r "AbstractAction.extend" addons_custom/
  ```

---

## Week 2: JavaScript Migration - Utility & Simple Widgets

### Day 6: Simple JavaScript Modules (8h)

1. [ ] **disable_quick_create** (3h)
   - File: `static/src/js/disable_quick_create.js`
   - Pattern: Simple override
   - Test: Verify quick create is disabled

2. [ ] **kg_hide_menu** (3h)
   - File: May have simple JS
   - Pattern: Menu manipulation
   - Test: Verify menu hiding

3. [ ] **report_pdf_options** (2h)
   - Files: Report generation JS
   - Pattern: Simple action
   - Test: Generate PDF with options

---

### Day 7-10: Dashboard Modules (32h total, ~8h each)

**Pattern:** All dashboards are similar, learn from first, apply to others

#### Module 1: jupiter_dashboard (8h) [LEARN PATTERN]

**Step-by-step:**

1. [ ] **Analyze current code** (1h)
   ```bash
   cat addons_custom/jupiter_dashboard/static/src/js/dashboard.js
   ```
   - List all methods
   - Identify chart libraries used
   - Note RPC calls
   - List event handlers

2. [ ] **Create new OWL component** (3h)
   - Copy template from JAVASCRIPT_OWL_MIGRATION_GUIDE.md
   - Convert AbstractAction to Component
   - Add setup() method
   - Convert lifecycle methods:
     * init → setup
     * willStart → onWillStart
     * start → onMounted

3. [ ] **Migrate template** (1h)
   - Add `owl="1"` attribute
   - Convert `class="button_class"` events to `t-on-click="methodName"`
   - Add `t-ref` for DOM elements

4. [ ] **Update manifest** (0.5h)
   - Move templates from `web.assets_qweb` to `web.assets_backend`

5. [ ] **Test thoroughly** (2h)
   - Install module
   - Open dashboard action
   - Verify charts render
   - Test all buttons
   - Check console for errors

6. [ ] **Document pattern** (0.5h)
   - Note what worked
   - Create reusable snippets for next dashboard

#### Modules 2-4: Remaining Dashboards (24h)

- [ ] **jupiter_dashboard_deux** (6h) [APPLY PATTERN]
- [ ] **jupiter_dashboard_tres** (6h) [APPLY PATTERN - has Highcharts]
- [ ] **jupiter_dashboard_optima** (6h) [APPLY PATTERN - has Highcharts]

**Efficiency Tips:**
- Reuse migration pattern from first dashboard
- Copy-paste common OWL setup code
- Use same template structure
- Test against same data

---

## Week 3: Complex JavaScript Modules

### Day 11-13: Real Estate Modules (24h)

#### itsys_real_estate (12h)

**High Priority Files:**

1. [ ] **map_widget.js** (4h)
   - Convert AbstractField to StandardFieldProps Component
   - Google Maps integration
   - Marker draggable events
   - Test with real coordinates

2. [ ] **map_widget_multi.js** (3h)
   - Multiple markers
   - Similar to map_widget.js
   - Test with multiple locations

3. [ ] **place_autocomplete.js** (2h)
   - Google Places API
   - Autocomplete widget
   - Test with real API key

4. [ ] **Other widgets** (3h)
   - view_file_toggle.js
   - swipe_images_backend.js
   - Various utility widgets

#### real_estate_extension (6h)

1. [ ] **fields.js** (3h)
   - Custom field widgets
   - One2Many extensions

2. [ ] **one2manySearch.js** (3h)
   - Search functionality in One2Many fields

#### real_estate_sheets (6h)

1. [ ] **import.js** (2h)
   - ListController.include → patch
   - File upload functionality

2. [ ] **abstract_field.js** (2h)
   - Base field class

3. [ ] **relational_fields.js + button_generate.js** (2h)
   - Field widgets

---

### Day 14-15: Accounting Module (16h)

#### base_accounting_kit (16h)

**Critical Files (prioritized):**

1. [ ] **account_dashboard.js** (5h)
   - Main accounting dashboard
   - Multiple charts (Chart.js)
   - Complex data loading

2. [ ] **payment_matching.js** (4h)
   - Payment matching interface
   - Critical business logic
   - Test extensively

3. [ ] **payment_render.js + payment_model.js** (4h)
   - Payment rendering logic

4. [ ] **account_asset.js** (3h)
   - Asset management dashboard

---

## Week 4: Controllers & Integration

### Day 16-17: Controller Patching (16h)

1. [ ] **real_estate_sheets - ListController patch** (4h)
2. [ ] **odoo_de_brand - BasicController/FormController** (8h)
3. [ ] **Other controller includes** (4h)

### Day 18-19: GST Invoice Module (12h)

1. [ ] **gst_dashboard.js** (6h)
   - GST reporting dashboard
   - Tax calculations display

2. [ ] **Other GST widgets** (6h)
   - Invoice-specific functionality

---

### Day 20: Final Integration Testing (8h)

- [ ] **Install all modules together**
  ```bash
  sudo -u odoo18 bash -c "
      source /opt/odoo18/odoo18-venv/bin/activate && \
      /opt/odoo18/odoo18/odoo-bin -c /etc/odoo18/odoo18.conf \
      -d production_test -i base_accounting_kit,itsys_real_estate,jupiter_dashboard,gst_invoice \
      --stop-after-init
  "
  ```

- [ ] **Test critical workflows**
  - Accounting: Create invoice, match payment
  - Real Estate: Create property, contract, payment
  - Dashboards: Verify all charts load
  - GST: Generate GST report

- [ ] **Performance testing**
  - Dashboard load times
  - Chart rendering speed
  - Large dataset handling

- [ ] **Documentation**
  - Update module READMEs
  - Document breaking changes
  - Create upgrade guide

---

## Testing Checklist (Per Module)

### Installation Test
```bash
# Test install
sudo -u odoo18 bash -c "source /opt/odoo18/odoo18-venv/bin/activate && \
    /opt/odoo18/odoo18/odoo-bin -c /etc/odoo18/odoo18.conf \
    -d test_MODULE -i MODULE_NAME --stop-after-init"

# Check logs for errors
sudo grep -i "error\|warning\|traceback" /var/log/odoo18/odoo.log | tail -50
```

### Functional Test
- [ ] Module installs without errors
- [ ] Menu items appear
- [ ] Forms open correctly
- [ ] Can create/edit/delete records
- [ ] Reports generate
- [ ] Buttons work
- [ ] No JavaScript console errors

### Browser Console Check
```javascript
// Open browser console (F12)
// Should see NO errors
// Verify Odoo is loaded:
odoo.__DEBUG__
```

### Module-Specific Tests

**For Dashboard Modules:**
- [ ] Dashboard opens
- [ ] Charts render
- [ ] Data loads
- [ ] Filters work
- [ ] Export works

**For Real Estate:**
- [ ] Map widget displays
- [ ] Can select location
- [ ] Autocomplete works
- [ ] Image gallery works

**For Accounting:**
- [ ] Dashboard charts render
- [ ] Payment matching works
- [ ] Reports generate
- [ ] Asset management works

---

## Git Workflow

### Branch Strategy
```bash
# Main migration branch
git checkout -b feature/odoo18-module-migration

# Per module branches (optional)
git checkout -b feature/odoo18-jupiter-dashboard
# Work on module
git add .
git commit -m "Migrate jupiter_dashboard to Odoo 18 OWL"
git checkout feature/odoo18-module-migration
git merge feature/odoo18-jupiter-dashboard
```

### Commit Messages
```
Format: "Migrate [MODULE_NAME] to Odoo 18: [DESCRIPTION]"

Examples:
- "Migrate jupiter_dashboard to Odoo 18: Convert to OWL Component"
- "Fix date handling in payment_adjustment module"
- "Update base_accounting_kit dashboard to OWL framework"
```

---

## Troubleshooting

### Common Issues

**Issue: Module won't install**
```bash
# Check Python syntax
python3 -m py_compile addons_custom/MODULE/models/*.py

# Check manifest syntax
python3 -c "import ast; ast.literal_eval(open('addons_custom/MODULE/__manifest__.py').read())"
```

**Issue: JavaScript errors in console**
```javascript
// Check module is loaded
console.log(odoo.loader.modules);

// Check for OWL errors
// Common: Template not found
// Fix: Check template name matches exactly
```

**Issue: Charts not rendering**
```javascript
// Verify Chart.js loaded
console.log(Chart);

// Check canvas element exists
document.querySelector('canvas#myChart');

// Verify data format
console.log(chartData);
```

---

## Success Criteria

### Module Level
- ✅ Installs without errors
- ✅ No Python exceptions
- ✅ No JavaScript console errors
- ✅ All views render
- ✅ All functionality works
- ✅ Performance acceptable

### Phase Level
- ✅ All 22 modules migrated
- ✅ Integration tests pass
- ✅ User acceptance tests pass
- ✅ Documentation complete
- ✅ Ready for Phase 3 (database migration)

---

## Progress Tracking

**Use this checklist to track progress:**

```markdown
## Week 1 Progress
- [x] Day 1: Foundation (8h)
- [x] Day 2-3: Simple modules (16h)
- [ ] Day 4-5: JavaScript prep (16h)

## Week 2 Progress
- [ ] Day 6: Simple JS modules (8h)
- [ ] Day 7-10: Dashboards (32h)

## Week 3 Progress
- [ ] Day 11-13: Real estate (24h)
- [ ] Day 14-15: Accounting (16h)

## Week 4 Progress
- [ ] Day 16-17: Controllers (16h)
- [ ] Day 18-19: GST Invoice (12h)
- [ ] Day 20: Integration (8h)

Total Hours: ~148h (Est. 3-4 weeks with 1 developer)
```

---

**Last Updated:** 2025-11-09
**Phase:** 2 - Module Migration
**Status:** Ready to begin
**Next Review:** After Week 1 completion
