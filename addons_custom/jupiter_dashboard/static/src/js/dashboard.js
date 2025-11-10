/** @odoo-module **/

import { Component, onMounted, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class JupiterDashboard extends Component {
    static template = "JupiterDashboard";

    setup() {
        this.rpc = useService("rpc");

        // Container refs for charts
        this.regionWiseBookingRef = useRef("regionWiseBooking");
        this.bookingChartRef = useRef("bookingChart");
        this.registrationChartRef = useRef("registrationChart");
        this.bookingVsBudgetChartRef = useRef("bookingVsBudgetChart");
        this.registrationVsBudgetChartRef = useRef("registrationVsBudgetChart");
        this.regionWiseFlatStatusRef = useRef("regionWiseFlatStatus");
        this.projectWiseFlatStatusRef = useRef("projectWiseFlatStatus");

        // Chart instances
        this.charts = {};

        onMounted(() => this.onMounted());
    }

    async onMounted() {
        // Load all dashboard data
        await this.loadRow1Data();
        await this.loadFinancialYearData();
        await this.loadRow2Data();
        await this.loadRow3Data();
        await this.loadRow4Data();
        await this.loadRegions();

        // Setup event listeners
        this.setupEventListeners();
    }

    setupEventListeners() {
        const finYearSelect = document.getElementById('financial_year_selection');
        if (finYearSelect) {
            finYearSelect.addEventListener('change', (ev) => this.onChangeFinancialYear(ev));
        }

        const bookingTypeInputs = document.querySelectorAll('[name="booking_type_select"]');
        bookingTypeInputs.forEach(input => {
            input.addEventListener('change', (ev) => this.onChangeBookingType(ev));
        });

        const registrationTypeInputs = document.querySelectorAll('[name="registration_type_select"]');
        registrationTypeInputs.forEach(input => {
            input.addEventListener('change', (ev) => this.onChangeRegistrationType(ev));
        });

        const regionItems = document.querySelectorAll('#region_selection .dropdown-item');
        regionItems.forEach(item => {
            item.addEventListener('click', (ev) => this.onChangeRegion(ev));
        });
    }

    async onChangeFinancialYear(ev) {
        const finYear = ev.target.value;
        const result = await this.rpc('/jupiter_dashboard/get_financial_year_data', {
            get_selection: false,
            fin_year: finYear
        });

        this.updateElement('year_booking_gross', result['year_booking_gross']);
        this.updateElement('year_booking_cancelled', result['year_booking_cancelled']);
        this.updateElement('year_booking_net', result['year_booking_net']);
        this.updateElement('year_registration_count', result['year_registration_count']);
        this.updateElement('year_registration_value', result['year_registration_value']);
        this.updateElement('year_booking_value', result['year_booking_value']);

        const finYearStrings = document.querySelectorAll('.fin_year_string');
        finYearStrings.forEach(el => {
            el.textContent = result['fin_year_string'];
        });
    }

    async onChangeRegion(ev) {
        const region = ev.target.getAttribute('value') || false;
        const regionButton = document.querySelector('#region_selection button');
        if (regionButton) {
            regionButton.textContent = ev.target.textContent;
        }

        const result = await this.rpc('/jupiter_dashboard/row_4', {
            'region_wise': false,
            'project_wise': true,
            'project_region': region
        });

        this.projectOrRegionFlatStatus(result, true, false);
    }

    onChangeBookingType(ev) {
        const bookingType = document.querySelector('[name="booking_type_select"]:checked').value;
        this.rpc('/jupiter_dashboard/row_2', {
            booking_type: bookingType,
            registration_type: false,
            budget_type: false
        }).then((result) => {
            this.bookingAndRegistrationChart(result, bookingType, false);
        });
    }

    onChangeRegistrationType(ev) {
        const registrationType = document.querySelector('[name="registration_type_select"]:checked').value;
        this.rpc('/jupiter_dashboard/row_2', {
            booking_type: false,
            registration_type: registrationType,
            budget_type: false
        }).then((result) => {
            this.bookingAndRegistrationChart(result, false, registrationType);
        });
    }

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

            const container = this.regionWiseFlatStatusRef.el;
            container.innerHTML = '';
            if (this.charts.regionWiseFlatStatus) {
                this.charts.regionWiseFlatStatus.destroy();
            }
            this.charts.regionWiseFlatStatus = new ApexCharts(container, options);
            this.charts.regionWiseFlatStatus.render();
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

            const container = this.projectWiseFlatStatusRef.el;
            container.innerHTML = '';
            if (this.charts.projectWiseFlatStatus) {
                this.charts.projectWiseFlatStatus.destroy();
            }
            this.charts.projectWiseFlatStatus = new ApexCharts(container, options);
            this.charts.projectWiseFlatStatus.render();
        }
    }

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

        const container = this.regionWiseBookingRef.el;
        if (this.charts.regionWiseBooking) {
            this.charts.regionWiseBooking.destroy();
        }
        this.charts.regionWiseBooking = new ApexCharts(container, options);
        this.charts.regionWiseBooking.render();
    }

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

            const container = this.bookingChartRef.el;
            container.innerHTML = '';
            if (this.charts.bookingChart) {
                this.charts.bookingChart.destroy();
            }
            this.charts.bookingChart = new ApexCharts(container, options);
            this.charts.bookingChart.render();
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

            const container = this.registrationChartRef.el;
            container.innerHTML = '';
            if (this.charts.registrationChart) {
                this.charts.registrationChart.destroy();
            }
            this.charts.registrationChart = new ApexCharts(container, options);
            this.charts.registrationChart.render();
        }
    }

    ActualBudgetComparison(result) {
        // Booking vs Budget Chart
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

        const bookingContainer = this.bookingVsBudgetChartRef.el;
        bookingContainer.innerHTML = '';
        if (this.charts.bookingVsBudget) {
            this.charts.bookingVsBudget.destroy();
        }
        this.charts.bookingVsBudget = new ApexCharts(bookingContainer, bookingOptions);
        this.charts.bookingVsBudget.render();

        // Registration vs Budget Chart
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

        const registrationContainer = this.registrationVsBudgetChartRef.el;
        registrationContainer.innerHTML = '';
        if (this.charts.registrationVsBudget) {
            this.charts.registrationVsBudget.destroy();
        }
        this.charts.registrationVsBudget = new ApexCharts(registrationContainer, registrationOptions);
        this.charts.registrationVsBudget.render();
    }

    async loadRow1Data() {
        const result = await this.rpc('/jupiter_dashboard/row_1', {});

        this.updateElement('today_booking_gross', result['today_booking_gross']);
        this.updateElement('today_booking_cancelled', result['today_booking_cancelled']);
        this.updateElement('today_booking_net', result['today_booking_net']);
        this.updateElement('week_booking_gross', result['week_booking_gross']);
        this.updateElement('week_booking_cancelled', result['week_booking_cancelled']);
        this.updateElement('week_booking_net', result['week_booking_net']);
        this.updateElement('month_booking_gross', result['month_booking_gross']);
        this.updateElement('month_booking_cancelled', result['month_booking_cancelled']);
        this.updateElement('month_booking_net', result['month_booking_net']);

        this.updateElement('today_registration_count', result['today_registration_count']);
        this.updateElement('this_week_registration_count', result['this_week_registration_count']);
        this.updateElement('this_month_registration_count', result['this_month_registration_count']);
    }

    async loadFinancialYearData() {
        const result = await this.rpc('/jupiter_dashboard/get_financial_year_data', {
            get_selection: true,
            fin_year: false
        });

        const finYearSelect = document.getElementById('financial_year_selection');
        if (finYearSelect) {
            finYearSelect.innerHTML = result['fin_year_selection'];
        }

        this.updateElement('year_booking_gross', result['year_booking_gross']);
        this.updateElement('year_booking_cancelled', result['year_booking_cancelled']);
        this.updateElement('year_booking_net', result['year_booking_net']);
        this.updateElement('year_registration_count', result['year_registration_count']);
        this.updateElement('year_registration_value', result['year_registration_value']);
        this.updateElement('year_booking_value', result['year_booking_value']);

        const finYearStrings = document.querySelectorAll('.fin_year_string');
        finYearStrings.forEach(el => {
            el.textContent = result['fin_year_string'];
        });
    }

    async loadRow2Data() {
        const result = await this.rpc('/jupiter_dashboard/row_2', {});
        this.bookingAndRegistrationChart(result, 'number', 'number');
        this.ActualBudgetComparison(result);
    }

    async loadRow3Data() {
        const result = await this.rpc('/jupiter_dashboard/row_3', {});
        this.regionWiseBooking(result);
    }

    async loadRow4Data() {
        const result = await this.rpc('/jupiter_dashboard/row_4', {
            'region_wise': true,
            'project_wise': true,
            'project_region': false
        });
        this.projectOrRegionFlatStatus(result, true, true);
    }

    async loadRegions() {
        const result = await this.rpc('/jupiter_dashboard/get_region', {});
        const regionDropdown = document.querySelector('#region_selection .dropdown-menu');
        if (regionDropdown) {
            regionDropdown.innerHTML = result;

            // Re-attach event listeners after DOM update
            const regionItems = document.querySelectorAll('#region_selection .dropdown-item');
            regionItems.forEach(item => {
                item.addEventListener('click', (ev) => this.onChangeRegion(ev));
            });
        }
    }

    updateElement(id, content) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = content;
        }
    }
}

registry.category("actions").add("jupiter_dashboard", JupiterDashboard);
