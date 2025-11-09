# Charting Library Migration Guide
**Migration:** Highcharts → ApexCharts & FusionCharts → Chart.js v4
**For:** Odoo 18 Migration - Justo Works Project
**Date:** 2025-11-09
**Effort:** 8 days (64 hours)

---

## 📋 Overview

This guide provides step-by-step technical instructions for replacing commercial charting libraries with free MIT-licensed alternatives.

### What's Being Replaced

| Old Library | New Library | Modules Affected | License Savings |
|------------|-------------|------------------|-----------------|
| **Highcharts 11.4.8** | **ApexCharts 3.x** | jupiter_dashboard_optima, jupiter_dashboard_tres | $1,750/year |
| **FusionCharts** | **Chart.js 4.4** | base_accounting_kit | $997 one-time |

### Why We're Migrating

✅ **Save $5,747 over 5 years**
✅ **Eliminate license compliance risk**
✅ **Better OWL compatibility** for Odoo 18
✅ **Modern, actively maintained libraries**
✅ **No vendor lock-in**

---

## 🎯 Part 1: Highcharts → ApexCharts Migration

### Modules to Migrate
1. `jupiter_dashboard_tres` (2,127 LOC)
2. `jupiter_dashboard_optima` (4,436 LOC) - depends on tres

---

### Step 1.1: Install ApexCharts Library (30 minutes)

#### Download ApexCharts

```bash
cd /home/user/Justo-Works/addons_custom/jupiter_dashboard_tres/static/src/js/

# Download latest ApexCharts (v3.x)
wget https://cdn.jsdelivr.net/npm/apexcharts@latest/dist/apexcharts.min.js

# Verify download
ls -lh apexcharts.min.js
# Should be ~300-400KB

# Optional: Download source map for debugging
wget https://cdn.jsdelivr.net/npm/apexcharts@latest/dist/apexcharts.min.js.map
```

#### Remove Highcharts Files

```bash
# Backup first
mkdir -p backups/
cp highcharts.js backups/highcharts.js.backup
cp exporting.js backups/exporting.js.backup
cp accessibility.js backups/accessibility.js.backup
cp export-data.js backups/export-data.js.backup

# Remove Highcharts files
rm highcharts.js exporting.js accessibility.js export-data.js

# List remaining files
ls -la
```

---

### Step 1.2: Update Module Manifest (15 minutes)

**File:** `addons_custom/jupiter_dashboard_tres/__manifest__.py`

```python
# BEFORE
{
    'name': 'Jupiter Dashboard Tres',
    'version': '18.0.0.1',  # Update version
    'depends': ['base', 'base_setup'],
    'assets': {
        'web.assets_backend': [
            # OLD - Remove these
            # 'jupiter_dashboard_tres/static/src/js/highcharts.js',
            # 'jupiter_dashboard_tres/static/src/js/exporting.js',
            # 'jupiter_dashboard_tres/static/src/js/accessibility.js',
            # 'jupiter_dashboard_tres/static/src/js/export-data.js',

            # NEW - Add ApexCharts
            'jupiter_dashboard_tres/static/src/js/apexcharts.min.js',

            # Dashboard JavaScript (will be rewritten)
            'jupiter_dashboard_tres/static/src/js/dashboard.js',
            'jupiter_dashboard_tres/static/src/xml/dashboard.xml',
        ],
    },
}
```

**Repeat for `jupiter_dashboard_optima`:**

```bash
# Copy ApexCharts to optima module
cp addons_custom/jupiter_dashboard_tres/static/src/js/apexcharts.min.js \
   addons_custom/jupiter_dashboard_optima/static/src/js/

# Update manifest.py similarly
nano addons_custom/jupiter_dashboard_optima/__manifest__.py
```

---

### Step 1.3: Chart Type Mapping Reference

#### Common Highcharts → ApexCharts Conversions

