/** @odoo-module **/

/**
 * Jupiter Dashboard II - Bookings, Registrations, Collections Dashboard
 * Migrated to Odoo 18 OWL framework
 *
 * Features:
 * - ApexCharts integration (bar and line charts)
 * - Real-time booking and registration metrics
 * - Collection and billing tracking
 * - CP (Channel Partner) analytics
 * - Horizontal scrollable dashboard with drag support
 */

import { Component, onMounted, onWillStart, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { loadJS } from "@web/core/assets";

export class JupiterDashboardDeux extends Component {
    static template = "JupiterDashboardDeux";

    setup() {
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.containerRef = useRef("horizontal_scroll_container");

        onWillStart(async () => {
            // Load ApexCharts library
            await loadJS("/web/static/lib/apexcharts/apexcharts.js");
        });

        onMounted(async () => {
            await this.renderElement();
            this.setupHorizontalScroll();
        });
    }

    /**
     * Link to list view with domain filter
     */
    async linkToList(ev) {
        const target = ev.currentTarget;
        const domain = target.getAttribute('domain');
        const model = target.getAttribute('model');
        const name = target.getAttribute('name');

        const result = await this.rpc('/jupiter_dashboard_deux/call_list_view', {
            domain: domain,
            model: model,
            name: name
        });

        this.action.doAction(result);
    }

    /**
     * Link to report with attributes
     */
    async linkToReport(ev) {
        const target = ev.currentTarget;
        const reportAttrStr = target.getAttribute('report_attr').replace(/'/g, '"');
        const reportAttr = JSON.parse(reportAttrStr);

        // Handle consolidate boolean conversion
        if ('consolidate' in reportAttr) {
            reportAttr['consolidate'] = reportAttr['consolidate'] !== 'False';
        }

        const model = target.getAttribute('model');

        const result = await this.rpc('/jupiter_dashboard_deux/call_report', {
            report_attr: reportAttr,
            model: model
        });

        this.action.doAction(result);
    }

    /**
     * Render CP Count Chart (Bar Chart)
     */
    applyCpCountChart(result) {
        const options = {
            series: [{
                name: 'New CPs Added',
                data: result['create_cps_list'],
            }, {
                name: 'Active CPs',
                data: result['active_cps_list'],
            }],
            chart: {
                fontFamily: 'Poppins, sans-serif',
                type: 'bar',
                height: 300,
                zoom: {
                    enabled: false
                },
                toolbar: {
                    show: false
                }
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '55%',
                    endingShape: 'rounded'
                },
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                show: true,
                width: 2,
                colors: ['transparent']
            },
            xaxis: {
                categories: result['months'],
            },
            yaxis: {
                title: {
                    text: 'Count'
                }
            },
            fill: {
                opacity: 1
            },
        };

        const chartElement = document.querySelector("#cp_count_chart");
        if (chartElement) {
            chartElement.innerHTML = '';
            const chart = new ApexCharts(chartElement, options);
            chart.render();
        }
    }

    /**
     * Render CP Booking Chart (Line Chart)
     */
    applyCpBookingChart(result) {
        const options = {
            series: [{
                name: "Booking",
                data: result['bookings']
            }],
            chart: {
                fontFamily: 'Poppins, sans-serif',
                height: 320,
                type: 'line',
                dropShadow: {
                    enabled: true,
                    color: '#000',
                    top: 18,
                    left: 7,
                    blur: 10,
                    opacity: 0.2
                },
                zoom: {
                    enabled: false
                },
                toolbar: {
                    show: false
                }
            },
            colors: ['#ff006e'],
            dataLabels: {
                enabled: true,
                background: {
                    enabled: true,
                    foreColor: '#fff',
                    padding: 3,
                    borderRadius: 5,
                    borderWidth: 0,
                    borderColor: '#fff',
                    opacity: 0.9,
                    dropShadow: {
                        enabled: true,
                        top: 1,
                        left: 1,
                        blur: 1,
                        color: '#000',
                        opacity: 0.45
                    }
                },
            },
            stroke: {
                curve: 'smooth'
            },
            title: {
                text: "CP's Booking Units- Last 6 Months",
                align: 'left'
            },
            grid: {
                borderColor: '#e7e7e7',
                row: {
                    colors: ['#f3f3f3', 'transparent'],
                    opacity: 0.5
                },
            },
            markers: {
                size: 1
            },
            xaxis: {
                categories: result['months'],
                title: {
                    text: 'Month'
                }
            },
            yaxis: {
                title: {
                    text: 'Count'
                },
            },
            legend: {
                position: 'top',
                horizontalAlign: 'right',
                floating: true,
                offsetY: -25,
                offsetX: -5
            }
        };

        const chartElement = document.querySelector("#cp_chart");
        if (chartElement) {
            chartElement.innerHTML = '';
            const chart = new ApexCharts(chartElement, options);
            chart.render();
        }
    }

    /**
     * Main render function - loads all dashboard data
     */
    async renderElement() {
        // Load booking and registration data
        const bookingData = await this.rpc('/jupiter_dashboard_deux/bookings_registrations', {});

        // Update all booking counts and values
        this.updateElement('#today_booking_count', bookingData['today_booking_count']);
        this.updateElement('#week_booking_count', bookingData['week_booking_count']);
        this.updateElement('#month_booking_count', bookingData['month_booking_count']);
        this.updateElement('#year_booking_count', bookingData['year_booking_count']);
        this.updateElement('#quarter_booking_count', bookingData['quarter_booking_count']);
        this.updateElement('#half_booking_count', bookingData['half_booking_count']);

        this.updateElement('#today_booking_value', bookingData['today_booking_value']);
        this.updateElement('#week_booking_value', bookingData['week_booking_value']);
        this.updateElement('#month_booking_value', bookingData['month_booking_value']);
        this.updateElement('#year_booking_value', bookingData['year_booking_value']);
        this.updateElement('#quarter_booking_value', bookingData['quarter_booking_value']);
        this.updateElement('#half_booking_value', bookingData['half_booking_value']);

        // Update registration counts and values
        this.updateElement('#today_registration_count', bookingData['today_registration_count']);
        this.updateElement('#week_registration_count', bookingData['week_registration_count']);
        this.updateElement('#month_registration_count', bookingData['month_registration_count']);
        this.updateElement('#year_registration_count', bookingData['year_registration_count']);
        this.updateElement('#quarter_registration_count', bookingData['quarter_registration_count']);
        this.updateElement('#half_registration_count', bookingData['half_registration_count']);

        this.updateElement('#today_registration_value', bookingData['today_registration_value']);
        this.updateElement('#week_registration_value', bookingData['week_registration_value']);
        this.updateElement('#month_registration_value', bookingData['month_registration_value']);
        this.updateElement('#year_registration_value', bookingData['year_registration_value']);
        this.updateElement('#quarter_registration_value', bookingData['quarter_registration_value']);
        this.updateElement('#half_registration_value', bookingData['half_registration_value']);

        // Set report attributes for links
        this.setAttribute('#today_booking_link', 'report_attr', bookingData['today_booking_attrs']);
        this.setAttribute('#week_booking_link', 'report_attr', bookingData['week_booking_attrs']);
        this.setAttribute('#month_booking_link', 'report_attr', bookingData['month_booking_attrs']);
        this.setAttribute('#year_booking_link', 'report_attr', bookingData['year_booking_attrs']);
        this.setAttribute('#quarter_booking_link', 'report_attr', bookingData['quarter_booking_attrs']);
        this.setAttribute('#half_booking_link', 'report_attr', bookingData['half_booking_attrs']);

        this.setAttributeAll('.today_registration_link', 'report_attr', bookingData['today_registration_attrs']);
        this.setAttributeAll('.week_registration_link', 'report_attr', bookingData['week_registration_attrs']);
        this.setAttributeAll('.month_registration_link', 'report_attr', bookingData['month_registration_attrs']);
        this.setAttributeAll('.year_registration_link', 'report_attr', bookingData['year_registration_attrs']);
        this.setAttributeAll('.quarter_registration_link', 'report_attr', bookingData['quarter_registration_attrs']);
        this.setAttributeAll('.half_registration_link', 'report_attr', bookingData['half_registration_attrs']);

        // Update cancelled bookings
        this.updateElement('#today_booking_cancelled_count', bookingData['today_booking_cancelled_count']);
        this.updateElement('#week_booking_cancelled_count', bookingData['week_booking_cancelled_count']);
        this.updateElement('#month_booking_cancelled_count', bookingData['month_booking_cancelled_count']);
        this.updateElement('#year_booking_cancelled_count', bookingData['year_booking_cancelled_count']);
        this.updateElement('#quarter_booking_cancelled_count', bookingData['quarter_booking_cancelled_count']);
        this.updateElement('#half_booking_cancelled_count', bookingData['half_booking_cancelled_count']);

        this.updateElement('#today_booking_cancelled_value', bookingData['today_booking_cancelled_value']);
        this.updateElement('#week_booking_cancelled_value', bookingData['week_booking_cancelled_value']);
        this.updateElement('#month_booking_cancelled_value', bookingData['month_booking_cancelled_value']);
        this.updateElement('#year_booking_cancelled_value', bookingData['year_booking_cancelled_value']);
        this.updateElement('#quarter_booking_cancelled_value', bookingData['quarter_booking_cancelled_value']);
        this.updateElement('#half_booking_cancelled_value', bookingData['half_booking_cancelled_value']);

        this.setAttribute('#today_booking_cancelled_link', 'report_attr', bookingData['today_booking_cancelled_attrs']);
        this.setAttribute('#week_booking_cancelled_link', 'report_attr', bookingData['week_booking_cancelled_attrs']);
        this.setAttribute('#month_booking_cancelled_link', 'report_attr', bookingData['month_booking_cancelled_attrs']);
        this.setAttribute('#year_booking_cancelled_link', 'report_attr', bookingData['year_booking_cancelled_attrs']);
        this.setAttribute('#quarter_booking_cancelled_link', 'report_attr', bookingData['quarter_booking_cancelled_attrs']);
        this.setAttribute('#half_booking_cancelled_link', 'report_attr', bookingData['half_booking_cancelled_attrs']);

        // Update labels
        this.updateElementAll('.quarter_label', bookingData['quarter_label']);
        this.updateElementAll('.half_label', bookingData['half_label']);
        this.updateElementAll('.year_label', bookingData['year_label']);

        // Update CP booking counts
        this.updateElement('#today_booking_cp_count', bookingData['today_booking_cp_count']);
        this.updateElement('#week_booking_cp_count', bookingData['week_booking_cp_count']);
        this.updateElement('#month_booking_cp_count', bookingData['month_booking_cp_count']);
        this.updateElement('#year_booking_cp_count', bookingData['year_booking_cp_count']);
        this.updateElement('#quarter_booking_cp_count', bookingData['quarter_booking_cp_count']);
        this.updateElement('#half_booking_cp_count', bookingData['half_booking_cp_count']);

        // Set CP domains
        this.setAttribute('#today_booking_cp_domain', 'domain', bookingData['today_booking_cp_domain']);
        this.setAttribute('#week_booking_cp_domain', 'domain', bookingData['week_booking_cp_domain']);
        this.setAttribute('#month_booking_cp_domain', 'domain', bookingData['month_booking_cp_domain']);
        this.setAttribute('#quarter_booking_cp_domain', 'domain', bookingData['quarter_booking_cp_domain']);
        this.setAttribute('#half_booking_cp_domain', 'domain', bookingData['half_booking_cp_domain']);
        this.setAttribute('#year_booking_cp_domain', 'domain', bookingData['year_booking_cp_domain']);

        // Update direct bookings
        this.updateElement('#today_direct', bookingData['today_direct']);
        this.updateElement('#week_direct', bookingData['week_direct']);
        this.updateElement('#month_direct', bookingData['month_direct']);
        this.updateElement('#year_direct', bookingData['year_direct']);
        this.updateElement('#quarter_direct', bookingData['quarter_direct']);
        this.updateElement('#half_direct', bookingData['half_direct']);

        this.setAttribute('#today_direct_domain', 'domain', bookingData['today_direct_domain']);
        this.setAttribute('#week_direct_domain', 'domain', bookingData['week_direct_domain']);
        this.setAttribute('#month_direct_domain', 'domain', bookingData['month_direct_domain']);
        this.setAttribute('#quarter_direct_domain', 'domain', bookingData['quarter_direct_domain']);
        this.setAttribute('#half_direct_domain', 'domain', bookingData['half_direct_domain']);
        this.setAttribute('#year_direct_domain', 'domain', bookingData['year_direct_domain']);

        // Update average values
        this.updateElement('#today_average_av', bookingData['today_average_av']);
        this.updateElement('#week_average_av', bookingData['week_average_av']);
        this.updateElement('#month_average_av', bookingData['month_average_av']);
        this.updateElement('#quarter_average_av', bookingData['quarter_average_av']);
        this.updateElement('#half_average_av', bookingData['half_average_av']);
        this.updateElement('#year_average_av', bookingData['year_average_av']);

        // Load collections and billings
        const collectionData = await this.rpc('/jupiter_dashboard_deux/collections_billings', {});

        this.updateElement('#today_collection', collectionData['today_collection']);
        this.updateElement('#week_collection', collectionData['week_collection']);
        this.updateElement('#month_collection', collectionData['month_collection']);
        this.updateElement('#year_collection', collectionData['year_collection']);
        this.updateElement('#quarter_collection', collectionData['quarter_collection']);
        this.updateElement('#half_collection', collectionData['half_collection']);

        this.updateElement('#today_billing', collectionData['today_billing']);
        this.updateElement('#week_billing', collectionData['week_billing']);
        this.updateElement('#month_billing', collectionData['month_billing']);
        this.updateElement('#year_billing', collectionData['year_billing']);
        this.updateElement('#quarter_billing', collectionData['quarter_billing']);
        this.updateElement('#half_billing', collectionData['half_billing']);

        this.setAttribute('#today_billing_attrs', 'report_attr', collectionData['today_billing_attrs']);
        this.setAttribute('#week_billing_attrs', 'report_attr', collectionData['week_billing_attrs']);
        this.setAttribute('#month_billing_attrs', 'report_attr', collectionData['month_billing_attrs']);
        this.setAttribute('#quarter_billing_attrs', 'report_attr', collectionData['quarter_billing_attrs']);
        this.setAttribute('#half_billing_attrs', 'report_attr', collectionData['half_billing_attrs']);
        this.setAttribute('#year_billing_attrs', 'report_attr', collectionData['year_billing_attrs']);

        this.setAttribute('#today_collection_attr', 'domain', collectionData['today_collection_domain']);
        this.setAttribute('#week_collection_attr', 'domain', collectionData['week_collection_domain']);
        this.setAttribute('#month_collection_attr', 'domain', collectionData['month_collection_domain']);
        this.setAttribute('#quarter_collection_attr', 'domain', collectionData['quarter_collection_domain']);
        this.setAttribute('#half_collection_attr', 'domain', collectionData['half_collection_domain']);
        this.setAttribute('#year_collection_attr', 'domain', collectionData['year_collection_domain']);

        // Load and render CP booking chart
        const cpBookingData = await this.rpc('/jupiter_dashboard_deux/get_last_6_month_cp_booking', {});
        this.applyCpBookingChart(cpBookingData);

        // Load and render CP count data
        const cpCountData = await this.rpc('/jupiter_dashboard_deux/get_cp_count', {});

        this.updateElement('#month_cps', cpCountData['month_cps']);
        this.updateElement('#quarter_cps', cpCountData['quarter_cps']);
        this.updateElement('#half_cps', cpCountData['half_cps']);
        this.updateElement('#year_cps', cpCountData['year_cps']);

        this.updateElement('#month_cps_active', cpCountData['month_cps_active']);
        this.updateElement('#quarter_cps_active', cpCountData['quarter_cps_active']);
        this.updateElement('#half_cps_active', cpCountData['half_cps_active']);
        this.updateElement('#year_cps_active', cpCountData['year_cps_active']);

        this.setAttribute('#month_cp_domain', 'domain', cpCountData['month_cp_domain']);
        this.setAttribute('#quarter_cp_domain', 'domain', cpCountData['quarter_cp_domain']);
        this.setAttribute('#half_cp_domain', 'domain', cpCountData['half_cp_domain']);
        this.setAttribute('#year_cp_domain', 'domain', cpCountData['year_cp_domain']);

        this.setAttribute('#month_cp_active_domain', 'domain', cpCountData['month_cp_active_domain']);
        this.setAttribute('#quarter_cp_active_domain', 'domain', cpCountData['quarter_cp_active_domain']);
        this.setAttribute('#half_cp_active_domain', 'domain', cpCountData['half_cp_active_domain']);
        this.setAttribute('#year_cp_active_domain', 'domain', cpCountData['year_cp_active_domain']);

        this.applyCpCountChart(cpCountData);
    }

    /**
     * Setup horizontal scroll with drag and arrow controls
     */
    setupHorizontalScroll() {
        try {
            const container = document.getElementById('horizontal-scroll-container');
            if (!container) return;

            let isDragging = false;
            let startX;
            let scrollLeft;

            const leftArrow = document.querySelector('.left-arrow');
            const rightArrow = document.querySelector('.right-arrow');

            const singleItem = document.querySelector('.flex-scroll-item');
            const itemWidth = singleItem ? singleItem.offsetWidth + 10 : 1000;

            // Shift + Mouse wheel scroll
            container.addEventListener('wheel', (e) => {
                if (e.shiftKey) {
                    e.preventDefault();
                    smoothScroll(container.scrollLeft + e.deltaY * 2);
                }
            });

            // Arrow click events
            if (leftArrow) {
                leftArrow.addEventListener('click', () => {
                    smoothScroll(container.scrollLeft - itemWidth);
                    updateArrowVisibility();
                });
            }

            if (rightArrow) {
                rightArrow.addEventListener('click', () => {
                    smoothScroll(container.scrollLeft + itemWidth);
                    updateArrowVisibility();
                });
            }

            // Mouse drag events
            container.addEventListener('mousedown', (e) => {
                isDragging = true;
                container.classList.add('active', 'grabbing');
                startX = e.pageX - container.offsetLeft;
                scrollLeft = container.scrollLeft;
            });

            container.addEventListener('mouseup', () => {
                isDragging = false;
                container.classList.remove('active', 'grabbing');
                updateArrowVisibility();
            });

            container.addEventListener('mousemove', (e) => {
                if (!isDragging) return;
                e.preventDefault();
                const x = e.pageX - container.offsetLeft;
                const walk = (x - startX) * 3;
                smoothScroll(scrollLeft - walk);
            });

            container.addEventListener('mouseleave', () => {
                if (isDragging) {
                    isDragging = false;
                    container.classList.remove('active', 'grabbing');
                    updateArrowVisibility();
                }
            });

            // Smooth scroll function
            function smoothScroll(targetX) {
                let start = container.scrollLeft;
                let change = targetX - start;
                let currentTime = 0;
                const increment = 20;
                const duration = 300;

                function animateScroll() {
                    currentTime += increment;
                    const val = easeInOutQuad(currentTime, start, change, duration);
                    container.scrollLeft = val;
                    if (currentTime < duration) {
                        requestAnimationFrame(animateScroll);
                    } else {
                        updateArrowVisibility();
                    }
                }
                animateScroll();
            }

            // Easing function
            function easeInOutQuad(t, b, c, d) {
                t /= d / 2;
                if (t < 1) return c / 2 * t * t + b;
                t--;
                return -c / 2 * (t * (t - 2) - 1) + b;
            }

            // Update arrow visibility
            function updateArrowVisibility() {
                if (leftArrow) {
                    leftArrow.style.display = container.scrollLeft <= 0 ? 'none' : 'block';
                }
                if (rightArrow) {
                    rightArrow.style.display =
                        container.scrollLeft + container.clientWidth >= container.scrollWidth ? 'none' : 'block';
                }
            }

            updateArrowVisibility();
        } catch (e) {
            console.error("Error setting up horizontal scroll:", e);
        }
    }

    /**
     * Helper: Update element content
     */
    updateElement(selector, content) {
        const el = document.querySelector(selector);
        if (el) el.textContent = content;
    }

    /**
     * Helper: Update all matching elements
     */
    updateElementAll(selector, content) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => el.textContent = content);
    }

    /**
     * Helper: Set attribute on element
     */
    setAttribute(selector, attr, value) {
        const el = document.querySelector(selector);
        if (el) el.setAttribute(attr, value);
    }

    /**
     * Helper: Set attribute on all matching elements
     */
    setAttributeAll(selector, attr, value) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => el.setAttribute(attr, value));
    }
}

