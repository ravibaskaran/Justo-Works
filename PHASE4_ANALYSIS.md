# Phase 4: Advanced Web Components Migration Analysis

## Migration Status: IN PROGRESS
**Started:** 2025-11-10
**Estimated Completion:** TBD

## Overview
Phase 4 focuses on migrating advanced web components from Odoo 15 to Odoo 18 OWL framework across 14 custom modules. These modules contain complex JavaScript implementations including dashboards, widgets, custom fields, and integrations.

---

## Migration Requirements

### Core Odoo 18 Changes
1. **JavaScript Framework:**
   - `odoo.define()` → ES6 modules with `@odoo/owl`
   - `Widget.extend()` → OWL Components
   - `AbstractAction.extend()` → OWL Components with services
   - `.include()` → `patch()` pattern

2. **Service Injection:**
   - `web.rpc` → `useService("rpc")`
   - `web.ajax` → `useService("ajax")` or fetch API
   - `web_client` → `useService("action")`

3. **QWeb Templates:**
   - Convert to OWL XML templates
   - Update template references and data binding

4. **Event Handling:**
   - jQuery events → OWL event handlers (t-on-click, etc.)
   - Direct DOM manipulation → reactive state management

---

## Module Breakdown (14 Modules)

### Priority 1: Core Real Estate Module (Highest Complexity)
#### 1. **itsys_real_estate** ⏳
- **JavaScript Files:** 10 files
  - `map_widget.js` - Google Maps integration widget
  - `map_widget_multi.js` - Multiple location map widget
  - `place_autocomplete.js` - Google Places autocomplete
  - `place_autocomplete_multi.js` - Multi-field autocomplete
  - `view_file_toggle.js` - File view toggle functionality
  - `swipe_images_backend.js` - Image gallery swiper
  - `pyeval.js` - Python expression evaluator
  - `init.js` - Module initialization
  - `ug-theme-compact.js` - Gallery theme (3rd party)
  - `unitegallery.min.js` - Gallery library (3rd party - no migration)

- **External Dependencies:**
  - Google Maps API
  - jQuery.Brazzers-Carousel.js
  - Lightbox library

- **Migration Complexity:** HIGH
  - Complex widget inheritance
  - Third-party library integrations
  - Google Maps API integration
  - Image gallery components

- **Estimated Effort:** 10-12 hours

---

### Priority 2: Accounting Dashboard (High Complexity)
#### 2. **base_accounting_kit** ⏳
- **JavaScript Files:** 5 custom files + libraries
  - `account_dashboard.js` - Main dashboard with Chart.js (1,714 lines!)
  - `payment_model.js` - Payment reconciliation model
  - `payment_matching.js` - Payment matching logic
  - `payment_render.js` - Payment rendering
  - `account_asset.js` - Asset management

- **External Libraries (no migration needed):**
  - Chart.js / Chart.bundle.js
  - FusionCharts
  - Bootstrap Toggle
  - jQuery 3.3.1

- **Migration Complexity:** HIGH
  - Very large file (1,714 lines)
  - Extensive RPC calls
  - Complex Chart.js integration
  - Heavy jQuery DOM manipulation
  - Multiple event handlers

- **Estimated Effort:** 12-15 hours

---

### Priority 3: Real Estate Extensions (Medium-High Complexity)
#### 3. **real_estate_sheets** ⏳
- **JavaScript Files:** 5 files
  - `list_renderer.js` - Custom list renderer extension
  - `relational_fields.js` - Custom relational field widgets
  - `abstract_field.js` - Base field extension
  - `button_generate.js` - Sheet generation button
  - `import.js` - Import functionality

- **Migration Complexity:** MEDIUM-HIGH
  - ListRenderer patching required
  - Custom field implementations
  - Form/List view customizations

- **Estimated Effort:** 8-10 hours