| Highcharts Chart Type | ApexCharts Chart Type | Notes |
|-----------------------|-----------------------|-------|
| `chart: { type: 'column' }` | `chart: { type: 'bar' }` | Bar is vertical in ApexCharts |
| `chart: { type: 'bar' }` | `chart: { type: 'bar', horizontal: true }` | Specify horizontal |
| `chart: { type: 'line' }` | `chart: { type: 'line' }` | Direct mapping |
| `chart: { type: 'pie' }` | `chart: { type: 'pie' }` | Direct mapping |
| `chart: { type: 'area' }` | `chart: { type: 'area' }` | Direct mapping |
| `chart: { type: 'spline' }` | `chart: { type: 'line', curve: 'smooth' }` | Use curve option |

---

### Step 1.4: Code Migration Patterns

#### Pattern 1: Basic Column Chart

**BEFORE (Highcharts):**

```javascript
// In dashboard.js
Highcharts.chart('container-id', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Monthly Revenue'
    },
    xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    },
    yAxis: {
        title: {
            text: 'Revenue ($)'
        }
    },
    series: [{
        name: 'Revenue',
        data: [29.9, 71.5, 106.4, 129.2, 144.0]
    }]
});
```

**AFTER (ApexCharts):**

```javascript
// In dashboard.js
const options = {
    chart: {
        type: 'bar',  // Note: 'bar' in ApexCharts is vertical (column)
        height: 350,
        toolbar: {
            show: true  // Equivalent to Highcharts exporting
        }
    },
    title: {
        text: 'Monthly Revenue',
        align: 'left'
    },
    xaxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    },
    yaxis: {
        title: {
            text: 'Revenue ($)'
        }
    },
    series: [{
        name: 'Revenue',
        data: [29.9, 71.5, 106.4, 129.2, 144.0]
    }]
};

const chart = new ApexCharts(document.querySelector("#container-id"), options);
chart.render();
```

---

#### Pattern 2: Multiple Series Chart

**BEFORE (Highcharts):**

```javascript
Highcharts.chart('multi-series-chart', {
    chart: {
        type: 'line'
    },
    title: {
        text: 'Revenue vs Expenses'
    },
    xAxis: {
        categories: ['Q1', 'Q2', 'Q3', 'Q4']
    },
    series: [{
        name: 'Revenue',
        data: [100, 120, 140, 160]
    }, {
        name: 'Expenses',
        data: [80, 90, 95, 100]
    }],
    legend: {
        enabled: true
    }
});
```

**AFTER (ApexCharts):**

```javascript
const options = {
    chart: {
        type: 'line',
        height: 350
    },
    title: {
        text: 'Revenue vs Expenses'
    },
    xaxis: {
        categories: ['Q1', 'Q2', 'Q3', 'Q4']
    },
    series: [{
        name: 'Revenue',
        data: [100, 120, 140, 160]
    }, {
        name: 'Expenses',
        data: [80, 90, 95, 100]
    }],
    legend: {
        show: true,
        position: 'bottom'
    }
};

const chart = new ApexCharts(document.querySelector("#multi-series-chart"), options);
chart.render();
```

---

#### Pattern 3: Pie Chart

**BEFORE (Highcharts):**

```javascript
Highcharts.chart('pie-chart', {
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Property Types Distribution'
    },
    series: [{
        name: 'Properties',
        data: [
            ['Residential', 45],
            ['Commercial', 26],
            ['Industrial', 12],
            ['Land', 17]
        ]
    }]
});
```

**AFTER (ApexCharts):**

```javascript
const options = {
    chart: {
        type: 'pie',
        height: 350
    },
    title: {
        text: 'Property Types Distribution'
    },
    labels: ['Residential', 'Commercial', 'Industrial', 'Land'],
    series: [45, 26, 12, 17],
    legend: {
        position: 'bottom'
    }
};

const chart = new ApexCharts(document.querySelector("#pie-chart"), options);
chart.render();
```

