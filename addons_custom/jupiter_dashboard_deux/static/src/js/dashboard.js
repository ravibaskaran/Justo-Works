/** @odoo-module **/
// Migrated to Odoo 18 OWL framework - 2025-11-10
// Original: Odoo 15 AbstractAction with custom scroll functionality
// Changes:
// - odoo.define → @odoo-module
// - AbstractAction → OWL Component
// - ajax.jsonRpc → useService("rpc")
// - jQuery → Native DOM and OWL refs
// - Custom scroll logic adapted for OWL
// - Event handlers via addEventListener
// - ApexCharts integration preserved

import { Component, onMounted, onWillUnmount, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class JupiterDashboardDeux extends Component {
    static template = "JupiterDashboardDeux";

    setup() {
        this.rpc = useService("rpc");
        this.action = useService("action");

        // Chart refs
        this.cpCountChartRef = useRef("cpCountChart");
        this.cpChartRef = useRef("cpChart");
        this.scrollContainerRef = useRef("scrollContainer");

        // Store chart instances for cleanup
        this.charts = {};

        // Store scroll state
        this.scrollState = {
            isDragging: false,
            startX: 0,
            scrollLeft: 0
        };

        // Store event listeners for cleanup
        this.eventListeners = [];

        onMounted(() => this.onMounted());
        onWillUnmount(() => this.onWillUnmount());
    }

    async onMounted() {
        await this.loadDashboardData();
        this.setupEventListeners();
        this.setupScrollFunctionality();
    }

    onWillUnmount() {
        // Cleanup charts
        Object.values(this.charts).forEach(chart => {
            if (chart && chart.destroy) {
                chart.destroy();
            }
        });

        // Cleanup event listeners
        this.eventListeners.forEach(({ element, event, handler }) => {
            element.removeEventListener(event, handler);
        });
    }

    addEventListener(element, event, handler) {
        if (element) {
            element.addEventListener(event, handler);
            this.eventListeners.push({ element, event, handler });
        }
    }

    async loadDashboardData() {
        try {
            // Load bookings and registrations
            const bookingsResult = await this.rpc('/jupiter_dashboard_deux/bookings_registrations', {});
            this.updateBookingsData(bookingsResult);

            // Load collections and billings
            const collectionsResult = await this.rpc('/jupiter_dashboard_deux/collections_billings', {});
            this.updateCollectionsData(collectionsResult);

            // Load CP booking chart data
            const cpBookingResult = await this.rpc('/jupiter_dashboard_deux/get_last_6_month_cp_booking', {});
            this.applyCpBookingChart(cpBookingResult);

            // Load CP count data
            const cpCountResult = await this.rpc('/jupiter_dashboard_deux/get_cp_count', {});
            this.updateCpCountData(cpCountResult);
            this.applyCpCountChart(cpCountResult);
        } catch (error) {
            console.error('Error loading dashboard data:', error);
        }
    }

    updateBookingsData(result) {
        // Update booking counts
        this.updateElement('today_booking_count', result.today_booking_count);
        this.updateElement('week_booking_count', result.week_booking_count);
        this.updateElement('month_booking_count', result.month_booking_count);
        this.updateElement('year_booking_count', result.year_booking_count);
        this.updateElement('quarter_booking_count', result.quarter_booking_count);
        this.updateElement('half_booking_count', result.half_booking_count);

        // Update booking values
        this.updateElement('today_booking_value', result.today_booking_value);
        this.updateElement('week_booking_value', result.week_booking_value);
        this.updateElement('month_booking_value', result.month_booking_value);
        this.updateElement('year_booking_value', result.year_booking_value);
        this.updateElement('quarter_booking_value', result.quarter_booking_value);
        this.updateElement('half_booking_value', result.half_booking_value);

        // Update registration counts
        this.updateElement('today_registration_count', result.today_registration_count);
        this.updateElement('week_registration_count', result.week_registration_count);
        this.updateElement('month_registration_count', result.month_registration_count);
        this.updateElement('year_registration_count', result.year_registration_count);
        this.updateElement('quarter_registration_count', result.quarter_registration_count);
        this.updateElement('half_registration_count', result.half_registration_count);

        // Update registration values
        this.updateElement('today_registration_value', result.today_registration_value);
        this.updateElement('week_registration_value', result.week_registration_value);
        this.updateElement('month_registration_value', result.month_registration_value);
        this.updateElement('year_registration_value', result.year_registration_value);
        this.updateElement('quarter_registration_value', result.quarter_registration_value);
        this.updateElement('half_registration_value', result.half_registration_value);

        // Update booking attributes
        this.setAttribute('today_booking_link', 'report_attr', result.today_booking_attrs);
        this.setAttribute('week_booking_link', 'report_attr', result.week_booking_attrs);
        this.setAttribute('month_booking_link', 'report_attr', result.month_booking_attrs);
        this.setAttribute('year_booking_link', 'report_attr', result.year_booking_attrs);
        this.setAttribute('quarter_booking_link', 'report_attr', result.quarter_booking_attrs);
        this.setAttribute('half_booking_link', 'report_attr', result.half_booking_attrs);

        // Update registration attributes
        this.setAttributeForAll('.today_registration_link', 'report_attr', result.today_registration_attrs);
        this.setAttributeForAll('.week_registration_link', 'report_attr', result.week_registration_attrs);
        this.setAttributeForAll('.month_registration_link', 'report_attr', result.month_registration_attrs);
        this.setAttributeForAll('.year_registration_link', 'report_attr', result.year_registration_attrs);
        this.setAttributeForAll('.quarter_registration_link', 'report_attr', result.quarter_registration_attrs);
        this.setAttributeForAll('.half_registration_link', 'report_attr', result.half_registration_attrs);

        // Update cancelled booking counts
        this.updateElement('today_booking_cancelled_count', result.today_booking_cancelled_count);
        this.updateElement('week_booking_cancelled_count', result.week_booking_cancelled_count);
        this.updateElement('month_booking_cancelled_count', result.month_booking_cancelled_count);
        this.updateElement('year_booking_cancelled_count', result.year_booking_cancelled_count);
        this.updateElement('quarter_booking_cancelled_count', result.quarter_booking_cancelled_count);
        this.updateElement('half_booking_cancelled_count', result.half_booking_cancelled_count);

        // Update cancelled booking values
        this.updateElement('today_booking_cancelled_value', result.today_booking_cancelled_value);
        this.updateElement('week_booking_cancelled_value', result.week_booking_cancelled_value);
        this.updateElement('month_booking_cancelled_value', result.month_booking_cancelled_value);
        this.updateElement('year_booking_cancelled_value', result.year_booking_cancelled_value);
        this.updateElement('quarter_booking_cancelled_value', result.quarter_booking_cancelled_value);
        this.updateElement('half_booking_cancelled_value', result.half_booking_cancelled_value);

        // Update cancelled booking attributes
        this.setAttribute('today_booking_cancelled_link', 'report_attr', result.today_booking_cancelled_attrs);
        this.setAttribute('week_booking_cancelled_link', 'report_attr', result.week_booking_cancelled_attrs);
        this.setAttribute('month_booking_cancelled_link', 'report_attr', result.month_booking_cancelled_attrs);
        this.setAttribute('year_booking_cancelled_link', 'report_attr', result.year_booking_cancelled_attrs);
        this.setAttribute('quarter_booking_cancelled_link', 'report_attr', result.quarter_booking_cancelled_attrs);
        this.setAttribute('half_booking_cancelled_link', 'report_attr', result.half_booking_cancelled_attrs);

        // Update labels
        this.setElementsText('.quarter_label', result.quarter_label);
        this.setElementsText('.half_label', result.half_label);
        this.setElementsText('.year_label', result.year_label);

        // Update booking CP counts
        this.updateElement('today_booking_cp_count', result.today_booking_cp_count);
        this.updateElement('week_booking_cp_count', result.week_booking_cp_count);
        this.updateElement('month_booking_cp_count', result.month_booking_cp_count);
        this.updateElement('year_booking_cp_count', result.year_booking_cp_count);
        this.updateElement('quarter_booking_cp_count', result.quarter_booking_cp_count);
        this.updateElement('half_booking_cp_count', result.half_booking_cp_count);

        // Update booking CP domains
        this.setAttribute('today_booking_cp_domain', 'domain', result.today_booking_cp_domain);
        this.setAttribute('week_booking_cp_domain', 'domain', result.week_booking_cp_domain);
        this.setAttribute('month_booking_cp_domain', 'domain', result.month_booking_cp_domain);
        this.setAttribute('quarter_booking_cp_domain', 'domain', result.quarter_booking_cp_domain);
        this.setAttribute('half_booking_cp_domain', 'domain', result.half_booking_cp_domain);
        this.setAttribute('year_booking_cp_domain', 'domain', result.year_booking_cp_domain);

        // Update direct counts
        this.updateElement('today_direct', result.today_direct);
        this.updateElement('week_direct', result.week_direct);
        this.updateElement('month_direct', result.month_direct);
        this.updateElement('year_direct', result.year_direct);
        this.updateElement('quarter_direct', result.quarter_direct);
        this.updateElement('half_direct', result.half_direct);

        // Update direct domains
        this.setAttribute('today_direct_domain', 'domain', result.today_direct_domain);
        this.setAttribute('week_direct_domain', 'domain', result.week_direct_domain);
        this.setAttribute('month_direct_domain', 'domain', result.month_direct_domain);
        this.setAttribute('quarter_direct_domain', 'domain', result.quarter_direct_domain);
        this.setAttribute('half_direct_domain', 'domain', result.half_direct_domain);
        this.setAttribute('year_direct_domain', 'domain', result.year_direct_domain);

        // Update average AV
        this.updateElement('today_average_av', result.today_average_av);
        this.updateElement('week_average_av', result.week_average_av);
        this.updateElement('month_average_av', result.month_average_av);
        this.updateElement('quarter_average_av', result.quarter_average_av);
        this.updateElement('half_average_av', result.half_average_av);
        this.updateElement('year_average_av', result.year_average_av);
    }

    updateCollectionsData(result) {
        // Update collection values
        this.updateElement('today_collection', result.today_collection);
        this.updateElement('week_collection', result.week_collection);
        this.updateElement('month_collection', result.month_collection);
        this.updateElement('year_collection', result.year_collection);
        this.updateElement('quarter_collection', result.quarter_collection);
        this.updateElement('half_collection', result.half_collection);

        // Update billing values
        this.updateElement('today_billing', result.today_billing);
        this.updateElement('week_billing', result.week_billing);
        this.updateElement('month_billing', result.month_billing);
        this.updateElement('year_billing', result.year_billing);
        this.updateElement('quarter_billing', result.quarter_billing);
        this.updateElement('half_billing', result.half_billing);

        // Update billing attributes
        this.setAttribute('today_billing_attrs', 'report_attr', result.today_billing_attrs);
        this.setAttribute('week_billing_attrs', 'report_attr', result.week_billing_attrs);
        this.setAttribute('month_billing_attrs', 'report_attr', result.month_billing_attrs);
        this.setAttribute('quarter_billing_attrs', 'report_attr', result.quarter_billing_attrs);
        this.setAttribute('half_billing_attrs', 'report_attr', result.half_billing_attrs);
        this.setAttribute('year_billing_attrs', 'report_attr', result.year_billing_attrs);

        // Update collection attributes
        this.setAttribute('today_collection_attr', 'domain', result.today_collection_domain);
        this.setAttribute('week_collection_attr', 'domain', result.week_collection_domain);
        this.setAttribute('month_collection_attr', 'domain', result.month_collection_domain);
        this.setAttribute('quarter_collection_attr', 'domain', result.quarter_collection_domain);
        this.setAttribute('half_collection_attr', 'domain', result.half_collection_domain);
        this.setAttribute('year_collection_attr', 'domain', result.year_collection_domain);
    }

    updateCpCountData(result) {
        // Update CP counts
        this.updateElement('month_cps', result.month_cps);
        this.updateElement('quarter_cps', result.quarter_cps);
        this.updateElement('half_cps', result.half_cps);
        this.updateElement('year_cps', result.year_cps);

        // Update active CP counts
        this.updateElement('month_cps_active', result.month_cps_active);
        this.updateElement('quarter_cps_active', result.quarter_cps_active);
        this.updateElement('half_cps_active', result.half_cps_active);
        this.updateElement('year_cps_active', result.year_cps_active);

        // Update CP domains
        this.setAttribute('month_cp_domain', 'domain', result.month_cp_domain);
        this.setAttribute('quarter_cp_domain', 'domain', result.quarter_cp_domain);
        this.setAttribute('half_cp_domain', 'domain', result.half_cp_domain);
        this.setAttribute('year_cp_domain', 'domain', result.year_cp_domain);

        // Update active CP domains
        this.setAttribute('month_cp_active_domain', 'domain', result.month_cp_active_domain);
        this.setAttribute('quarter_cp_active_domain', 'domain', result.quarter_cp_active_domain);
        this.setAttribute('half_cp_active_domain', 'domain', result.half_cp_active_domain);
        this.setAttribute('year_cp_active_domain', 'domain', result.year_cp_active_domain);
    }

    applyCpCountChart(result) {
        const options = {
            series: [{
                name: 'New CPs Added',
                data: result.create_cps_list,
            }, {
                name: 'Active CPs',
                data: result.active_cps_list,
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
                categories: result.months,
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

        const chartElement = document.getElementById('cp_count_chart');
        if (chartElement) {
            chartElement.innerHTML = '';
            // Destroy existing chart if any
            if (this.charts.cpCountChart) {
                this.charts.cpCountChart.destroy();
            }
            this.charts.cpCountChart = new ApexCharts(chartElement, options);
            this.charts.cpCountChart.render();
        }
    }

    applyCpBookingChart(result) {
        const options = {
            series: [
                {
                    name: "Booking",
                    data: result.bookings
                }
            ],
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
                categories: result.months,
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

        const chartElement = document.getElementById('cp_chart');
        if (chartElement) {
            chartElement.innerHTML = '';
            // Destroy existing chart if any
            if (this.charts.cpChart) {
                this.charts.cpChart.destroy();
            }
            this.charts.cpChart = new ApexCharts(chartElement, options);
            this.charts.cpChart.render();
        }
    }

    setupEventListeners() {
        // Add click event listeners for report links
        const reportLinks = document.querySelectorAll('.report_link');
        reportLinks.forEach(link => {
            this.addEventListener(link, 'click', (ev) => this.linkToReport(ev));
        });

        // Add click event listeners for list view links
        const listViewLinks = document.querySelectorAll('.list_view_link');
        listViewLinks.forEach(link => {
            this.addEventListener(link, 'click', (ev) => this.linkToList(ev));
        });
    }

    async linkToList(ev) {
        const target = ev.currentTarget;
        const domain = target.getAttribute('domain');
        const model = target.getAttribute('model');
        const name = target.getAttribute('name');

        try {
            const result = await this.rpc('/jupiter_dashboard_deux/call_list_view', {
                domain: domain,
                model: model,
                name: name
            });
            this.action.doAction(result);
        } catch (error) {
            console.error('Error calling list view:', error);
        }
    }

    async linkToReport(ev) {
        const target = ev.currentTarget;
        let reportAttrStr = target.getAttribute('report_attr');
        const model = target.getAttribute('model');

        if (!reportAttrStr) return;

        try {
            // Parse the report attributes (replace single quotes with double quotes)
            let reportAttr = JSON.parse(reportAttrStr.replace(/'/g, '"'));

            // Handle consolidate boolean conversion
            if ('consolidate' in reportAttr) {
                if (reportAttr.consolidate === 'False') {
                    reportAttr.consolidate = false;
                } else {
                    reportAttr.consolidate = true;
                }
            }

            const result = await this.rpc('/jupiter_dashboard_deux/call_report', {
                report_attr: reportAttr,
                model: model
            });
            this.action.doAction(result);
        } catch (error) {
            console.error('Error calling report:', error);
        }
    }

    setupScrollFunctionality() {
        try {
            const container = document.getElementById('horizontal-scroll-container');
            if (!container) return;

            const leftArrow = document.querySelector('.left-arrow');
            const rightArrow = document.querySelector('.right-arrow');

            // Get the width of a single flex-scroll-item
            const singleFlexScrollItem = document.querySelector('.flex-scroll-item');
            const itemWidth = singleFlexScrollItem ? singleFlexScrollItem.offsetWidth + 10 : 1000;

            // Wheel event for shift+scroll
            const wheelHandler = (e) => {
                if (e.shiftKey) {
                    e.preventDefault();
                    this.smoothScroll(container, container.scrollLeft + e.deltaY * 2);
                }
            };
            this.addEventListener(container, 'wheel', wheelHandler);

            // Arrow click events
            if (leftArrow) {
                this.addEventListener(leftArrow, 'click', () => {
                    this.smoothScroll(container, container.scrollLeft - itemWidth);
                    this.updateArrowVisibility(container, leftArrow, rightArrow);
                });
            }

            if (rightArrow) {
                this.addEventListener(rightArrow, 'click', () => {
                    this.smoothScroll(container, container.scrollLeft + itemWidth);
                    this.updateArrowVisibility(container, leftArrow, rightArrow);
                });
            }

            // Mouse down event
            this.addEventListener(container, 'mousedown', (e) => {
                this.scrollState.isDragging = true;
                container.classList.add('active');
                container.classList.add('grabbing');
                this.scrollState.startX = e.pageX - container.offsetLeft;
                this.scrollState.scrollLeft = container.scrollLeft;
            });

            // Mouse up event
            this.addEventListener(container, 'mouseup', () => {
                this.scrollState.isDragging = false;
                container.classList.remove('active');
                container.classList.remove('grabbing');
                this.updateArrowVisibility(container, leftArrow, rightArrow);
            });

            // Mouse move event
            this.addEventListener(container, 'mousemove', (e) => {
                if (!this.scrollState.isDragging) return;
                e.preventDefault();
                const x = e.pageX - container.offsetLeft;
                const walk = (x - this.scrollState.startX) * 3;
                this.smoothScroll(container, this.scrollState.scrollLeft - walk);
            });

            // Mouse leave event
            this.addEventListener(container, 'mouseleave', () => {
                if (this.scrollState.isDragging) {
                    this.scrollState.isDragging = false;
                    container.classList.remove('active');
                    container.classList.remove('grabbing');
                    this.updateArrowVisibility(container, leftArrow, rightArrow);
                }
            });

            // Initial arrow visibility
            this.updateArrowVisibility(container, leftArrow, rightArrow);
        } catch (e) {
            console.error('Error setting up scroll functionality:', e);
        }
    }

    smoothScroll(container, targetX) {
        let start = container.scrollLeft;
        let change = targetX - start;
        let currentTime = 0;
        const increment = 20;
        const duration = 300;

        const animateScroll = () => {
            currentTime += increment;
            const val = this.easeInOutQuad(currentTime, start, change, duration);
            container.scrollLeft = val;
            if (currentTime < duration) {
                requestAnimationFrame(animateScroll);
            } else {
                this.updateArrowVisibility(container,
                    document.querySelector('.left-arrow'),
                    document.querySelector('.right-arrow'));
            }
        };
        animateScroll();
    }

    easeInOutQuad(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
    }

    updateArrowVisibility(container, leftArrow, rightArrow) {
        if (leftArrow) {
            leftArrow.style.display = container.scrollLeft <= 0 ? 'none' : 'block';
        }
        if (rightArrow) {
            rightArrow.style.display = container.scrollLeft + container.clientWidth >= container.scrollWidth ? 'none' : 'block';
        }
    }

    // Helper methods for DOM manipulation
    updateElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value || '';
        }
    }

    setAttribute(id, attr, value) {
        const element = document.getElementById(id);
        if (element && value !== undefined) {
            element.setAttribute(attr, value);
        }
    }

    setAttributeForAll(selector, attr, value) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
            if (value !== undefined) {
                el.setAttribute(attr, value);
            }
        });
    }

    setElementsText(selector, value) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
            el.textContent = value || '';
        });
    }
}

registry.category("actions").add("jupiter_dashboard_deux", JupiterDashboardDeux);
