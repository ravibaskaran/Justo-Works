# JavaScript to OWL Migration Guide - Odoo 18

## Overview

This guide provides step-by-step instructions for migrating JavaScript code from Odoo 15's legacy Widget pattern to Odoo 18's OWL (Odoo Web Library) framework.

**Estimated Effort:** 140-210 hours across 27 JavaScript files
**Complexity:** HIGH
**Priority:** CRITICAL (blocking for module installation)

---

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Pattern Migrations](#pattern-migrations)
3. [Module-Specific Guides](#module-specific-guides)
4. [Common Pitfalls](#common-pitfalls)
5. [Testing Checklist](#testing-checklist)

---

## Quick Reference

### File Header Changes

**Before (Odoo 15):**
```javascript
odoo.define('module_name.ComponentName', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    // ...
});
```

**After (Odoo 18):**
```javascript
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
```

---

## Pattern Migrations

### 1. Dashboard/Action Widget Migration

#### Pattern: AbstractAction.extend → OWL Component

**BEFORE (Odoo 15):**
```javascript
// jupiter_dashboard/static/src/js/dashboard.js
odoo.define('jupiter_dashboard.JupiterDashboard', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;

    var JupiterDashboard = AbstractAction.extend({
        template: 'JupiterDashboard',

        events: {
            'click .button_class': '_onButtonClick',
        },

        init: function(parent, context) {
            this._super(parent, context);
            this.data = {};
        },

        willStart: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function() {
                return self._rpc({
                    model: 'some.model',
                    method: 'get_data',
                }).then(function(result) {
                    self.data = result;
                });
            });
        },

        start: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function() {
                self._renderDashboard();
            });
        },

        _renderDashboard: function() {
            // Rendering logic
            this.$('.chart-container').html('<canvas id="myChart"></canvas>');
            this._renderChart();
        },

        _renderChart: function() {
            var ctx = document.getElementById('myChart');
            new Chart(ctx, {
                type: 'bar',
                data: this.data
            });
        },

        _onButtonClick: function(ev) {
            // Handle click
        },
    });

    core.action_registry.add('jupiter_dashboard', JupiterDashboard);

    return JupiterDashboard;
});
```

**AFTER (Odoo 18):**
```javascript
/** @odoo-module **/

import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class JupiterDashboard extends Component {
    static template = "jupiter_dashboard.JupiterDashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");

        this.chartRef = useRef("chartCanvas");
        this.data = {};

        onWillStart(async () => {
            await this.loadData();
        });

        onMounted(() => {
            this.renderChart();
        });
    }

    async loadData() {
        this.data = await this.orm.call(
            'some.model',
            'get_data',
            []
        );
    }

    renderChart() {
        if (!this.chartRef.el) return;

        new Chart(this.chartRef.el, {
            type: 'bar',
            data: this.data
        });
    }

    onButtonClick(ev) {
        // Handle click
        this.notification.add("Button clicked", {
            type: "success",
        });
    }
}

registry.category("actions").add("jupiter_dashboard", JupiterDashboard);
```

**Template Changes (XML):**
```xml
<!-- BEFORE (Odoo 15) -->
<templates>
    <t t-name="JupiterDashboard">
        <div class="jupiter-dashboard">
            <button class="button_class">Click Me</button>
            <div class="chart-container"></div>
        </div>
    </t>
</templates>

<!-- AFTER (Odoo 18) -->
<templates xml:space="preserve">
    <t t-name="jupiter_dashboard.JupiterDashboard" owl="1">
        <div class="jupiter-dashboard">
            <button t-on-click="onButtonClick">Click Me</button>
            <div class="chart-container">
                <canvas t-ref="chartCanvas"/>
            </div>
        </div>
    </t>
</templates>
```

---

### 2. Custom Field Widget Migration

#### Pattern: AbstractField.extend → StandardFieldProps Component

**BEFORE (Odoo 15):**
```javascript
// itsys_real_estate/static/src/js/map_widget.js
odoo.define('itsys_real_estate.MapWidget', function (require) {
    'use strict';

    var AbstractField = require('web.AbstractField');
    var fieldRegistry = require('web.field_registry');

    var MapWidget = AbstractField.extend({
        template: 'MapWidget',

        _render: function() {
            this._super.apply(this, arguments);
            this._initializeMap();
        },

        _initializeMap: function() {
            var lat = this.value ? JSON.parse(this.value).lat : 0;
            var lng = this.value ? JSON.parse(this.value).lng : 0;

            var map = new google.maps.Map(this.$el[0], {
                center: {lat: lat, lng: lng},
                zoom: 13
            });

            this.marker = new google.maps.Marker({
                position: {lat: lat, lng: lng},
                map: map,
                draggable: true
            });

            google.maps.event.addListener(this.marker, 'dragend',
                this._onMarkerDragEnd.bind(this));
        },

        _onMarkerDragEnd: function(event) {
            var position = {
                lat: event.latLng.lat(),
                lng: event.latLng.lng()
            };
            this._setValue(JSON.stringify(position));
        },
    });

    fieldRegistry.add('map_widget', MapWidget);

    return MapWidget;
});
```

**AFTER (Odoo 18):**
```javascript
/** @odoo-module **/

import { Component, onMounted, onWillUpdateProps, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

class MapWidget extends Component {
    static template = "itsys_real_estate.MapWidget";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.mapContainer = useRef("mapContainer");
        this.map = null;
        this.marker = null;

        onMounted(() => {
            this.initializeMap();
        });

        onWillUpdateProps((nextProps) => {
            if (nextProps.value !== this.props.value) {
                this.updateMarkerPosition(nextProps.value);
            }
        });
    }

    initializeMap() {
        const value = this.props.value ? JSON.parse(this.props.value) : {lat: 0, lng: 0};

        this.map = new google.maps.Map(this.mapContainer.el, {
            center: value,
            zoom: 13
        });

        this.marker = new google.maps.Marker({
            position: value,
            map: this.map,
            draggable: !this.props.readonly
        });

        if (!this.props.readonly) {
            this.marker.addListener('dragend', (event) => {
                this.onMarkerDragEnd(event);
            });
        }
    }

    updateMarkerPosition(newValue) {
        if (!newValue || !this.marker) return;
        const position = JSON.parse(newValue);
        this.marker.setPosition(position);
        this.map.setCenter(position);
    }

    onMarkerDragEnd(event) {
        const position = {
            lat: event.latLng.lat(),
            lng: event.latLng.lng()
        };
        this.props.update(JSON.stringify(position));
    }
}

registry.category("fields").add("map_widget", {
    component: MapWidget,
});
```

**Template Changes:**
```xml
<!-- BEFORE -->
<templates>
    <t t-name="MapWidget">
        <div class="o_map_widget"></div>
    </t>
</templates>

<!-- AFTER -->
<templates xml:space="preserve">
    <t t-name="itsys_real_estate.MapWidget" owl="1">
        <div class="o_map_widget" t-ref="mapContainer"></div>
    </t>
</templates>
```

---

### 3. Controller Patching Migration

#### Pattern: Controller.include → patch()

**BEFORE (Odoo 15):**
```javascript
// real_estate_sheets/static/src/js/import.js
odoo.define('real_estate_sheets.import', function (require) {
    'use strict';

    var ListController = require('web.ListController');
    var core = require('web.core');
    var _t = core._t;

    ListController.include({
        events: _.extend({}, ListController.prototype.events, {
            'click .import_competition_sheet': 'onClickCompetitionSheetImport',
        }),

        onClickCompetitionSheetImport: function(ev) {
            ev.preventDefault();
            var self = this;

            // Show file upload dialog
            var $input = $('<input type="file" accept=".xlsx">');
            $input.on('change', function(e) {
                self._uploadFile(e.target.files[0]);
            });
            $input.click();
        },

        _uploadFile: function(file) {
            var self = this;
            var formData = new FormData();
            formData.append('file', file);

            this._rpc({
                route: '/real_estate_sheets/import',
                params: formData,
            }).then(function(result) {
                if (result.success) {
                    self.do_notify(_t('Success'), _t('File imported successfully'));
                    self.reload();
                }
            });
        },
    });
});
```

**AFTER (Odoo 18):**
```javascript
/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

patch(ListController.prototype, "real_estate_sheets.ListController", {
    setup() {
        this._super(...arguments);
        this.notification = useService("notification");
        this.rpc = useService("rpc");
    },

    async onClickCompetitionSheetImport(ev) {
        ev.preventDefault();

        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.xlsx';

        input.addEventListener('change', async (e) => {
            await this.uploadFile(e.target.files[0]);
        });

        input.click();
    },

    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const result = await this.rpc('/real_estate_sheets/import', formData);

            if (result.success) {
                this.notification.add(_t('File imported successfully'), {
                    type: 'success',
                });
                await this.model.load();
                this.render();
            }
        } catch (error) {
            this.notification.add(_t('Import failed'), {
                type: 'danger',
            });
        }
    },
});

// Add button to control panel
patch(ListController.prototype, "real_estate_sheets.ListControllerButtons", {
    get className() {
        return `${this._super(...arguments)} o_real_estate_sheets_list`;
    },
});
```

**Control Panel Button (XML):**
```xml
<!-- AFTER: Add button to control panel -->
<templates xml:space="preserve">
    <t t-name="real_estate_sheets.ListController.Buttons" t-inherit="web.ListController.Buttons" owl="1">
        <xpath expr="//t[@t-if='!env.isSmall']" position="inside">
            <button class="btn btn-primary import_competition_sheet"
                    t-on-click="onClickCompetitionSheetImport">
                Import Competition Sheet
            </button>
        </xpath>
    </t>
</templates>
```

---

### 4. RPC Call Migration

**BEFORE (Odoo 15):**
```javascript
this._rpc({
    model: 'account.move',
    method: 'get_dashboard_data',
    args: [[], domain],
}).then(function(result) {
    // handle result
});
```

**AFTER (Odoo 18):**
```javascript
// Using ORM service
const result = await this.orm.call(
    'account.move',
    'get_dashboard_data',
    [[], domain]
);

// Or using RPC service for routes
const result = await this.rpc('/my/custom/route', {
    param1: value1,
    param2: value2,
});
```

---

### 5. Notification Migration

**BEFORE (Odoo 15):**
```javascript
this.do_notify(_t('Success'), _t('Operation completed'), false);
this.do_warn(_t('Warning'), _t('Please check input'));
```

**AFTER (Odoo 18):**
```javascript
// In setup()
this.notification = useService("notification");

// Then use:
this.notification.add(_t('Operation completed'), {
    type: 'success',
    title: _t('Success'),
});

this.notification.add(_t('Please check input'), {
    type: 'warning',
    title: _t('Warning'),
});
```

---

### 6. Action Execution Migration

**BEFORE (Odoo 15):**
```javascript
this.do_action({
    type: 'ir.actions.act_window',
    res_model: 'res.partner',
    views: [[false, 'form']],
    target: 'new',
});
```

**AFTER (Odoo 18):**
```javascript
// In setup()
this.action = useService("action");

// Then use:
await this.action.doAction({
    type: 'ir.actions.act_window',
    res_model: 'res.partner',
    views: [[false, 'form']],
    target: 'new',
});
```

---

## Module-Specific Guides

### Jupiter Dashboards (4 modules)

**Files to Migrate:**
- `jupiter_dashboard/static/src/js/dashboard.js`
- `jupiter_dashboard_deux/static/src/js/dashboard.js`
- `jupiter_dashboard_tres/static/src/js/dashboard.js`
- `jupiter_dashboard_optima/static/src/js/dashboard.js`

**Common Pattern:**
All four dashboards use similar AbstractAction.extend patterns with chart rendering.

**Migration Priority:** HIGH
**Estimated Effort:** 60-80 hours (15-20h each)

**Key Changes:**
1. Convert AbstractAction to OWL Component
2. Convert Chart.js/Highcharts rendering to use `onMounted` lifecycle
3. Update RPC calls to use `orm` service
4. Convert event handlers to `t-on-click` in templates
5. Update asset bundles in manifest

### Base Accounting Kit

**Files to Migrate:**
- `account_dashboard.js` - Dashboard with multiple charts
- `payment_matching.js` - Payment matching widget
- `payment_render.js` - Payment renderer
- `payment_model.js` - Payment model
- `account_asset.js` - Asset management

**Migration Priority:** CRITICAL
**Estimated Effort:** 35-45 hours

**Special Considerations:**
- Complex chart interactions
- Multiple RPC calls
- Payment matching logic must preserve behavior
- Test thoroughly with real data

### Itsys Real Estate

**Files to Migrate:**
- `map_widget.js` - Google Maps integration
- `map_widget_multi.js` - Multiple locations map
- `place_autocomplete.js` - Google Places autocomplete
- `view_file_toggle.js` - File view toggle
- `swipe_images_backend.js` - Image gallery
- Other utility widgets

**Migration Priority:** CRITICAL
**Estimated Effort:** 30-40 hours

**Special Considerations:**
- Google Maps API integration
- Event listeners on map markers
- Image gallery interactivity
- Test with actual Google Maps API key

---

## Common Pitfalls

### 1. `this` Context

**Problem:** In OWL, `this` inside arrow functions always refers to the component.

**BEFORE (Odoo 15):**
```javascript
var self = this;
setTimeout(function() {
    self.doSomething();
}, 1000);
```

**AFTER (Odoo 18):**
```javascript
// Arrow function preserves this
setTimeout(() => {
    this.doSomething();
}, 1000);
```

### 2. Template References

**Problem:** Accessing DOM elements.

**BEFORE (Odoo 15):**
```javascript
this.$('.my-element').addClass('active');
```

**AFTER (Odoo 18):**
```javascript
// Use t-ref in template
const myElement = useRef("myElement");

// In onMounted or method:
myElement.el.classList.add('active');
```

### 3. Reactivity

**Problem:** OWL requires explicit reactive state.

**BEFORE (Odoo 15):**
```javascript
this.myData = {};
this.myData.value = 'changed'; // Automatically re-renders
```

**AFTER (Odoo 18):**
```javascript
import { useState } from "@odoo/owl";

setup() {
    this.state = useState({
        myData: {},
    });
}

// Modify reactive state
this.state.myData.value = 'changed'; // Triggers re-render
```

### 4. jQuery Dependencies

**Problem:** Odoo 18 minimizes jQuery usage.

**BEFORE (Odoo 15):**
```javascript
this.$el.find('.selector').hide();
```

**AFTER (Odoo 18):**
```javascript
// Use vanilla JS or refs
const element = this.el.querySelector('.selector');
element.style.display = 'none';

// Or better, use t-if in template
```

---

## Testing Checklist

### Per Module

- [ ] Module installs without errors
- [ ] No JavaScript console errors
- [ ] All buttons/clicks work correctly
- [ ] RPC calls complete successfully
- [ ] Charts render correctly
- [ ] Notifications display properly
- [ ] Forms save data correctly
- [ ] Navigation actions work
- [ ] Performance is acceptable
- [ ] Mobile responsiveness maintained

### Integration Testing

- [ ] Module works with other migrated modules
- [ ] Dashboard data loads correctly
- [ ] Report generation works
- [ ] Export functionality works
- [ ] Import functionality works
- [ ] Wizards function correctly

---

## Resources

### Official Documentation
- **OWL Guide**: https://github.com/odoo/owl/tree/master/doc
- **Odoo 18 Migration Guide**: https://www.odoo.com/documentation/18.0/developer/howtos/upgrade.html
- **JavaScript Framework**: https://www.odoo.com/documentation/18.0/developer/reference/frontend/javascript_reference.html

### Code Examples
- **Odoo GitHub**: https://github.com/odoo/odoo/tree/18.0/addons/web/static/src

### Testing
- **QUnit Tests**: https://www.odoo.com/documentation/18.0/developer/reference/frontend/qunit.html

---

## Migration Template Checklist

For each JavaScript file:

1. [ ] Add `/** @odoo-module **/` header
2. [ ] Replace `odoo.define` with ES6 imports
3. [ ] Convert Widget.extend to Component class
4. [ ] Add `setup()` method with hooks
5. [ ] Convert lifecycle methods (init→setup, willStart→onWillStart, start→onMounted)
6. [ ] Update RPC calls to use services
7. [ ] Convert event handlers to t-on-* directives
8. [ ] Update DOM manipulation to use refs
9. [ ] Register component in appropriate registry
10. [ ] Update template with OWL syntax
11. [ ] Update manifest assets section
12. [ ] Test thoroughly

---

**Last Updated:** 2025-11-09
**Odoo Version Target:** 18.0
**Complexity:** HIGH
**Estimated Total Effort:** 140-210 hours
