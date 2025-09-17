odoo.define('jupiter_dashboard_deux.JupiterDashboardDeux', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var web_client = require('web.web_client');
    var _t = core._t;
    var QWeb = core.qweb;
    var JupiterDashboardDeux = AbstractAction.extend({
        template: 'JupiterDashboardDeux',
        events: {
            'click .report_link': 'linkToReport',
            'click .list_view_link': 'linkToList',
        },

        linkToList: function(ev){
            var self = this;
            var domain = $(ev.currentTarget).attr('domain')
            ajax.jsonRpc('/jupiter_dashboard_deux/call_list_view', 'call',
                {domain: domain, model: $(ev.currentTarget).attr('model'), 'name': $(ev.currentTarget).attr('name')},
                {shadow:true}).then(function (result) {
                self.do_action(result)
            })
        },

        linkToReport: function(ev){
            var self = this;
            var report_attr = JSON.parse($(ev.currentTarget).attr('report_attr').replace(/'/g, '"'))
            if ('consolidate' in report_attr){
                if(report_attr['consolidate'] == 'False'){
                    report_attr['consolidate'] = false
                }else{
                    report_attr['consolidate'] = true
                }
            }
            ajax.jsonRpc('/jupiter_dashboard_deux/call_report', 'call',
                {report_attr: report_attr, model: $(ev.currentTarget).attr('model')},
                {shadow:true}).then(function (result) {
                self.do_action(result)
            })
        },

        applyCpCountChart: function(result){
            var options = {
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
            $("#cp_count_chart").empty()
            var chart = new ApexCharts(document.querySelector("#cp_count_chart"), options);
            chart.render();
        },

        applyCpBookingChart: function(result){
            var options = {
                series: [
                    {
                        name: "Booking",
                        data: result['bookings']
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

            $("#cp_chart").empty()
            var chart = new ApexCharts(document.querySelector("#cp_chart"), options);
            chart.render();
        },

        renderElement: function (ev){
            var self = this;
            $.when(this._super()).then(function (ev) {
                ajax.jsonRpc('/jupiter_dashboard_deux/bookings_registrations', 'call', {}, {shadow:true}).then(function (result) {
                    $('#today_booking_count').empty().append(result['today_booking_count'])
                    $('#week_booking_count').empty().append(result['week_booking_count'])
                    $('#month_booking_count').empty().append(result['month_booking_count'])
                    $('#year_booking_count').empty().append(result['year_booking_count'])
                    $('#quarter_booking_count').empty().append(result['quarter_booking_count'])
                    $('#half_booking_count').empty().append(result['half_booking_count'])

                    $('#today_booking_value').empty().append(result['today_booking_value'])
                    $('#week_booking_value').empty().append(result['week_booking_value'])
                    $('#month_booking_value').empty().append(result['month_booking_value'])
                    $('#year_booking_value').empty().append(result['year_booking_value'])
                    $('#quarter_booking_value').empty().append(result['quarter_booking_value'])
                    $('#half_booking_value').empty().append(result['half_booking_value'])

                    $('#today_registration_count').empty().append(result['today_registration_count'])
                    $('#week_registration_count').empty().append(result['week_registration_count'])
                    $('#month_registration_count').empty().append(result['month_registration_count'])
                    $('#year_registration_count').empty().append(result['year_registration_count'])
                    $('#quarter_registration_count').empty().append(result['quarter_registration_count'])
                    $('#half_registration_count').empty().append(result['half_registration_count'])

                    $('#today_registration_value').empty().append(result['today_registration_value'])
                    $('#week_registration_value').empty().append(result['week_registration_value'])
                    $('#month_registration_value').empty().append(result['month_registration_value'])
                    $('#year_registration_value').empty().append(result['year_registration_value'])
                    $('#quarter_registration_value').empty().append(result['quarter_registration_value'])
                    $('#half_registration_value').empty().append(result['half_registration_value'])

                    $('#today_booking_link').attr('report_attr', result['today_booking_attrs']);
                    $('#week_booking_link').attr('report_attr', result['week_booking_attrs']);
                    $('#month_booking_link').attr('report_attr', result['month_booking_attrs']);
                    $('#year_booking_link').attr('report_attr', result['year_booking_attrs']);
                    $('#quarter_booking_link').attr('report_attr', result['quarter_booking_attrs']);
                    $('#half_booking_link').attr('report_attr', result['half_booking_attrs']);

                    $('.today_registration_link').attr('report_attr', result['today_registration_attrs']);
                    $('.week_registration_link').attr('report_attr', result['week_registration_attrs']);
                    $('.month_registration_link').attr('report_attr', result['month_registration_attrs']);
                    $('.year_registration_link').attr('report_attr', result['year_registration_attrs']);
                    $('.quarter_registration_link').attr('report_attr', result['quarter_registration_attrs']);
                    $('.half_registration_link').attr('report_attr', result['half_registration_attrs']);

                    $('#today_booking_cancelled_count').empty().append(result['today_booking_cancelled_count'])
                    $('#week_booking_cancelled_count').empty().append(result['week_booking_cancelled_count'])
                    $('#month_booking_cancelled_count').empty().append(result['month_booking_cancelled_count'])
                    $('#year_booking_cancelled_count').empty().append(result['year_booking_cancelled_count'])
                    $('#quarter_booking_cancelled_count').empty().append(result['quarter_booking_cancelled_count'])
                    $('#half_booking_cancelled_count').empty().append(result['half_booking_cancelled_count'])

                    $('#today_booking_cancelled_value').empty().append(result['today_booking_cancelled_value'])
                    $('#week_booking_cancelled_value').empty().append(result['week_booking_cancelled_value'])
                    $('#month_booking_cancelled_value').empty().append(result['month_booking_cancelled_value'])
                    $('#year_booking_cancelled_value').empty().append(result['year_booking_cancelled_value'])
                    $('#quarter_booking_cancelled_value').empty().append(result['quarter_booking_cancelled_value'])
                    $('#half_booking_cancelled_value').empty().append(result['half_booking_cancelled_value'])

                    $('#today_booking_cancelled_link').attr('report_attr', result['today_booking_cancelled_attrs']);
                    $('#week_booking_cancelled_link').attr('report_attr', result['week_booking_cancelled_attrs']);
                    $('#month_booking_cancelled_link').attr('report_attr', result['month_booking_cancelled_attrs']);
                    $('#year_booking_cancelled_link').attr('report_attr', result['year_booking_cancelled_attrs']);
                    $('#quarter_booking_cancelled_link').attr('report_attr', result['quarter_booking_cancelled_attrs']);
                    $('#half_booking_cancelled_link').attr('report_attr', result['half_booking_cancelled_attrs']);

                    $('.quarter_label').empty().append(result['quarter_label'])
                    $('.half_label').empty().append(result['half_label'])
                    $('.year_label').empty().append(result['year_label'])

                    $('#today_booking_cp_count').empty().append(result['today_booking_cp_count'])
                    $('#week_booking_cp_count').empty().append(result['week_booking_cp_count'])
                    $('#month_booking_cp_count').empty().append(result['month_booking_cp_count'])
                    $('#year_booking_cp_count').empty().append(result['year_booking_cp_count'])
                    $('#quarter_booking_cp_count').empty().append(result['quarter_booking_cp_count'])
                    $('#half_booking_cp_count').empty().append(result['half_booking_cp_count'])

                    $('#today_booking_cp_domain').attr('domain', result['today_booking_cp_domain']);
                    $('#week_booking_cp_domain').attr('domain', result['week_booking_cp_domain']);
                    $('#month_booking_cp_domain').attr('domain', result['month_booking_cp_domain']);
                    $('#quarter_booking_cp_domain').attr('domain', result['quarter_booking_cp_domain']);
                    $('#half_booking_cp_domain').attr('domain', result['half_booking_cp_domain']);
                    $('#year_booking_cp_domain').attr('domain', result['year_booking_cp_domain']);

                    $('#today_direct').empty().append(result['today_direct'])
                    $('#week_direct').empty().append(result['week_direct'])
                    $('#month_direct').empty().append(result['month_direct'])
                    $('#year_direct').empty().append(result['year_direct'])
                    $('#quarter_direct').empty().append(result['quarter_direct'])
                    $('#half_direct').empty().append(result['half_direct'])

                    $('#today_direct_domain').attr('domain', result['today_direct_domain']);
                    $('#week_direct_domain').attr('domain', result['week_direct_domain']);
                    $('#month_direct_domain').attr('domain', result['month_direct_domain']);
                    $('#quarter_direct_domain').attr('domain', result['quarter_direct_domain']);
                    $('#half_direct_domain').attr('domain', result['half_direct_domain']);
                    $('#year_direct_domain').attr('domain', result['year_direct_domain']);

                    $('#today_average_av').empty().append(result['today_average_av'])
                    $('#week_average_av').empty().append(result['week_average_av'])
                    $('#month_average_av').empty().append(result['month_average_av'])
                    $('#quarter_average_av').empty().append(result['quarter_average_av'])
                    $('#half_average_av').empty().append(result['half_average_av'])
                    $('#year_average_av').empty().append(result['year_average_av'])
                })
                ajax.jsonRpc('/jupiter_dashboard_deux/collections_billings', 'call', {}, {shadow:true}).then(function (result) {
                    $('#today_collection').empty().append(result['today_collection'])
                    $('#week_collection').empty().append(result['week_collection'])
                    $('#month_collection').empty().append(result['month_collection'])
                    $('#year_collection').empty().append(result['year_collection'])
                    $('#quarter_collection').empty().append(result['quarter_collection'])
                    $('#half_collection').empty().append(result['half_collection'])

                    $('#today_billing').empty().append(result['today_billing'])
                    $('#week_billing').empty().append(result['week_billing'])
                    $('#month_billing').empty().append(result['month_billing'])
                    $('#year_billing').empty().append(result['year_billing'])
                    $('#quarter_billing').empty().append(result['quarter_billing'])
                    $('#half_billing').empty().append(result['half_billing'])

                    $('#today_billing_attrs').attr('report_attr', result['today_billing_attrs']);
                    $('#week_billing_attrs').attr('report_attr', result['week_billing_attrs']);
                    $('#month_billing_attrs').attr('report_attr', result['month_billing_attrs']);
                    $('#quarter_billing_attrs').attr('report_attr', result['quarter_billing_attrs']);
                    $('#half_billing_attrs').attr('report_attr', result['half_billing_attrs']);
                    $('#year_billing_attrs').attr('report_attr', result['year_billing_attrs']);

                    $('#today_collection_attr').attr('domain', result['today_collection_domain']);
                    $('#week_collection_attr').attr('domain', result['week_collection_domain']);
                    $('#month_collection_attr').attr('domain', result['month_collection_domain']);
                    $('#quarter_collection_attr').attr('domain', result['quarter_collection_domain']);
                    $('#half_collection_attr').attr('domain', result['half_collection_domain']);
                    $('#year_collection_attr').attr('domain', result['year_collection_domain']);

                })
                ajax.jsonRpc('/jupiter_dashboard_deux/get_last_6_month_cp_booking', 'call', {}, {shadow:true}).then(function (result) {
                    self.applyCpBookingChart(result)
                })
                ajax.jsonRpc('/jupiter_dashboard_deux/get_cp_count', 'call', {}, {shadow:true}).then(function (result) {
                    $('#month_cps').empty().append(result['month_cps'])
                    $('#quarter_cps').empty().append(result['quarter_cps'])
                    $('#half_cps').empty().append(result['half_cps'])
                    $('#year_cps').empty().append(result['year_cps'])

                    $('#month_cps_active').empty().append(result['month_cps_active'])
                    $('#quarter_cps_active').empty().append(result['quarter_cps_active'])
                    $('#half_cps_active').empty().append(result['half_cps_active'])
                    $('#year_cps_active').empty().append(result['year_cps_active'])

                    $('#month_cp_domain').attr('domain', result['month_cp_domain']);
                    $('#quarter_cp_domain').attr('domain', result['quarter_cp_domain']);
                    $('#half_cp_domain').attr('domain', result['half_cp_domain']);
                    $('#year_cp_domain').attr('domain', result['year_cp_domain']);

                    $('#month_cp_active_domain').attr('domain', result['month_cp_active_domain']);
                    $('#quarter_cp_active_domain').attr('domain', result['quarter_cp_active_domain']);
                    $('#half_cp_active_domain').attr('domain', result['half_cp_active_domain']);
                    $('#year_cp_active_domain').attr('domain', result['year_cp_active_domain']);
                    self.applyCpCountChart(result)
                })
                $(document).ready(function() {
                    try{
                        // Get the horizontal scroll container
                        const container = document.getElementById('horizontal-scroll-container');

                        let isDragging = false;
                        let startX;
                        let scrollLeft;

                        // Get the arrow elements
                        const leftArrow = document.querySelector('.left-arrow');
                        const rightArrow = document.querySelector('.right-arrow');

                        // Get the width of a single flex-scroll-item
                        var single_flex_scroll_item = document.querySelector('.flex-scroll-item')
                        if(single_flex_scroll_item){
                            var itemWidth = document.querySelector('.flex-scroll-item').offsetWidth + 10;
                        }else{
                            var itemWidth = 1000
                        }
                        container.addEventListener('wheel', (e) => {
                            // Check if the Shift key is pressed
                            if (e.shiftKey) {
                                e.preventDefault();
                                smoothScroll(container.scrollLeft + e.deltaY * 2); // Adjust multiplier for scroll speed
                            }
                        });

                        // Arrow click events
                        leftArrow.addEventListener('click', () => {
                            smoothScroll(container.scrollLeft - itemWidth);
                            updateArrowVisibility();
                        });

                        rightArrow.addEventListener('click', () => {
                            smoothScroll(container.scrollLeft + itemWidth);
                            updateArrowVisibility();
                        });

                        // Mouse down event
                        container.addEventListener('mousedown', (e) => {
                            isDragging = true;
                            container.classList.add('active');
                            container.classList.add('grabbing');
                            startX = e.pageX - container.offsetLeft;
                            scrollLeft = container.scrollLeft;
                        });

                        // Mouse up event
                        container.addEventListener('mouseup', () => {
                            isDragging = false;
                            container.classList.remove('active');
                            container.classList.remove('grabbing');
                            updateArrowVisibility();
                        });

                        // Mouse move event
                        container.addEventListener('mousemove', (e) => {
                            if (!isDragging) return;
                            e.preventDefault();
                            const x = e.pageX - container.offsetLeft;
                            const walk = (x - startX) * 3;
                            smoothScroll(scrollLeft - walk);
                        });

                        // Mouse leave event
                        container.addEventListener('mouseleave', () => {
                            if (isDragging) {
                                isDragging = false;
                                container.classList.remove('active');
                                container.classList.remove('grabbing');
                                updateArrowVisibility();
                            }
                        });

                        // Smooth scroll function
                        function smoothScroll(targetX) {
                            let start = container.scrollLeft;
                            let change = targetX - start;
                            let currentTime = 0;
                            let increment = 20; // Adjust increment for smoother or faster scrolling
                            let duration = 300; // Adjust duration for slower or faster scrolling

                            function animateScroll() {
                                currentTime += increment;
                                let val = Math.easeInOutQuad(currentTime, start, change, duration);
                                container.scrollLeft = val;
                                if (currentTime < duration) {
                                    requestAnimationFrame(animateScroll);
                                } else {
                                    updateArrowVisibility(); // Update arrow visibility at the end of scrolling
                                }
                            }
                            animateScroll();
                        }

                        // Easing function
                        Math.easeInOutQuad = function (t, b, c, d) {
                            t /= d / 2;
                            if (t < 1) return c / 2 * t * t + b;
                            t--;
                            return -c / 2 * (t * (t - 2) - 1) + b;
                        };

                        // Function to update arrow visibility
                        function updateArrowVisibility() {
                            leftArrow.style.display = container.scrollLeft <= 0 ? 'none' : 'block';
                            rightArrow.style.display = container.scrollLeft + container.clientWidth >= container.scrollWidth ? 'none' : 'block';
                        }

                        // Initial arrow visibility
                        updateArrowVisibility();
                    }catch(e){}
                })
            })
        },
    })
    core.action_registry.add('jupiter_dashboard_deux', JupiterDashboardDeux);
    return JupiterDashboardDeux;
});