---

#### Pattern 4: Chart with Click Events

**BEFORE (Highcharts):**

```javascript
Highcharts.chart('clickable-chart', {
    chart: {
        type: 'column'
    },
    plotOptions: {
        series: {
            cursor: 'pointer',
            point: {
                events: {
                    click: function () {
                        alert('Category: ' + this.category + ', value: ' + this.y);
                    }
                }
            }
        }
    },
    // ... other options
});
```

**AFTER (ApexCharts):**

```javascript
const options = {
    chart: {
        type: 'bar',
        height: 350,
        events: {
            dataPointSelection: (event, chartContext, config) => {
                const category = config.w.globals.labels[config.dataPointIndex];
                const value = config.w.globals.series[config.seriesIndex][config.dataPointIndex];
                alert('Category: ' + category + ', value: ' + value);
            }
        }
    },
    // ... other options
};

const chart = new ApexCharts(document.querySelector("#clickable-chart"), options);
chart.render();
```

---

### Step 1.5: OWL Component Integration

**Complete OWL Component Example for Dashboard:**

```javascript
/** @odoo-module **/

import { Component, onWillStart, onMounted, useRef, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class JupiterDashboardTres extends Component {
    static template = "jupiter_dashboard_tres.Dashboard";

    setup() {
        // Odoo services
        this.orm = useService("orm");
        this.action = useService("action");

        // Chart references
        this.revenueChartRef = useRef("revenueChart");
        this.expenseChartRef = useRef("expenseChart");

        // Chart instances (for cleanup)
        this.charts = [];

        // Data
        this.dashboardData = {};

        // Lifecycle hooks
        onWillStart(async () => {
            await this.loadDashboardData();
        });

        onMounted(() => {
            this.renderCharts();
        });

        onWillUnmount(() => {
            // Cleanup: destroy all chart instances
            this.charts.forEach(chart => {
                if (chart && chart.destroy) {
                    chart.destroy();
                }
            });
        });
    }

    async loadDashboardData() {
        // Load data from backend
        this.dashboardData = await this.orm.call(
            'dashboard.model',  // Your model
            'get_dashboard_data',  // Your method
            []
        );
    }

    renderCharts() {
        this.renderRevenueChart();
        this.renderExpenseChart();
    }

    renderRevenueChart() {
        if (!this.revenueChartRef.el) return;

        const options = {
            chart: {
                type: 'bar',
                height: 350,
                toolbar: { show: true }
            },
            title: {
                text: 'Monthly Revenue',
                align: 'left'
            },
            xaxis: {
                categories: this.dashboardData.months || []
            },
            yaxis: {
                title: { text: 'Revenue ($)' }
            },
            series: [{
                name: 'Revenue',
                data: this.dashboardData.revenue || []
            }],
            colors: ['#008FFB']
        };

        const chart = new ApexCharts(this.revenueChartRef.el, options);
        chart.render();
        this.charts.push(chart);  // Store for cleanup
    }

    renderExpenseChart() {
        if (!this.expenseChartRef.el) return;

        const options = {
            chart: {
                type: 'line',
                height: 350
            },
            title: {
                text: 'Expenses Trend',
                align: 'left'
            },
            xaxis: {
                categories: this.dashboardData.months || []
            },
            series: [{
                name: 'Expenses',
                data: this.dashboardData.expenses || []
            }],
            stroke: {
                curve: 'smooth'
            },
            colors: ['#FF4560']
        };

        const chart = new ApexCharts(this.expenseChartRef.el, options);
        chart.render();
        this.charts.push(chart);  // Store for cleanup
    }

    // Action handlers
    onRefreshDashboard() {
        this.loadDashboardData().then(() => {
            // Destroy old charts
            this.charts.forEach(chart => chart && chart.destroy());
            this.charts = [];

            // Re-render charts
            this.renderCharts();
        });
    }

    onExportData() {
        // Export functionality
        console.log('Exporting dashboard data...');
    }
}

// Register the dashboard
registry.category("actions").add("jupiter_dashboard_tres_action", JupiterDashboardTres);

export default JupiterDashboardTres;
```