// Register as client action
registry.category("actions").add("jupiter_dashboard_deux", JupiterDashboardDeux);

/*
 * MIGRATION NOTES:
 * ================
 *
 * Changes from Odoo 15:
 * - odoo.define() → ES6 module with @odoo-module
 * - AbstractAction → OWL Component
 * - core.action_registry → registry.category("actions")
 * - ajax.jsonRpc() → useService("rpc")
 * - renderElement() → onMounted() lifecycle hook
 * - this.do_action() → this.action.doAction()
 * - jQuery $ → Native DOM queries (querySelector, querySelectorAll)
 * - Preserved ApexCharts library (third-party)
 * - Kept complex scroll/drag logic intact
 * - Added helper methods for DOM manipulation
 *
 * Dependencies:
 * - ApexCharts (/web/static/lib/apexcharts/apexcharts.js)
 * - OWL framework
 * - RPC and Action services
 *
 * Template Required:
 * - JupiterDashboardDeux (static/src/xml/template.xml)
 *
 * Testing Checklist:
 * - [ ] Dashboard loads without errors
 * - [ ] All metrics display correctly
 * - [ ] ApexCharts render properly
 * - [ ] Click events work (report links, list view links)
 * - [ ] Horizontal scroll with drag works
 * - [ ] Arrow navigation works
 * - [ ] Shift + mouse wheel scrolling works
 * - [ ] All RPC calls complete successfully
 * - [ ] Data updates reflect in real-time
 */
