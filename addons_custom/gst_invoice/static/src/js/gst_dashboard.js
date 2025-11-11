/** @odoo-module **/

/**
 * GST Dashboard Graph Widget for Odoo 18
 * Chart visualization using NVD3 (line and bar charts)
 *
 * Migrated from Odoo 15 to Odoo 18 OWL framework
 */

import { Component, onMounted, onWillUnmount, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { loadJS, loadCSS } from "@web/core/assets";

export class GstDashboardGraph extends Component {
    static template = "gst_invoice.GstDashboardGraphTemplate";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.svgRef = useRef("svg");
        this.chart = null;

        // Parse field value
        this.graphType = this.props.record.activeFields[this.props.name]?.options?.graph_type || 'line';
        this.data = this.props.record.data[this.props.name]
            ? JSON.parse(this.props.record.data[this.props.name])
            : [];

        onMounted(async () => {
            await this.loadLibraries();
            this.displayGraph();
        });

        onWillUnmount(() => {
            if (window.nv && window.nv.utils) {
                window.nv.utils.offWindowResize(this.onResize.bind(this));
            }
        });
    }

    /**
     * Load NVD3 libraries (CSS and JS)
     */
    async loadLibraries() {
        await loadCSS('/web/static/lib/nvd3/nv.d3.css');
        await loadJS('/web/static/lib/nvd3/d3.v3.js');
        await loadJS('/web/static/lib/nvd3/nv.d3.js');
        await loadJS('/web/static/src/js/libs/nvd3.js');
    }

    /**
     * Display the chart based on graph type
     */
    displayGraph() {
        const self = this;

        if (!window.nv) {
            console.error("NVD3 library not loaded");
            return;
        }

        window.nv.addGraph(() => {
            const svg = self.svgRef.el;

            switch (self.graphType) {
                case "line":
                    svg.classList.add('o_graph_linechart');
                    self.chart = window.nv.models.lineChart();
                    self.chart.forceY([0]);
                    self.chart.options({
                        x: (d, u) => u,
                        margin: {
                            left: 0,
                            right: 0,
                            top: 0,
                            bottom: 0
                        },
                        showYAxis: false,
                        showLegend: false,
                    });

                    self.chart.xAxis.tickFormat((d) => {
                        let label = '';
                        self.data.forEach((v) => {
                            if (v.values[d] && v.values[d].x) {
                                label = v.values[d].x;
                            }
                        });
                        return label;
                    });

                    self.chart.yAxis.tickFormat(window.d3.format(',.2f'));
                    break;

                case "bar":
                    svg.classList.add('o_graph_barchart');
                    self.chart = window.nv.models.discreteBarChart()
                        .x((d) => d.label)
                        .y((d) => d.value)
                        .showValues(false)
                        .showYAxis(false)
                        .margin({
                            left: 0,
                            right: 0,
                            top: 0,
                            bottom: 40
                        });

                    self.chart.xAxis.axisLabel(self.data[0]?.title || '');
                    self.chart.yAxis.tickFormat(window.d3.format(',.2f'));
                    break;
            }

            window.d3.select(svg)
                .datum(self.data)
                .transition()
                .duration(1200)
                .call(self.chart);

            self.customizeChart();

            window.nv.utils.windowResize(self.onResize.bind(self));
        });
    }

    /**
     * Handle window resize
     */
    onResize() {
        if (this.chart) {
            this.chart.update();
            this.customizeChart();
        }
    }

    /**
     * Customize chart appearance
     */
    customizeChart() {
        if (this.graphType === 'bar' && this.data[0]) {
            // Add classes related to time on each bar of the bar chart
            const barClasses = this.data[0].values.map(v => v.type);

            const bars = this.svgRef.el.querySelectorAll('.nv-bar');
            bars.forEach((bar, index) => {
                if (barClasses[index]) {
                    bar.classList.add(barClasses[index]);
                }
            });
        }
    }
}

// Register field widget
registry.category("fields").add("gst_dashboard_graph", GstDashboardGraph);

/*
 * MIGRATION NOTES:
 * ================
 *
 * Changes from Odoo 15:
 * - odoo.define() → ES6 module with @odoo-module
 * - AbstractField → OWL Component
 * - field_registry → registry.category("fields")
 * - cssLibs/jsLibs → loadJS/loadCSS in setup
 * - start() → onMounted() lifecycle hook
 * - destroy() → onWillUnmount() lifecycle hook
 * - this.$el → this.svgRef.el (useRef pattern)
 * - jQuery selectors → native DOM queries
 * - Added standardFieldProps for proper field integration
 * - Arrow functions for cleaner syntax
 * - Proper async/await for library loading
 *
 * Dependencies:
 * - NVD3 library (preserved from Odoo 15)
 * - D3.js v3 (preserved from Odoo 15)
 * - /web/static/lib/nvd3/* (core Odoo assets)
 *
 * Template Required:
 * - gst_invoice.GstDashboardGraphTemplate (simple SVG container)
 *   Example:
 *   <t t-name="gst_invoice.GstDashboardGraphTemplate">
 *       <svg t-ref="svg"></svg>
 *   </t>
 *
 * Usage in Views:
 * - Field type: gst_dashboard_graph
 * - Options: graph_type (line or bar)
 *
 * Testing Checklist:
 * - [ ] Line chart renders correctly
 * - [ ] Bar chart renders correctly
 * - [ ] Chart updates on window resize
 * - [ ] Data formatting displays properly
 * - [ ] No console errors on mount/unmount
 * - [ ] Works with different data sets
 * - [ ] Responsive behavior maintained
 */