**Template (XML):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="jupiter_dashboard_tres.Dashboard" owl="1">
        <div class="o_jupiter_dashboard_tres">
            <div class="dashboard-header">
                <h2>Jupiter Dashboard</h2>
                <div class="dashboard-actions">
                    <button class="btn btn-primary" t-on-click="onRefreshDashboard">
                        <i class="fa fa-refresh"/> Refresh
                    </button>
                    <button class="btn btn-secondary" t-on-click="onExportData">
                        <i class="fa fa-download"/> Export
                    </button>
                </div>
            </div>

            <div class="dashboard-content">
                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <div t-ref="revenueChart"></div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <div t-ref="expenseChart"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </t>
</templates>
```

---

### Step 1.6: Testing Checklist

After migration, verify:

**Visual Testing:**
- [ ] Charts render correctly
- [ ] Colors match or look better
- [ ] Tooltips show on hover
- [ ] Legends display properly
- [ ] Responsive behavior works
- [ ] Animations are smooth

**Functional Testing:**
- [ ] Data loads from backend
- [ ] Click events work (if applicable)
- [ ] Refresh button updates charts
- [ ] Export functionality works
- [ ] Filters update charts
- [ ] No JavaScript console errors

**Performance Testing:**
- [ ] Chart render time < 500ms
- [ ] Smooth scrolling with charts
- [ ] No memory leaks (check with DevTools)
- [ ] Works with large datasets (1000+ points)

**Browser Testing:**
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

---

## 🎯 Part 2: FusionCharts → Chart.js v4 Migration

### Module to Migrate
1. `base_accounting_kit` (8,371 LOC)

---

### Step 2.1: Upgrade Chart.js v2.9 → v4.4 (2 hours)

#### Download Chart.js v4.4

```bash
cd /home/user/Justo-Works/addons_custom/base_accounting_kit/static/lib/

# Backup old Chart.js
mkdir -p backups/
cp Chart.js backups/Chart.js.v2.9.backup
cp Chart.min.js backups/Chart.min.js.v2.9.backup

# Download Chart.js v4.4
wget https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js -O Chart.min.js

# Download non-minified version for development
wget https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js -O Chart.js

# Verify size (should be ~250-300KB)
ls -lh Chart.min.js
```

---

### Step 2.2: Chart.js v2 → v4 Breaking Changes

#### Major Changes to Update

**1. Import/Registration Changes**

```javascript
// v2.9 (OLD)
// Chart was global, no import needed

// v4.4 (NEW)
// Chart is modular, import components
import Chart from 'chart.js/auto';  // Includes all components
// OR
import { Chart, BarController, BarElement, CategoryScale, LinearScale } from 'chart.js';
Chart.register(BarController, BarElement, CategoryScale, LinearScale);
```

**2. Options Structure Changes**

```javascript
// v2.9 (OLD)
const options = {
    scales: {
        yAxes: [{
            ticks: {
                beginAtZero: true
            }
        }],
        xAxes: [{
            type: 'category'
        }]
    }
};

// v4.4 (NEW)
const options = {
    scales: {
        y: {  // No longer 'yAxes' array
            beginAtZero: true,
            ticks: {
                // ticks options
            }
        },
        x: {  // No longer 'xAxes' array
            type: 'category'
        }
    }
};
```

**3. Legend Options**

```javascript
// v2.9 (OLD)
const options = {
    legend: {
        display: true,
        position: 'bottom'
    }
};

// v4.4 (NEW)
const options = {
    plugins: {
        legend: {
            display: true,
            position: 'bottom'
        }
    }
};
```

---

### Step 2.3: Remove FusionCharts (1 hour)

```bash
cd /home/user/Justo-Works/addons_custom/base_accounting_kit/static/lib/