#### 4. **real_estate_extension** ⏳
- **JavaScript Files:** 2 files
  - `fields.js` - Custom field widgets
  - `one2manySearch.js` - One2Many search widget

- **Migration Complexity:** MEDIUM
  - Field widget implementations
  - Relational field customizations

- **Estimated Effort:** 4-6 hours

---

### Priority 4: Dashboard Modules (Medium Complexity)
#### 5. **jupiter_dashboard_trois** ⏳
- **JavaScript Files:** 5 files
  - `dashboard.js` - Main dashboard component
  - `highcharts.js` - Highcharts library (no migration)
  - `export-data.js` - Highcharts export module
  - `exporting.js` - Export functionality
  - `accessibility.js` - Highcharts accessibility

- **Migration Complexity:** MEDIUM
  - Highcharts integration
  - Dashboard rendering
  - Export functionality

- **Estimated Effort:** 6-8 hours

#### 6. **jupiter_dashboard_deux** ⏳
- **JavaScript Files:** 1 file
  - `dashboard.js` - Dashboard component

- **Migration Complexity:** MEDIUM
  - Similar to jupiter_dashboard_trois

- **Estimated Effort:** 4-5 hours

#### 7. **jupiter_dashboard** ⏳
- **JavaScript Files:** Check pending
- **Migration Complexity:** MEDIUM
- **Estimated Effort:** 4-5 hours

#### 8. **jupiter_dashboard_optima** ⏳
- **JavaScript Files:** Check pending
- **Migration Complexity:** MEDIUM
- **Estimated Effort:** 4-5 hours

---

### Priority 5: System & UI Customizations (Low-Medium Complexity)
#### 9. **odoo_de_brand** ⏳
- **JavaScript Files:** 3 files
  - `error_dialogs.js` - Custom error dialog handling
  - `basic_controller.js` - Controller customizations
  - `user_menu_items.js` - User menu modifications

- **Migration Complexity:** MEDIUM
  - Error handling customization
  - Controller patching
  - UI component modifications

- **Estimated Effort:** 4-6 hours

#### 10. **disable_quick_create** ⏳
- **JavaScript Files:** 1 file
  - `disable_quick_create.js` - Disable quick create in various views

- **Migration Complexity:** LOW
  - Simple functionality override

- **Estimated Effort:** 1-2 hours

---

### Priority 6: Python-Only Modules (Review Only)
These modules need Python compatibility review but have no JavaScript:

#### 11. **gst_invoice** ✓
- **JavaScript Files:** 0
- **Migration:** Python review only
- **Estimated Effort:** 2-3 hours

#### 12. **jupiter_accounts** ✓
- **JavaScript Files:** 0
- **Migration:** Python review only
- **Estimated Effort:** 2-3 hours

#### 13. **ms_query** ✓
- **JavaScript Files:** 0
- **Migration:** Python review only
- **Estimated Effort:** 2-3 hours

#### 14. **report_pdf_options** ✓
- **JavaScript Files:** 0
- **Migration:** Python review only
- **Estimated Effort:** 2-3 hours

---

## Additional Modules (Python-Only Review)
- **base_account_budget** - Python review
- **hide_menu_user** - Python review
- **kg_hide_menu** - Python review
- **partner_account_creation** - Python review
- **payment_adjustment** - Python review
- **project_transactions** - Python review

---

## Migration Strategy

### Phase 4A: Foundation (Weeks 1-2)
1. itsys_real_estate (map widgets, autocomplete)
2. disable_quick_create (simple, warm-up)

### Phase 4B: Advanced Components (Weeks 3-4)
3. base_accounting_kit (dashboard, payment modules)
4. real_estate_sheets (list renderer, fields)
5. real_estate_extension (custom fields)

### Phase 4C: Dashboards (Week 5)
6. jupiter_dashboard_trois
7. jupiter_dashboard_deux
8. jupiter_dashboard
9. jupiter_dashboard_optima

