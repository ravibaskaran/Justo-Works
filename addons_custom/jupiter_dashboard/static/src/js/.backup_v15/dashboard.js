odoo.define('jupiter_dashboard.JupiterDashboard', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var web_client = require('web.web_client');
    var _t = core._t;
    var QWeb = core.qweb;
    var JupiterDashboard = AbstractAction.extend({
        template: 'JupiterDashboard',
        events: {
            'change [name="booking_type_select"]': 'onChangeBookingType',
            'change [name="registration_type_select"]': 'onChangeRegistrationType',
            'click #region_selection .dropdown-item': 'onChangeRegion',
            'change #financial_year_selection': 'onChangeFinancialYear'
        },

        onChangeFinancialYear: function(ev){
            var fin_year = ev.target.value
            ajax.jsonRpc('/jupiter_dashboard/get_financial_year_data', 'call', {get_selection: false, fin_year: fin_year}, {shadow:true}).then(function (result) {
                $('#year_booking_gross').empty().append(result['year_booking_gross'])
                $('#year_booking_cancelled').empty().append(result['year_booking_cancelled'])
                $('#year_booking_net').empty().append(result['year_booking_net'])
                $('#year_registration_count').empty().append(result['year_registration_count'])
                $('#year_registration_value').empty().append(result['year_registration_value'])
                $('#year_booking_value').empty().append(result['year_booking_value'])
                $('.fin_year_string').empty().append(result['fin_year_string'])
            })
        },

        onChangeRegion: function(ev){
            var self = this;
            var region = $(ev.target).attr('value') || false
            $('#region_selection button').empty().append($(ev.target).text())
            ajax.jsonRpc('/jupiter_dashboard/row_4', 'call', {'region_wise': false, 'project_wise': true, 'project_region': region}, {shadow:true}).then(function (result) {
                self.projectOrRegionFlatStatus(result, true, false)
            })
        },

        onChangeBookingType: function (ev){
            var self = this;
            console.log($('[name="booking_type_select"]:checked').val(), 'fhfofheohf')
            var booking_type = $('[name="booking_type_select"]:checked').val()
            ajax.jsonRpc('/jupiter_dashboard/row_2', 'call', {booking_type: booking_type, registration_type: false, budget_type: false}, {shadow:true}).then(function (result) {
                self.bookingAndRegistrationChart(result, booking_type, false)
            })
        },

        onChangeRegistrationType: function (ev){
            var self = this;
            var registration_type = $('[name="registration_type_select"]:checked').val()
            ajax.jsonRpc('/jupiter_dashboard/row_2', 'call', {booking_type: false, registration_type: registration_type, budget_type: false}, {shadow:true}).then(function (result) {
                self.bookingAndRegistrationChart(result, false, registration_type)
            })
        },

        projectOrRegionFlatStatus: function (result, project_wise, region_wise){
            if(region_wise){
                var options = {
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
                            return val
                        }
                    },
                    plotOptions: {
                        bar: {
                            //columnWidth: '40%',
                            borderRadius: 4,
                            dataLabels: {
                                position: 'center', // top, center, bottom
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
                                return val
                            }
                        }
                    },
                    legend: {
                        position: 'bottom',
                        horizontalAlign: 'left'
                    }
                };
                $("#region_wise_flat_status").empty()
                var chart2 = new ApexCharts(document.querySelector("#region_wise_flat_status"), options);
                chart2.render();
            }
            if(project_wise){
                var options = {
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
                            return val
                        }
                    },
                    plotOptions: {
                        bar: {
                            borderRadius: 3,
                            dataLabels: {
                                position: 'center', // top, center, bottom
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
                                return val
                            }
                        }
                    },
                    legend: {
                        position: 'top',
                        horizontalAlign: 'right'
                    }
                };
                $("#project_wise_flat_status").empty()
                var chart2 = new ApexCharts(document.querySelector("#project_wise_flat_status"), options);
                chart2.render();
            }
        },

        regionWiseBooking: function(result){
            var options = {
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
            var chart = new ApexCharts(document.querySelector("#region_wise_booking"), options);
            chart.render();
        },

        bookingAndRegistrationChart: function(result, booking_type, registration_type){
            if(booking_type){
                var options = {
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
                                position: 'top', // top, center, bottom
                            },
                        }
                    },
                    dataLabels: {
                        enabled: true,
                        formatter: function (val) {
                            return (booking_type === 'number') ? val : val.toFixed(2)
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
                            text: (booking_type === 'number') ? 'Count' : 'Value (*In Lakhs)'
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
                                return (booking_type === 'number') ? val : val.toFixed(2)
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
                $("#booking_chart").empty()
                var chart = new ApexCharts(document.querySelector("#booking_chart"), options);
                chart.render();
            }
            if(registration_type){
                var options = {
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
                                position: 'top', // top, center, bottom
                            },
                        }
                    },
                    dataLabels: {
                        enabled: true,
                        formatter: function (val) {
                            return (registration_type === 'number') ? val : val.toFixed(2)
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
                            text: (registration_type === 'number') ? 'Count' : 'Value (*In Lakhs)'
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
                                return (registration_type === 'number') ? val : val.toFixed(2)
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
                $("#registration_chart").empty()
                var chart = new ApexCharts(document.querySelector("#registration_chart"), options);
                chart.render();
            }
        },

        ActualBudgetComparison: function(result){
            var options = {
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
                        colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
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
            $("#booking_vs_budget_chart").empty()
            var chart = new ApexCharts(document.querySelector("#booking_vs_budget_chart"), options);
            chart.render();

            var options = {
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
                        colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
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
            $("#registration_vs_budget_chart").empty()
            var chart = new ApexCharts(document.querySelector("#registration_vs_budget_chart"), options);
            chart.render();
        },

        renderElement: function (ev){
            var self = this;
            $.when(this._super()).then(function (ev) {
                ajax.jsonRpc('/jupiter_dashboard/row_1', 'call', {}, {shadow:true}).then(function (result) {
                    $('#today_booking_gross').empty().append(result['today_booking_gross'])
                    $('#today_booking_cancelled').empty().append(result['today_booking_cancelled'])
                    $('#today_booking_net').empty().append(result['today_booking_net'])
                    $('#week_booking_gross').empty().append(result['week_booking_gross'])
                    $('#week_booking_cancelled').empty().append(result['week_booking_cancelled'])
                    $('#week_booking_net').empty().append(result['week_booking_net'])
                    $('#month_booking_gross').empty().append(result['month_booking_gross'])
                    $('#month_booking_cancelled').empty().append(result['month_booking_cancelled'])
                    $('#month_booking_net').empty().append(result['month_booking_net'])

                    $('#today_registration_count').empty().append(result['today_registration_count'])
                    $('#this_week_registration_count').empty().append(result['this_week_registration_count'])
                    $('#this_month_registration_count').empty().append(result['this_month_registration_count'])
                })
                ajax.jsonRpc('/jupiter_dashboard/get_financial_year_data', 'call', {get_selection: true, fin_year: false}, {shadow:true}).then(function (result) {
                    $('#financial_year_selection').empty().append(result['fin_year_selection'])
                    $('#year_booking_gross').empty().append(result['year_booking_gross'])
                    $('#year_booking_cancelled').empty().append(result['year_booking_cancelled'])
                    $('#year_booking_net').empty().append(result['year_booking_net'])
                    $('#year_registration_count').empty().append(result['year_registration_count'])
                    $('#year_registration_value').empty().append(result['year_registration_value'])
                    $('#year_booking_value').empty().append(result['year_booking_value'])
                    $('.fin_year_string').empty().append(result['fin_year_string'])
                })
                ajax.jsonRpc('/jupiter_dashboard/row_2', 'call', {}, {shadow:true}).then(function (result) {
                    self.bookingAndRegistrationChart(result, 'number', 'number')
                    self.ActualBudgetComparison(result)
                })
                ajax.jsonRpc('/jupiter_dashboard/row_3', 'call', {}, {shadow:true}).then(function (result) {
                    self.regionWiseBooking(result)
                })
                ajax.jsonRpc('/jupiter_dashboard/row_4', 'call', {'region_wise': true, 'project_wise': true, 'project_region': false}, {shadow:true}).then(function (result) {
                    self.projectOrRegionFlatStatus(result, true, true)
                })
                ajax.jsonRpc('/jupiter_dashboard/get_region', 'call', {}, {shadow:true}).then(function (result) {
                    $('#region_selection .dropdown-menu').empty().append(result)
                })
            })
        },
    })
    core.action_registry.add('jupiter_dashboard', JupiterDashboard);
    return JupiterDashboard;
});