# Backup FusionCharts files
mkdir -p backups/fusioncharts/
cp fusioncharts.js backups/fusioncharts/fusioncharts.js.backup
cp fusioncharts.charts.js backups/fusioncharts/fusioncharts.charts.js.backup

# Remove FusionCharts
rm -f fusioncharts*.js

# Verify removal
ls -la | grep fusion
# Should return nothing
```

---

### Step 2.4: Migrate FusionCharts Code to Chart.js v4

#### Pattern 1: Basic Column Chart

**BEFORE (FusionCharts):**

```javascript
FusionCharts.ready(function(){
    var revenueChart = new FusionCharts({
        type: 'column2d',
        renderAt: 'revenue-chart-container',
        width: '100%',
        height: '400',
        dataFormat: 'json',
        dataSource: {
            "chart": {
                "caption": "Monthly Revenue",
                "xAxisName": "Month",
                "yAxisName": "Revenue",
                "theme": "fusion"
            },
            "data": [
                {"label": "Jan", "value": "29900"},
                {"label": "Feb", "value": "71500"},
                {"label": "Mar", "value": "106400"}
            ]
        }
    });
    revenueChart.render();
});
```

**AFTER (Chart.js v4):**

```javascript
// Get canvas element
const ctx = document.getElementById('revenue-chart-container').getContext('2d');

// Create chart
const revenueChart = new Chart(ctx, {
    type: 'bar',  // 'bar' is vertical column in Chart.js
    data: {
        labels: ['Jan', 'Feb', 'Mar'],
        datasets: [{
            label: 'Monthly Revenue',
            data: [29900, 71500, 106400],
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: 'Monthly Revenue'
            },
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Revenue'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Month'
                }
            }
        }
    }
});
```

---

#### Pattern 2: Multi-Series Line Chart

**BEFORE (FusionCharts):**

```javascript
var chartObj = new FusionCharts({
    type: 'msline',
    renderAt: 'chart-container',
    width: '100%',
    height: '400',
    dataFormat: 'json',
    dataSource: {
        "chart": {
            "caption": "Revenue vs Expenses",
            "showValues": "0",
            "theme": "fusion"
        },
        "categories": [{
            "category": [
                {"label": "Q1"},
                {"label": "Q2"},
                {"label": "Q3"},
                {"label": "Q4"}
            ]
        }],
        "dataset": [{
            "seriesname": "Revenue",
            "data": [
                {"value": "100000"},
                {"value": "120000"},
                {"value": "140000"},
                {"value": "160000"}
            ]
        }, {
            "seriesname": "Expenses",
            "data": [
                {"value": "80000"},
                {"value": "90000"},
                {"value": "95000"},
                {"value": "100000"}
            ]
        }]
    }
});
```

**AFTER (Chart.js v4):**

```javascript
const ctx = document.getElementById('chart-container').getContext('2d');