### Phase 4D: System Customizations (Week 6)
10. odoo_de_brand (error handling, UI)
11. Python-only module reviews

---

## Technical Migration Patterns

### Pattern 1: Widget to OWL Component
```javascript
// Odoo 15
odoo.define('module.Widget', function (require) {
    var Widget = require('web.Widget');
    return Widget.extend({
        template: 'template_name',
        events: {
            'click .button': '_onClick',
        },
        _onClick: function() {}
    });
});

// Odoo 18
/** @odoo-module **/
import { Component } from "@odoo/owl";

export class MyComponent extends Component {
    static template = "module.template_name";

    onClick() {
        // handler
    }
}
```

### Pattern 2: AbstractAction Migration
```javascript
// Odoo 15
var AbstractAction = require('web.AbstractAction');
var ActionMenu = AbstractAction.extend({
    contentTemplate: 'Template',
});

// Odoo 18
/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ActionMenu extends Component {
    static template = "module.Template";
}
registry.category("actions").add("action_name", ActionMenu);
```

### Pattern 3: Include to Patch
```javascript
// Odoo 15
var ListRenderer = require("web.ListRenderer");
ListRenderer.include({
    _renderHeaderCell: function (node) {
        var res = this._super(node);
        // custom logic
        return res;
    }
});

// Odoo 18
/** @odoo-module **/
import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";

patch(ListRenderer.prototype, {
    _renderHeaderCell(node) {
        const res = super._renderHeaderCell(node);
        // custom logic
        return res;
    }
});
```

### Pattern 4: RPC Service Usage
```javascript
// Odoo 15
var rpc = require('web.rpc');
rpc.query({
    model: "account.move",
    method: "get_data",
    args: [posted],
}).then(function(result) {
    // handle result
});

// Odoo 18
import { useService } from "@web/core/utils/hooks";

setup() {
    this.rpc = useService("rpc");
}

async loadData() {
    const result = await this.rpc("/web/dataset/call_kw", {
        model: "account.move",
        method: "get_data",
        args: [posted],
        kwargs: {},
    });
    // handle result
}
```

---

## Quality Standards
- ✅ All JavaScript converted to ES6 modules
- ✅ OWL components with proper lifecycle
- ✅ Service injection instead of require()
- ✅ Reactive state management (useState, useRef)
- ✅ Event handlers using t-on-* directives
- ✅ No direct jQuery DOM manipulation (where possible)
- ✅ Proper error handling
- ✅ Code comments preserved
- ✅ Manifest files updated (__manifest__.py)
- ✅ Assets bundles configured correctly

---

## Testing Checklist (Per Module)
- [ ] JavaScript console has no errors
- [ ] All widgets render correctly
- [ ] Event handlers work as expected
- [ ] RPC calls return proper data
- [ ] Third-party libraries load correctly
- [ ] Mobile responsive (if applicable)
- [ ] No jQuery conflicts
- [ ] Browser compatibility (Chrome, Firefox, Safari)

---

## Estimated Timeline
- **Phase 4A:** 2 weeks (14-20 hours)
- **Phase 4B:** 2 weeks (26-34 hours)
- **Phase 4C:** 1 week (18-23 hours)
- **Phase 4D:** 1 week (14-20 hours)
- **Total:** 6 weeks (72-97 hours)

---

## Progress Tracking
- [ ] Phase 4A: Foundation
- [ ] Phase 4B: Advanced Components
- [ ] Phase 4C: Dashboards
- [ ] Phase 4D: System Customizations
- [ ] Final Review & Testing
- [ ] Documentation Updates

---

## Next Steps
1. Start with `disable_quick_create` (simplest module - warm up)
2. Move to `itsys_real_estate` (largest, most complex)
3. Proceed through priorities systematically
4. Document patterns and reusable components
5. Test incrementally after each module

---

**Last Updated:** 2025-11-10
**Status:** Analysis Complete, Ready to Begin Migration
