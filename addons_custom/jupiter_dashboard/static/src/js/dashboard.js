/** @odoo-module **/

/**
 * Jupiter Dashboard - Bookings, Registrations, Budget Analytics Dashboard
 * Migrated to Odoo 18 OWL framework
 *
 * Features:
 * - ApexCharts integration (bar, line, and polar area charts)
 * - Booking and registration metrics
 * - Budget vs Actual comparison
 * - Region-wise and project-wise analytics
 * - Financial year selection
 */

import { Component, onMounted, onWillStart, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { loadJS } from "@web/core/assets";

export class JupiterDashboard extends Component {
    static template = "JupiterDashboard";

    setup() {
        this.action = useService("action");
        this.rpc = useService("rpc");

        onWillStart(async () => {
            // Load ApexCharts library
            await loadJS("/web/static/lib/apexcharts/apexcharts.js");
        });

        onMounted(async () => {
            await this.renderElement();
            this.setupEventListeners();
        });
    }

    /**
     * Setup event listeners for interactive elements
     */
    setupEventListeners() {
        // Booking type selection
        const bookingTypeRadios = document.querySelectorAll('[name="booking_type_select"]');
        bookingTypeRadios.forEach(radio => {
            radio.addEventListener('change', (ev) => this.onChangeBookingType(ev));
        });

        // Registration type selection
        const registrationTypeRadios = document.querySelectorAll('[name="registration_type_select"]');
        registrationTypeRadios.forEach(radio => {
            radio.addEventListener('change', (ev) => this.onChangeRegistrationType(ev));
        });

        // Region selection
        const regionItems = document.querySelectorAll('#region_selection .dropdown-item');
        regionItems.forEach(item => {
            item.addEventListener('click', (ev) => this.onChangeRegion(ev));
        });

        // Financial year selection
        const finYearSelect = document.querySelector('#financial_year_selection');
        if (finYearSelect) {
            finYearSelect.addEventListener('change', (ev) => this.onChangeFinancialYear(ev));
        }
    }

    /**
     * Handle financial year change
     */
    async onChangeFinancialYear(ev) {
        const finYear = ev.target.value;
        const result = await this.rpc('/jupiter_dashboard/get_financial_year_data', {
            get_selection: false,
            fin_year: finYear
        });

        this.updateElement('#year_booking_gross', result['year_booking_gross']);
        this.updateElement('#year_booking_cancelled', result['year_booking_cancelled']);
        this.updateElement('#year_booking_net', result['year_booking_net']);
        this.updateElement('#year_registration_count', result['year_registration_count']);
        this.updateElement('#year_registration_value', result['year_registration_value']);
        this.updateElement('#year_booking_value', result['year_booking_value']);
        this.updateElementAll('.fin_year_string', result['fin_year_string']);
    }

    /**
     * Handle region change
     */
    async onChangeRegion(ev) {
        const target = ev.currentTarget;
        const region = target.getAttribute('value') || false;
        const regionText = target.textContent;

        const regionButton = document.querySelector('#region_selection button');
        if (regionButton) {
            regionButton.textContent = regionText;
        }

        const result = await this.rpc('/jupiter_dashboard/row_4', {
            region_wise: false,
            project_wise: true,
            project_region: region
        });

        this.projectOrRegionFlatStatus(result, true, false);
    }

    /**
     * Handle booking type change
     */
    async onChangeBookingType(ev) {
        const bookingType = document.querySelector('[name="booking_type_select"]:checked')?.value;

        const result = await this.rpc('/jupiter_dashboard/row_2', {
            booking_type: bookingType,
            registration_type: false,
            budget_type: false
        });

        this.bookingAndRegistrationChart(result, bookingType, false);
    }

    /**
     * Handle registration type change
     */
    async onChangeRegistrationType(ev) {
        const registrationType = document.querySelector('[name="registration_type_select"]:checked')?.value;

        const result = await this.rpc('/jupiter_dashboard/row_2', {
            booking_type: false,
            registration_type: registrationType,
            budget_type: false
        });

        this.bookingAndRegistrationChart(result, false, registrationType);
    }

    /**
     * Render project or region flat status charts
     */
    projectOrRegionFlatStatus(result, projectWise, regionWise) {
        if (regionWise) {
            const options = {
                series: [
                    {
                        name: 'Booked',
                        data: result['region_booked']
                    },
                    {
                        name: 'Available',
                        data: result['region_available']
                    },
                ],
                title: {
                    text: 'Region Wise Flat Status',
                    align: 'left'
                },
                chart: {
                    fontFamily: 'Poppins, sans-serif',
                    type: 'bar',
                    height: 350,
                    stacked: true,
                    zoom: {
                        enabled: false
                    },
                    toolbar: {
                        show: false
                    }
                },
                stroke: {
                    width: 1,
                    colors: ['#fff']
                },
                dataLabels: {
                    formatter: (val) => {
                        return val;
                    }
                },
                plotOptions: {
                    bar: {
                        borderRadius: 4,
                        dataLabels: {
                            position: 'center',
                        },
                    }
                },
                xaxis: {
                    title: {
                        text: 'Region'
                    },
                    categories: result['regions']
                },
                fill: {
                    opacity: 1,
                    type: 'gradient',
                    gradient: {
                        shade: 'dark',
                        type: 'vertical',
                        shadeIntensity: 1,
                        gradientToColors: ['#007FFF', '#007FFF']
                    }
                },
                colors: ['#6F00FF', '#007FFF'],
                yaxis: {
                    title: {
                        text: 'Count'
                    },
                    labels: {
                        formatter: (val) => {
                            return val;
                        }
                    }
                },
                legend: {
                    position: 'bottom',
                    horizontalAlign: 'left'
                }
            };

            const chartElement = document.querySelector("#region_wise_flat_status");
            if (chartElement) {
                chartElement.innerHTML = '';
                const chart = new ApexCharts(chartElement, options);
                chart.render();
            }
        }

        if (projectWise) {
            const options = {
                series: [
                    {
                        name: 'Booked',
                        data: result['project_booked']
                    },
                    {
                        name: 'Available',
                        data: result['project_available']
                    },
                ],
                title: {
                    text: 'Project Wise Flat Status',
                    align: 'left'
                },
                chart: {
                    fontFamily: 'Poppins, sans-serif',
                    type: 'bar',
                    height: 550,
                    stacked: true,
                    zoom: {
                        enabled: false
                    },
                    toolbar: {
                        show: false
                    }
                },
                stroke: {
                    width: 1,
                    colors: ['#fff']
                },
                dataLabels: {
                    formatter: (val) => {
                        return val;
                    }
                },
                plotOptions: {
                    bar: {
                        borderRadius: 3,
                        dataLabels: {
                            position: 'center',
                        },
                    }
                },
                xaxis: {
                    title: {
                        text: 'Projects'
                    },
                    categories: result['projects']
                },
                fill: {
                    opacity: 1,
                    type: 'gradient',
                    gradient: {
                        shade: 'dark',
                        type: 'vertical',
                        shadeIntensity: 0.5,
                        gradientToColors: ['#00CCFF', '#00CCFF']
                    }
                },
                colors: ['#00A693', '#00CCFF'],
                yaxis: {
                    title: {
                        text: 'Count'
                    },
                    labels: {
                        formatter: (val) => {
                            return val;
                        }
                    }
                },
                legend: {
                    position: 'top',
                    horizontalAlign: 'right'
                }
            };

            const chartElement = document.querySelector("#project_wise_flat_status");
            if (chartElement) {
                chartElement.innerHTML = '';
                const chart = new ApexCharts(chartElement, options);
                chart.render();
            }
        }
    }

    /**
     * Render region-wise booking chart (Polar Area)
     */
    regionWiseBooking(result) {
        const options = {
            series: result['booking'],
            chart: {
                fontFamily: 'Poppins, sans-serif',
                height: 400,
                type: 'polarArea'
            },
            labels: result['region'],
            fill: {
                opacity: 1
            },
            stroke: {
                width: 1,
                colors: undefined
            },
            yaxis: {
                show: false
            },
            legend: {
                position: 'bottom'
            },
            title: {
                text: 'Region Wise Booking',
                align: 'left'
            },
            plotOptions: {
                polarArea: {
                    rings: {
                        strokeWidth: 0
                    },
                    spokes: {
                        strokeWidth: 0
                    },
                }
            },
        };

        const chartElement = document.querySelector("#region_wise_booking");
        if (chartElement) {
            const chart = new ApexCharts(chartElement, options);
            chart.render();
        }
    }

    /**
     * Render booking and registration charts
     */
    bookingAndRegistrationChart(result, bookingType, registrationType) {
        if (bookingType) {
            const options = {
                colors: ['#04AA6D'],
                series: [{
                    name: 'Booking',
                    data: result['bookings']
                }],
                chart: {
                    fontFamily: 'Poppins, sans-serif',
                    height: 400,
                    type: 'bar',
                    zoom: {
                        enabled: true
                    },
                    toolbar: {
                        show: false
                    }
                },
                plotOptions: {
                    bar: {
                        borderRadius: 5,
                        dataLabels: {
                            position: 'top',
                        },
                    }
                },
                dataLabels: {
                    enabled: true,
                    formatter: function (val) {
                        return (bookingType === 'number') ? val : val.toFixed(2);
                    },
                    offsetY: -20,
                    style: {
                        fontSize: '12px',
                        colors: ["#304758"]
                    }
                },
                xaxis: {
                    title: {
                        text: 'Month'
                    },
                    categories: result['months'],
                    position: 'bottom',
                    axisBorder: {
                        show: false
                    },
                    axisTicks: {
                        show: false
                    },
                    crosshairs: {
                        fill: {
                            type: 'gradient',
                            gradient: {
                                colorFrom: '#D8E3F0',
                                colorTo: '#BED1E6',
                                stops: [0, 100],
                                opacityFrom: 0.4,
                                opacityTo: 0.5,
                            }
                        }
                    },
                    tooltip: {
                        enabled: true,
                    }
                },
                yaxis: {
                    title: {
                        text: (bookingType === 'number') ? 'Count' : 'Value (*In Lakhs)'
                    },
                    axisBorder: {
                        show: true
                    },
                    labels: {
                        show: true,
                        formatter: function (val) {
                            return val;
                        }
                    }
                },
                tooltip: {
                    y: {
                        formatter: function(val) {
                            return (bookingType === 'number') ? val : val.toFixed(2);
                        }
                    }
                },
                title: {
                    text: 'Last 12 Month Booking',
                    align: 'left',
                    style: {
                        color: '#444'
                    }
                }
            };

            const chartElement = document.querySelector("#booking_chart");
            if (chartElement) {
                chartElement.innerHTML = '';
                const chart = new ApexCharts(chartElement, options);
                chart.render();
            }
        }

        if (registrationType) {
            const options = {
                series: [{
                    name: 'Registration',
                    data: result['registrations']
                }],
                chart: {
                    fontFamily: 'Poppins, sans-serif',
                    height: 400,
                    type: 'bar',
                    zoom: {
                        enabled: true
                    },
                    toolbar: {
                        show: false
                    }
                },
                plotOptions: {
                    bar: {
                        borderRadius: 5,
                        dataLabels: {
                            position: 'top',
                        },
                    }
                },
                dataLabels: {
                    enabled: true,
                    formatter: function (val) {
                        return (registrationType === 'number') ? val : val.toFixed(2);
                    },
                    offsetY: -20,
                    style: {
                        fontSize: '12px',
                        colors: ["#304758"]
                    }
                },
                xaxis: {
                    title: {
                        text: 'Month'
                    },
                    categories: result['months'],
                    position: 'bottom',
                    axisBorder: {
                        show: false
                    },
                    axisTicks: {
                        show: false
                    },
                    crosshairs: {
                        fill: {
                            type: 'gradient',
                            gradient: {
                                colorFrom: '#D8E3F0',
                                colorTo: '#BED1E6',
                                stops: [0, 100],
                                opacityFrom: 0.4,
                                opacityTo: 0.5,
                            }
                        }
                    },
                    tooltip: {
                        enabled: true,
                    }
                },
                yaxis: {
                    title: {
                        text: (registrationType === 'number') ? 'Count' : 'Value (*In Lakhs)'
                    },
                    axisBorder: {
                        show: true
                    },
                    labels: {
                        show: true,
                        formatter: function (val) {
                            return val;
                        }
                    }
                },
                tooltip: {
                    y: {
                        formatter: function(val) {
                            return (registrationType === 'number') ? val : val.toFixed(2);
                        }
                    }
                },
                title: {
                    text: 'Last 12 Month Registration',
                    align: 'left',
                    style: {
                        color: '#444'
                    }
                }
            };

            const chartElement = document.querySelector("#registration_chart");
            if (chartElement) {
                chartElement.innerHTML = '';
                const chart = new ApexCharts(chartElement, options);
                chart.render();
            }
        }
    }

    /**
     * Render Budget vs Actual comparison charts
     */
    ActualBudgetComparison(result) {
        // Booking Budget vs Actual
        const bookingOptions = {
            series: [
                {
                    name: "Budget",
                    data: result['booking_budgets']
                },
                {
                    name: "Actual",
                    data: result['bookings']
                }
            ],
            chart: {
                fontFamily: 'Poppins, sans-serif',
                height: 400,
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
            colors: ['#ff006e', '#2ec4b6'],
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
                text: 'Booking - Budget Vs Actual',
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

        const bookingChartElement = document.querySelector("#booking_vs_budget_chart");
        if (bookingChartElement) {
            bookingChartElement.innerHTML = '';
            const bookingChart = new ApexCharts(bookingChartElement, bookingOptions);
            bookingChart.render();
        }

        // Registration Budget vs Actual
        const registrationOptions = {
            series: [
                {
                    name: "Budget",
                    data: result['registration_budgets']
                },
                {
                    name: "Actual",
                    data: result['registrations']
                }
            ],
            chart: {
                fontFamily: 'Poppins, sans-serif',
                height: 400,
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
            colors: ['#1e96fc', '#00af54'],
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
                text: 'Registrations - Budget Vs Actual',
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

        const registrationChartElement = document.querySelector("#registration_vs_budget_chart");
        if (registrationChartElement) {
            registrationChartElement.innerHTML = '';
            const registrationChart = new ApexCharts(registrationChartElement, registrationOptions);
            registrationChart.render();
        }
    }

    /**
     * Main render function - loads all dashboard data
     */
    async renderElement() {
        // Load row 1 data (today, week, month booking and registration)
        const row1Data = await this.rpc('/jupiter_dashboard/row_1', {});

        this.updateElement('#today_booking_gross', row1Data['today_booking_gross']);
        this.updateElement('#today_booking_cancelled', row1Data['today_booking_cancelled']);
        this.updateElement('#today_booking_net', row1Data['today_booking_net']);
        this.updateElement('#week_booking_gross', row1Data['week_booking_gross']);
        this.updateElement('#week_booking_cancelled', row1Data['week_booking_cancelled']);
        this.updateElement('#week_booking_net', row1Data['week_booking_net']);
        this.updateElement('#month_booking_gross', row1Data['month_booking_gross']);
        this.updateElement('#month_booking_cancelled', row1Data['month_booking_cancelled']);
        this.updateElement('#month_booking_net', row1Data['month_booking_net']);

        this.updateElement('#today_registration_count', row1Data['today_registration_count']);
        this.updateElement('#this_week_registration_count', row1Data['this_week_registration_count']);
        this.updateElement('#this_month_registration_count', row1Data['this_month_registration_count']);

        // Load financial year data
        const finYearData = await this.rpc('/jupiter_dashboard/get_financial_year_data', {
            get_selection: true,
            fin_year: false
        });

        const finYearSelect = document.querySelector('#financial_year_selection');
        if (finYearSelect) {
            finYearSelect.innerHTML = finYearData['fin_year_selection'];
        }

        this.updateElement('#year_booking_gross', finYearData['year_booking_gross']);
        this.updateElement('#year_booking_cancelled', finYearData['year_booking_cancelled']);
        this.updateElement('#year_booking_net', finYearData['year_booking_net']);
        this.updateElement('#year_registration_count', finYearData['year_registration_count']);
        this.updateElement('#year_registration_value', finYearData['year_registration_value']);
        this.updateElement('#year_booking_value', finYearData['year_booking_value']);
        this.updateElementAll('.fin_year_string', finYearData['fin_year_string']);

        // Load row 2 data (booking and registration charts, budget comparison)
        const row2Data = await this.rpc('/jupiter_dashboard/row_2', {});

        this.bookingAndRegistrationChart(row2Data, 'number', 'number');
        this.ActualBudgetComparison(row2Data);

        // Load row 3 data (region-wise booking)
        const row3Data = await this.rpc('/jupiter_dashboard/row_3', {});

        this.regionWiseBooking(row3Data);

        // Load row 4 data (region and project flat status)
        const row4Data = await this.rpc('/jupiter_dashboard/row_4', {
            region_wise: true,
            project_wise: true,
            project_region: false
        });

        this.projectOrRegionFlatStatus(row4Data, true, true);

        // Load region dropdown
        const regionData = await this.rpc('/jupiter_dashboard/get_region', {});

        const regionDropdown = document.querySelector('#region_selection .dropdown-menu');
        if (regionDropdown) {
            regionDropdown.innerHTML = regionData;
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
registry.category("actions").add("jupiter_dashboard", JupiterDashboard);

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
 * - Added helper methods for DOM manipulation
 * - Event handlers setup in separate method
 *
 * Dependencies:
 * - ApexCharts (/web/static/lib/apexcharts/apexcharts.js)
 * - OWL framework
 * - RPC and Action services
 *
 * Template Required:
 * - JupiterDashboard (static/src/xml/template.xml)
 *
 * Testing Checklist:
 * - [ ] Dashboard loads without errors
 * - [ ] All metrics display correctly
 * - [ ] ApexCharts render properly (bar, line, polar area)
 * - [ ] Booking type selection updates chart
 * - [ ] Registration type selection updates chart
 * - [ ] Financial year selection updates data
 * - [ ] Region selection updates project flat status
 * - [ ] Budget vs Actual charts render correctly
 * - [ ] All RPC calls complete successfully
 * - [ ] Interactive elements work (dropdowns, radio buttons)
 */