const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        datasets: [{
            label: 'Revenue',
            data: [100000, 120000, 140000, 160000],
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.1  // Smooth line
        }, {
            label: 'Expenses',
            data: [80000, 90000, 95000, 100000],
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: 'Revenue vs Expenses'
            },
            legend: {
                display: true,
                position: 'bottom'
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
```

---

#### Pattern 3: Pie Chart

**BEFORE (FusionCharts):**

```javascript
var pieChart = new FusionCharts({
    type: 'pie2d',
    renderAt: 'pie-chart-container',
    width: '100%',
    height: '400',
    dataFormat: 'json',
    dataSource: {
        "chart": {
            "caption": "Assets Distribution",
            "theme": "fusion"
        },
        "data": [
            {"label": "Buildings", "value": "45"},
            {"label": "Equipment", "value": "25"},
            {"label": "Vehicles", "value": "15"},
            {"label": "Other", "value": "15"}
        ]
    }
});
```

**AFTER (Chart.js v4):**

```javascript
const ctx = document.getElementById('pie-chart-container').getContext('2d');

const pieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Buildings', 'Equipment', 'Vehicles', 'Other'],
        datasets: [{
            data: [45, 25, 15, 15],
            backgroundColor: [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: 'Assets Distribution'
            },
            legend: {
                display: true,
                position: 'right'
            }
        }
    }
});
```

---

### Step 2.5: Update Manifest for Chart.js v4

**File:** `addons_custom/base_accounting_kit/__manifest__.py`

```python
{
    'name': 'Base Accounting Kit',
    'version': '18.0.2.2.2',  # Update version
    'assets': {
        'web.assets_backend': [
            # Remove FusionCharts
            # 'base_accounting_kit/static/lib/fusioncharts.js',
            # 'base_accounting_kit/static/lib/fusioncharts.charts.js',

            # Update Chart.js reference
            'base_accounting_kit/static/lib/Chart.min.js',  # v4.4 now

            # Dashboard scripts
            'base_accounting_kit/static/src/js/account_dashboard.js',
            'base_accounting_kit/static/src/js/account_asset.js',
            # ... other scripts
        ],
    },
}
```

---

### Step 2.6: Complete OWL Component Example (Accounting Dashboard)

```javascript
/** @odoo-module **/

import { Component, onWillStart, onMounted, useRef, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class AccountingDashboard extends Component {
    static template = "base_accounting_kit.Dashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        // Chart references
        this.revenueChartRef = useRef("revenueChart");
        this.expenseChartRef = useRef("expenseChart");
        this.assetChartRef = useRef("assetChart");

        // Store chart instances for cleanup
        this.chartInstances = [];

        // Dashboard data
        this.dashboardData = {
            revenue: [],
            expenses: [],
            assets: [],
            months: []
        };

        onWillStart(async () => {
            await this.loadDashboardData();
        });

        onMounted(() => {
            this.renderAllCharts();
        });

        onWillUnmount(() => {
            // Cleanup: destroy all chart instances
            this.chartInstances.forEach(chart => {
                if (chart && typeof chart.destroy === 'function') {
                    chart.destroy();
                }
            });
            this.chartInstances = [];
        });
    }

    async loadDashboardData() {
        const data = await this.orm.call(
            'account.dashboard',
            'get_dashboard_data',
            []
        );

        this.dashboardData = {
            revenue: data.revenue || [],
            expenses: data.expenses || [],
            assets: data.assets || [],
            months: data.months || []
        };
    }

    renderAllCharts() {
        this.renderRevenueChart();
        this.renderExpenseChart();
        this.renderAssetChart();
    }

    renderRevenueChart() {
        if (!this.revenueChartRef.el) return;

        const ctx = this.revenueChartRef.el.getContext('2d');

        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: this.dashboardData.months,
                datasets: [{
                    label: 'Revenue',
                    data: this.dashboardData.revenue,
                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Monthly Revenue'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });

        this.chartInstances.push(chart);
    }

    renderExpenseChart() {
        if (!this.expenseChartRef.el) return;

        const ctx = this.expenseChartRef.el.getContext('2d');

        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.dashboardData.months,
                datasets: [{
                    label: 'Expenses',
                    data: this.dashboardData.expenses,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Monthly Expenses'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        this.chartInstances.push(chart);
    }

    renderAssetChart() {
        if (!this.assetChartRef.el) return;

        const ctx = this.assetChartRef.el.getContext('2d');

        const chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: this.dashboardData.assets.labels || [],
                datasets: [{
                    data: this.dashboardData.assets.data || [],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Assets Distribution'
                    },
                    legend: {
                        position: 'right'
                    }
                }
            }
        });

        this.chartInstances.push(chart);
    }

    async onRefreshDashboard() {
        // Destroy existing charts
        this.chartInstances.forEach(chart => chart && chart.destroy());
        this.chartInstances = [];

        // Reload data
        await this.loadDashboardData();

        // Re-render charts
        this.renderAllCharts();
    }
}

registry.category("actions").add("accounting_dashboard", AccountingDashboard);

export default AccountingDashboard;
```

**Template:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="base_accounting_kit.Dashboard" owl="1">
        <div class="o_accounting_dashboard">
            <div class="dashboard-header">
                <h2>Accounting Dashboard</h2>
                <button class="btn btn-primary" t-on-click="onRefreshDashboard">
                    <i class="fa fa-refresh"/> Refresh
                </button>
            </div>

            <div class="dashboard-content">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <div class="card">
                            <div class="card-body" style="height: 400px;">
                                <canvas t-ref="revenueChart"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-3">
                        <div class="card">
                            <div class="card-body" style="height: 400px;">
                                <canvas t-ref="expenseChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <div class="card">
                            <div class="card-body" style="height: 400px;">
                                <canvas t-ref="assetChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </t>
</templates>
```

---

## ✅ Final Testing Checklist

### Part 1: ApexCharts Migration

**jupiter_dashboard_tres:**
- [ ] Dashboard loads without errors
- [ ] All charts render correctly
- [ ] Data displays accurately
- [ ] Tooltips work
- [ ] Export functionality works
- [ ] Responsive on mobile
- [ ] No console errors

**jupiter_dashboard_optima:**
- [ ] Same as above
- [ ] Dashboard settings work
- [ ] Configuration persists

### Part 2: Chart.js v4 Migration

**base_accounting_kit:**
- [ ] All accounting charts render
- [ ] Revenue chart works
- [ ] Expense chart works
- [ ] Asset distribution chart works
- [ ] No FusionCharts references remain
- [ ] Dashboard refresh works
- [ ] No console errors
- [ ] Performance is good

---

## 📊 Migration Metrics

Track your progress:

```
Module: jupiter_dashboard_tres
- Charts migrated: ___ / ___
- Tests passing: ___ / ___
- Time spent: ___ hours
- Status: [ ] Complete

Module: jupiter_dashboard_optima
- Charts migrated: ___ / ___
- Tests passing: ___ / ___
- Time spent: ___ hours
- Status: [ ] Complete

Module: base_accounting_kit
- Charts migrated: ___ / ___
- FusionCharts removed: [ ] Yes / [ ] No
- Chart.js upgraded: [ ] v4.4
- Tests passing: ___ / ___
- Time spent: ___ hours
- Status: [ ] Complete

TOTAL TIME: ___ hours (Target: 64 hours)
COST SAVINGS: $5,747 over 5 years ✅
```

---

## 🔧 Troubleshooting

### Common Issues

**Issue 1: "Chart is not defined"**
```javascript
// Problem: Chart.js not loaded
// Solution: Check manifest.py includes Chart.min.js
// Or add to template:
<script src="/base_accounting_kit/static/lib/Chart.min.js"></script>
```

**Issue 2: "Cannot read property 'getContext' of null"**
```javascript
// Problem: Element not found or not mounted yet
// Solution: Use onMounted hook and check element exists
onMounted(() => {
    if (this.chartRef.el) {
        this.renderChart();
    }
});
```

**Issue 3: Chart not responsive**
```javascript
// Problem: Canvas doesn't resize
// Solution: Set responsive options
options: {
    responsive: true,
    maintainAspectRatio: false
}
```

**Issue 4: Memory leak with charts**
```javascript
// Problem: Charts not destroyed properly
// Solution: Always destroy in onWillUnmount
onWillUnmount(() => {
    this.charts.forEach(chart => chart && chart.destroy());
});
```

---

**Migration Status:** Ready to begin
**Estimated Completion:** 8 days
**Cost Savings:** $5,747 over 5 years

---

**Last Updated:** 2025-11-09
