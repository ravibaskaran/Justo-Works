/** @odoo-module **/

import { Component, onMounted, onWillUnmount, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class JupiterDashboardTres extends Component {
    static template = "JupiterDashboardTres";

    setup() {
        this.rpc = useService("rpc");
        this.action = useService("action");
        this.charts = {};  // Store chart instances
        this.eventListeners = [];  // Track for cleanup
        onMounted(() => this.onMounted());
        onWillUnmount(() => this.onWillUnmount());
    }

    setupEventListeners() {
        // Convert event handlers to addEventListener
        // click .region-blocks
        this.el.querySelectorAll('.region-blocks').forEach(el => {
            const handler = this.changeRegion.bind(this);
            el.addEventListener('click', handler);
            this.eventListeners.push({ element: el, event: 'click', handler });
        });

        // click .region-blocks2
        this.el.querySelectorAll('.region-blocks2').forEach(el => {
            const handler = this.changeRegion2.bind(this);
            el.addEventListener('click', handler);
            this.eventListeners.push({ element: el, event: 'click', handler });
        });

        // click .cluster-blocks
        this.el.querySelectorAll('.cluster-blocks').forEach(el => {
            const handler = this.changeCluster.bind(this);
            el.addEventListener('click', handler);
            this.eventListeners.push({ element: el, event: 'click', handler });
        });

        // click .project-blocks
        this.el.querySelectorAll('.project-blocks').forEach(el => {
            const handler = this.changeProject.bind(this);
            el.addEventListener('click', handler);
            this.eventListeners.push({ element: el, event: 'click', handler });
        });

        // change .region_wise_radio
        this.el.querySelectorAll('.region_wise_radio').forEach(el => {
            const handler = this.changeRadioRegionWise.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change .region_wise_radio2
        this.el.querySelectorAll('.region_wise_radio2').forEach(el => {
            const handler = this.changeRadioRegionWise2.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change .cluster_wise_radio
        this.el.querySelectorAll('.cluster_wise_radio').forEach(el => {
            const handler = this.changeRadioClusterWise.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change .project_wise_radio
        this.el.querySelectorAll('.project_wise_radio').forEach(el => {
            const handler = this.changeRadioProjectWise.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #region_wise_booking_select
        this.el.querySelectorAll('#region_wise_booking_select').forEach(el => {
            const handler = this.changeRegionWiseSelect.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #cluster_wise_booking_select
        this.el.querySelectorAll('#cluster_wise_booking_select').forEach(el => {
            const handler = this.changeClusterWiseSelect.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #project_wise_booking_select
        this.el.querySelectorAll('#project_wise_booking_select').forEach(el => {
            const handler = this.changeProjectWiseSelect.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change .region-radio-input
        this.el.querySelectorAll('.region-radio-input').forEach(el => {
            const handler = this.changeRadioRegionWise.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change .region-radio-input2
        this.el.querySelectorAll('.region-radio-input2').forEach(el => {
            const handler = this.changeRadioRegionWise2.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change .cluster-radio-input
        this.el.querySelectorAll('.cluster-radio-input').forEach(el => {
            const handler = this.changeRadioClusterWise.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change .project-radio-input
        this.el.querySelectorAll('.project-radio-input').forEach(el => {
            const handler = this.changeRadioProjectWise.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change .region_select
        this.el.querySelectorAll('.region_select').forEach(el => {
            const handler = this.changeRegionSelect.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change .cluster_checkbox
        this.el.querySelectorAll('.cluster_checkbox').forEach(el => {
            const handler = this.changeClusterCheckbox.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // click #region_selection .dropdown-item
        this.el.querySelectorAll('#region_selection .dropdown-item').forEach(el => {
            const handler = this.onChangeRegion.bind(this);
            el.addEventListener('click', handler);
            this.eventListeners.push({ element: el, event: 'click', handler });
        });

        // change .configuration_select
        this.el.querySelectorAll('.configuration_select').forEach(el => {
            const handler = this.onChangeConfiguration.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change .cluster_select
        this.el.querySelectorAll('.cluster_select').forEach(el => {
            const handler = this.onChangeConfiguration.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #region_select_all
        this.el.querySelectorAll('#region_select_all').forEach(el => {
            const handler = this.onChangeRegionSelectAll.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #region_select_all2
        this.el.querySelectorAll('#region_select_all2').forEach(el => {
            const handler = this.onChangeRegionSelectAll2.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #cluster_select_all
        this.el.querySelectorAll('#cluster_select_all').forEach(el => {
            const handler = this.onChangeClusterSelectAll.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #cluster_select_all2
        this.el.querySelectorAll('#cluster_select_all2').forEach(el => {
            const handler = this.onChangeClusterSelectAll2.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #project_select_all
        this.el.querySelectorAll('#project_select_all').forEach(el => {
            const handler = this.onChangeProjectSelectAll.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #project_select_all2
        this.el.querySelectorAll('#project_select_all2').forEach(el => {
            const handler = this.onChangeProjectSelectAll2.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // click #walk_in_region_selection .dropdown-item
        this.el.querySelectorAll('#walk_in_region_selection .dropdown-item').forEach(el => {
            const handler = this.onChangeWalkInRegion.bind(this);
            el.addEventListener('click', handler);
            this.eventListeners.push({ element: el, event: 'click', handler });
        });

        // change .walk_in_cluster_select
        this.el.querySelectorAll('.walk_in_cluster_select').forEach(el => {
            const handler = this.onChangeWalkInCluster.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // click .report_link
        this.el.querySelectorAll('.report_link').forEach(el => {
            const handler = this.linkToReport.bind(this);
            el.addEventListener('click', handler);
            this.eventListeners.push({ element: el, event: 'click', handler });
        });

        // click .list_view_link
        this.el.querySelectorAll('.list_view_link').forEach(el => {
            const handler = this.linkToList.bind(this);
            el.addEventListener('click', handler);
            this.eventListeners.push({ element: el, event: 'click', handler });
        });

        // change #custom_date_range
        this.el.querySelectorAll('#custom_date_range').forEach(el => {
            const handler = this.onChangeCustomDateRange.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #manpower_date_from
        this.el.querySelectorAll('#manpower_date_from').forEach(el => {
            const handler = this.onChangeManPowerDate.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #manpower_date_to
        this.el.querySelectorAll('#manpower_date_to').forEach(el => {
            const handler = this.onChangeManPowerDate.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #custom_date_range_booking_registration
        this.el.querySelectorAll('#custom_date_range_booking_registration').forEach(el => {
            const handler = this.onChangeCustomDateRangeBookingRegistration.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #custom_date_range_booking_registration2
        this.el.querySelectorAll('#custom_date_range_booking_registration2').forEach(el => {
            const handler = this.onChangeCustomDateRangeBookingRegistration2.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #booking_registrations_date_from
        this.el.querySelectorAll('#booking_registrations_date_from').forEach(el => {
            const handler = this.changeRadioRegionWise.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #booking_registrations_date_from2
        this.el.querySelectorAll('#booking_registrations_date_from2').forEach(el => {
            const handler = this.changeRadioRegionWise2.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #booking_registrations_date_to
        this.el.querySelectorAll('#booking_registrations_date_to').forEach(el => {
            const handler = this.changeRadioRegionWise.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #booking_registrations_date_to2
        this.el.querySelectorAll('#booking_registrations_date_to2').forEach(el => {
            const handler = this.changeRadioRegionWise2.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #custom_date_range_cluster_booking_registration
        this.el.querySelectorAll('#custom_date_range_cluster_booking_registration').forEach(el => {
            const handler = this.onChangeCustomDateRangeClusterBookingRegistration.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #cluster_booking_registrations_date_from
        this.el.querySelectorAll('#cluster_booking_registrations_date_from').forEach(el => {
            const handler = this.changeRadioClusterWise.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #cluster_booking_registrations_date_to
        this.el.querySelectorAll('#cluster_booking_registrations_date_to').forEach(el => {
            const handler = this.changeRadioClusterWise.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #custom_date_range_project_booking_registration
        this.el.querySelectorAll('#custom_date_range_project_booking_registration').forEach(el => {
            const handler = this.onChangeCustomDateRangeProjectBookingRegistration.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #project_booking_registrations_date_from
        this.el.querySelectorAll('#project_booking_registrations_date_from').forEach(el => {
            const handler = this.changeRadioProjectWise.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #project_booking_registrations_date_to
        this.el.querySelectorAll('#project_booking_registrations_date_to').forEach(el => {
            const handler = this.changeRadioProjectWise.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #custom_date_range_cp_booking
        this.el.querySelectorAll('#custom_date_range_cp_booking').forEach(el => {
            const handler = this.onChangeCustomDateRangeCpBooking.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #cp_booking_date_from
        this.el.querySelectorAll('#cp_booking_date_from').forEach(el => {
            const handler = this.onChangeCpUnitRegionWiseRadio.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #cp_booking_date_to
        this.el.querySelectorAll('#cp_booking_date_to').forEach(el => {
            const handler = this.onChangeCpUnitRegionWiseRadio.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #custom_date_range_top_20_cp
        this.el.querySelectorAll('#custom_date_range_top_20_cp').forEach(el => {
            const handler = this.onChangeCustomDateRangeTop20Cp.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #top_20_cp_date_from
        this.el.querySelectorAll('#top_20_cp_date_from').forEach(el => {
            const handler = this.onChangeCP20Radio.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

        // change #top_20_cp_date_to
        this.el.querySelectorAll('#top_20_cp_date_to').forEach(el => {
            const handler = this.onChangeCP20Radio.bind(this);
            el.addEventListener('change', handler);
            this.eventListeners.push({ element: el, event: 'change', handler });
        });

    }

    onWillUnmount() {
        // Destroy all chart instances
        Object.values(this.charts).forEach(chart => {
            if (chart && chart.destroy) {
                chart.destroy();
            }
        });
        // Remove event listeners
        this.eventListeners.forEach(({ element, event, handler }) => {
            if (element) element.removeEventListener(event, handler);
        });
    }

                    onChangeCustomDateRangeTop20Cp: function(ev){
                var custom_range = $('#custom_date_range_top_20_cp').prop('checked')
                if (custom_range){
                    $('#top_20_cp_date_fields').show()
                    document.getElementById('top_20_cp_date_selectors').style.setProperty('display', 'none', 'important');
                    this.onChangeCP20Radio()
                }else{
                    document.getElementById('top_20_cp_date_selectors').style.setProperty('display', 'flex', 'important');
                    $('#top_20_cp_date_fields').hide()
                    this.onChangeCP20Radio()
                }
            },

            onChangeCustomDateRangeCpBooking: function(ev){
                var custom_range = $('#custom_date_range_cp_booking').prop('checked')
                if (custom_range){
                    $('#cp_booking_date_fields').show()
                    document.getElementById('cp_booking_date_selectors').style.setProperty('display', 'none', 'important');
                    this.onChangeCpUnitRegionWiseRadio()
                }else{
                    document.getElementById('cp_booking_date_selectors').style.setProperty('display', 'flex', 'important');
                    $('#cp_booking_date_fields').hide()
                    this.onChangeCpUnitRegionWiseRadio()
                }
            },

            onChangeCustomDateRangeProjectBookingRegistration: function(ev){
                var custom_range = $('#custom_date_range_project_booking_registration').prop('checked')
                if (custom_range){
                    $('#project_booking_registrations_date_fields').show()
                    $('#project_booking_registrations_date_selectors').hide()
                    this.changeRadioProjectWise()
                }else{
                    $('#project_booking_registrations_date_selectors').show()
                    $('#project_booking_registrations_date_fields').hide()
                    this.changeRadioProjectWise()
                }
            },

            onChangeCustomDateRangeClusterBookingRegistration: function(ev){
                var custom_range = $('#custom_date_range_cluster_booking_registration').prop('checked')
                if (custom_range){
                    $('#cluster_booking_registrations_date_fields').show()
                    $('#cluster_booking_registrations_date_selectors').hide()
                    this.changeRadioClusterWise()
                }else{
                    $('#cluster_booking_registrations_date_selectors').show()
                    $('#cluster_booking_registrations_date_fields').hide()
                    this.changeRadioClusterWise()
                }
            },

            onChangeCustomDateRangeBookingRegistration: function(ev){
                var custom_range = $('#custom_date_range_booking_registration').prop('checked')
                if (custom_range){
                    $('#booking_registrations_date_fields').show()
                    $('#booking_registrations_date_selectors').hide()
                    this.changeRadioRegionWise()
                }else{
                    $('#booking_registrations_date_selectors').show()
                    $('#booking_registrations_date_fields').hide()
                    this.changeRadioRegionWise()
                }
            },
    //        Graph 2
            onChangeCustomDateRangeBookingRegistration2: function(ev){
                var custom_range = $('#custom_date_range_booking_registration2').prop('checked')
                if (custom_range){
                    $('#booking_registrations_date_fields').show()
                    $('#booking_registrations_date_selectors').hide()
                    this.changeRadioRegionWise2()
                }else{
                    $('#booking_registrations_date_selectors').show()
                    $('#booking_registrations_date_fields').hide()
                    this.changeRadioRegionWise2()
                }
            },

            onChangeManPowerDate: function(ev){
                var self = this;
                var date_from = $('#manpower_date_from').val()
                var date_to = $('#manpower_date_to').val()
                var count_or_value = $('[name="manpower_count_or_value"]:checked').val()
                $('.manpower_loader').removeClass('invisible')
                this.rpc("/jupiter_dashboard_tres/manpower_productivity", {frequency: false, count_or_value: count_or_value, date_from, date_to}).then((result) => {
    //                self.ManPowerProductivityRadialChart(result[0])
                    $('#man_power_radial_chart').empty().append(result[0])
                    self.ManPowerProductivityRegionChart(result[1])
                    self.ManPowerProductivityClusterChart(result[2])
                    $('#manpower_project_tbody').empty().append(result[3])
                    $('.manpower_loader').addClass('invisible')
                })
            },

            onChangeCustomDateRange: function(ev){
                var custom_range = $('#custom_date_range').prop('checked')
                if (custom_range){
                    $('#manpower_date_fields').show()
                    $('#manpower_date_selectors').hide()
                    this.onChangeManPowerDate()
                }else{
                    $('#manpower_date_selectors').show()
                    $('#manpower_date_fields').hide()
                    this.manPowerRadioRadio()
                }
            },

            linkToList: function(ev){
                var self = this;
                var domain = $(ev.currentTarget).attr('domain')
                if ($(ev.currentTarget).closest('.active-dormant').length > 0){
                    if($('[name="cp-active-dormant"]:checked').val() == 'active'){
                        domain = $(ev.currentTarget).attr('active_domain')
                    }else{
                        domain = $(ev.currentTarget).attr('dormant_domain')
                    }
                }
                this.rpc("/jupiter_dashboard_tres/call_list_view", {domain: domain, model: $(ev.currentTarget).attr('model'), 'name': $(ev.currentTarget).attr('name')}).then((result) => {
                    this.action.doAction(result)
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
                var region_ids = []
                if($(ev.target).closest('.region-row').length > 0 && ($('.region-blocks').not('.active').length > 0 || $('.region-blocks').length == 0)){
                    region_ids = [.01]
                    $('.region-blocks').each(function(i, obj) {
                        if($(obj).hasClass('active')){
                            region_ids.push(parseInt($(obj).attr('region_id')))
                        }
                    })
                }
                var cluster_ids = []
                if($(ev.target).closest('.cluster-row').length > 0 && ($('.cluster-blocks').not('.active').length > 0 || $('.cluster-blocks').length == 0)){
                    cluster_ids = [.01]
                    $('.cluster-blocks').each(function(i, obj) {
                        if($(obj).hasClass('active')){
                            cluster_ids.push(parseInt($(obj).attr('cluster_id')))
                        }
                    })
                }
                var project_ids = []
                if($(ev.target).closest('.project-row').length > 0 && ($('.project-blocks').not('.active').length > 0 || $('.project-blocks').length == 0)){
                    project_ids = [.01]
                    $('.project-blocks').each(function(i, obj) {
                        if($(obj).hasClass('active')){
                            project_ids.push(parseInt($(obj).attr('project_id')))
                        }
                    })
                }
                this.rpc("/jupiter_dashboard_tres/call_report", {report_attr: report_attr, model: $(ev.currentTarget).attr('model'), region_ids: region_ids, cluster_ids: cluster_ids, project_ids: project_ids}).then((result) => {

                    result.context = result.context || {};
                    result.context.hide_loading_gif = false;

                    this.action.doAction(result)
                })
            },

            manPowerRadioRadio: function(ev){
                var self = this;
                var custom_range = $('#custom_date_range').prop('checked')
                if (custom_range){
                    self.onChangeManPowerDate()
                }else{
                    var frequency = $('[name="manpower_radio"]:checked').val()
                    var count_or_value = $('[name="manpower_count_or_value"]:checked').val()
                    if (count_or_value == 'count'){
                        $('#manpower_in_lack').hide()
                    }else{
                        $('#manpower_in_lack').show()
                    }
                    $('.manpower_loader').removeClass('invisible')
                    this.rpc("/jupiter_dashboard_tres/manpower_productivity", {frequency: frequency, count_or_value: count_or_value}).then((result) => {
            //                self.ManPowerProductivityRadialChart(result[0])
                        $('#man_power_radial_chart').empty().append(result[0])
                        self.ManPowerProductivityRegionChart(result[1])
                        self.ManPowerProductivityClusterChart(result[2])
                        $('#manpower_project_tbody').empty().append(result[3])
                        $('.manpower_loader').addClass('invisible')
                    })
                }
            },

            onChangeCpUnitRegionWiseRadio: function(ev){
                var self = this;
                var frequency = $('[name="cp_units_region_wise_radio"]:checked').val()
                var model = $('[name="cp_units_region_wise_select"]:checked').val()
                if(model == 'region'){
                    var label = 'Region'
                }else{
                    var label = 'Cluster'
                }
                var custom_range = $('#custom_date_range_cp_booking').prop('checked')
                var custom_start = false
                var custom_end = false
                if(custom_range){
                    custom_start = $('#cp_booking_date_from').val()
                    custom_end = $('#cp_booking_date_to').val()
                }
                this.rpc("/jupiter_dashboard_tres/cp_booking_units_region_wise", {'model': model, 'frequency': frequency, 'custom_start': custom_start, 'custom_end': custom_end}).then((result) => {
                    self.CpBookingUnitsRegionWise(result, label)
                })
            },

            onChangeWalkInCluster: function(ev){
                var self = this;
                var frequency = $('[name="walk_in_conversion_radio"]:checked').val()
                var model = $('[name="walk_in_select"]:checked').val()

                var region = $('#walk_in_region_selection').attr('region_id') || false
                var cluster_ids = []
                for(var option of document.getElementById('walk_in_cluster_select').options){
                    if (option.selected){
                        cluster_ids.push(parseInt(option.getAttribute('cluster_id')))
                    }
                }
                $('#walk_in_project_loader').show()
                $('.walk_in_project_div table').css({'filter': 'blur(4px)'})
                this.rpc("/jupiter_dashboard_tres/walk_in_data", {'model': 'project', 'frequency': frequency, 'region': region, 'cluster': cluster_ids}).then((result) => {
                    $('#walk_in_project_tbody').empty().append(result)
                    $('#walk_in_project_loader').hide()
                    $('.walk_in_project_div table').css({'filter': 'unset'})
                })
            },

            onChangeWalkInRegion: function(ev){
                var self = this;
                var frequency = $('[name="walk_in_conversion_radio"]:checked').val()
                var region = $(ev.target).attr('value') || false
                $('#walk_in_region_selection button').empty().append($(ev.target).text())
                $('#walk_in_region_selection button').attr('region_id', region)

                var cluster_ids = []
                for(var option of document.getElementById('walk_in_cluster_select').options){
                    if (option.selected){
                        cluster_ids.push(parseInt(option.getAttribute('cluster_id')))
                    }
                }
                $('#walk_in_project_loader').show()
                $('.walk_in_project_div table').css({'filter': 'blur(4px)'})
                this.rpc("/jupiter_dashboard_tres/walk_in_data", {'model': 'project', 'frequency': frequency, 'region': region, 'cluster': cluster_ids}).then((result) => {
                    $('#walk_in_project_tbody').empty().append(result)
                    $('#walk_in_project_loader').hide()
                    $('.walk_in_project_div table').css({'filter': 'unset'})
                })
                this.rpc("/jupiter_dashboard_tres/walk_in_get_cluster", {region: region}).then((result) => {
                    $('#walk_in_cluster_select_div').empty().append(result)
                    $('#walk_in_cluster_select').select2()
                })
            },

            onChangeWalkInRegionClusterRadio: function(ev){
                var self = this;
                var frequency = $('[name="walk_in_conversion_radio"]:checked').val()
                var model = $('[name="walk_in_select"]:checked').val()
                if(model == 'region'){
                    $('#walk_in_region_header').empty().append('Region')
                }else{
                    $('#walk_in_region_header').empty().append('Cluster')
                }
                $('#walk_in_region_loader').show()
                $('#walk_in_region_wise').css({'filter': 'blur(4px)'})
                this.rpc("/jupiter_dashboard_tres/walk_in_data", {'model': model, 'frequency': frequency}).then((result) => {
                    self.WalkInRegionWise(result)
                    $('#walk_in_region_loader').hide()
                    $('#walk_in_region_wise').css({'filter': 'unset'})
                })
            },

            onChangeWalkInRadio: function(ev){
                var self = this;
                var frequency = $('[name="walk_in_conversion_radio"]:checked').val()
                var model = $('[name="walk_in_select"]:checked').val()
                $('#walk_in_region_loader').show()
                $('#walk_in_region_wise').css({'filter': 'blur(4px)'})
                this.rpc("/jupiter_dashboard_tres/walk_in_data", {'model': model, 'frequency': frequency}).then((result) => {
                    self.WalkInRegionWise(result)
                    $('#walk_in_region_loader').hide()
                    $('#walk_in_region_wise').css({'filter': 'unset'})
                })

                var region = $('#walk_in_region_selection').attr('region_id') || false
                var cluster_ids = []
                for(var option of document.getElementById('walk_in_cluster_select').options){
                    if (option.selected){
                        cluster_ids.push(parseInt(option.getAttribute('cluster_id')))
                    }
                }
                $('#walk_in_project_loader').show()
                $('.walk_in_project_div table').css({'filter': 'blur(4px)'})
                this.rpc("/jupiter_dashboard_tres/walk_in_data", {'model': 'project', 'frequency': frequency, 'region': region, 'cluster': cluster_ids}).then((result) => {
                    $('#walk_in_project_tbody').empty().append(result)
                    $('#walk_in_project_loader').hide()
                    $('.walk_in_project_div table').css({'filter': 'unset'})
                })
            },

            onChangeCP20Radio: function(ev){
                var frequency = $('[name="cp_20_radio"]:checked').val()
                var custom_range = $('#custom_date_range_top_20_cp').prop('checked')
                var custom_start = false
                var custom_end = false
                if(custom_range){
                    custom_start = $('#top_20_cp_date_from').val()
                    custom_end = $('#top_20_cp_date_to').val()
                }
                this.rpc("/jupiter_dashboard_tres/get_top_20_cp", {'frequency': frequency, 'custom_start': custom_start, 'custom_end': custom_end}).then((result) => {
                    $('#cp_tbody').empty().append(result)
                })
            },

            onChangeProjectSelectAll: function(ev){
                if($('#project_select_all').prop('checked')){
                    $('.project-blocks').addClass('active')
                    this.changeProject()
                }else{
                    $('.project-blocks').removeClass('active')
                    this.changeProject()
                }
            },

            onChangeClusterSelectAll: function(ev){
                if($('#cluster_select_all').prop('checked')){
                    $('.cluster-blocks').addClass('active')
                    $('#project_select_all').prop('checked', true)
                    this.changeCluster()
                }else{
                    $('.cluster-blocks').removeClass('active')
                    $('#project_select_all').prop('checked', false)
                    this.changeCluster()
                }
            },

            onChangeRegionSelectAll: function(ev){
                if($('#region_select_all').prop('checked')){
                    $('.region-blocks').addClass('active')
                    $('#cluster_select_all').prop('checked', true)
                    $('#project_select_all').prop('checked', true)
                    $('#region_select_all2').prop('checked', true)
                    this.onChangeRegionSelectAll2(ev);
                    this.changeRegion()
                }else{
                    $('.region-blocks').removeClass('active')
                    $('#cluster_select_all').prop('checked', false)
                    $('#project_select_all').prop('checked', false)
                    $('#region_select_all2').prop('checked', false)
                    this.onChangeRegionSelectAll2(ev);
                    this.changeRegion()
                }
            },

    //        Graph 2
            onChangeRegionSelectAll2: function(ev){
                if($('#region_select_all2').prop('checked')){
                    $('.region-blocks2').addClass('active')
                    $('#cluster_select_all2').prop('checked', true)
                    $('#project_select_all2').prop('checked', true)
                    this.changeRegion2()
                }else{
                    $('.region-blocks2').removeClass('active')
                    $('#cluster_select_all2').prop('checked', false)
                    $('#project_select_all2').prop('checked', false)
                    this.changeRegion2()
                }
            },


            onChangeConfiguration: function(ev){
                var self = this;
                var configuration_ids = []
                for(var option of document.getElementById('configuration_select').options){
                    if (option.selected){
                        configuration_ids.push(parseInt(option.getAttribute('configuration_id')))
                    }
                }
                var cluster_ids = []
                for(var option of document.getElementById('cluster_select').options){
                    if (option.selected){
                        cluster_ids.push(parseInt(option.getAttribute('cluster_id')))
                    }
                }
                var region = $('#region_selection button').attr('region_id') || false
                this.rpc("/jupiter_dashboard_tres/sales_inventory", {'region_wise': false, 'project_wise': true, 'project_region': region, 'configuration_ids': configuration_ids, 'cluster_ids': cluster_ids}).then((result) => {
                    self.projectOrRegionFlatStatus(result, true, false)
                })
            },

            onChangeRegion: function(ev){
                var self = this;
                var region = $(ev.target).attr('value') || false
                $('#region_selection button').empty().append($(ev.target).text())
                $('#region_selection button').attr('region_id', region)
                var configuration_ids = []
                for(var option of document.getElementById('configuration_select').options){
                    if (option.selected){
                        configuration_ids.push(parseInt(option.getAttribute('configuration_id')))
                    }
                }
                var cluster_ids = []
                for(var option of document.getElementById('cluster_select').options){
                    if (option.selected){
                        cluster_ids.push(parseInt(option.getAttribute('cluster_id')))
                    }
                }
                this.rpc("/jupiter_dashboard_tres/sales_inventory", {'region_wise': false, 'project_wise': true, 'project_region': region, 'configuration_ids': configuration_ids, 'cluster_ids': cluster_ids}).then((result) => {
                    self.projectOrRegionFlatStatus(result, true, false)
                })
                this.rpc("/jupiter_dashboard_tres/get_cluster", {region: region}).then((result) => {
                    $('#cluster_select_div').empty().append(result)
                    $('#cluster_select').select2()
                })
            },

            projectOrRegionFlatStatus: function (result){
                var options = {
                    series: [
                        {
                            name: 'Available',
                            data: result['project_available']
                        },
                    ],
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
                    colors: ['#00CCFF'],
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
                if ($("#project_wise_flat_status").length > 0){
                    $("#project_wise_flat_status").empty()
                    var chart2 = new ApexCharts(document.querySelector("#project_wise_flat_status"), options);
                    chart2.render();
                }
            },

            changeCpActiveDormantRadio: function(ev){
                if($('[name="cp-active-dormant"]:checked').val() == 'active'){
                    $('#month_cps_active').removeClass('d-none')
                    $('#quarter_cps_active').removeClass('d-none')
                    $('#half_cps_active').removeClass('d-none')
                    $('#year_cps_active').removeClass('d-none')

                    $('#month_cps_dormant').addClass('d-none')
                    $('#quarter_cps_dormant').addClass('d-none')
                    $('#half_cps_dormant').addClass('d-none')
                    $('#year_cps_dormant').addClass('d-none')
                }else{
                    $('#month_cps_active').addClass('d-none')
                    $('#quarter_cps_active').addClass('d-none')
                    $('#half_cps_active').addClass('d-none')
                    $('#year_cps_active').addClass('d-none')

                    $('#month_cps_dormant').removeClass('d-none')
                    $('#quarter_cps_dormant').removeClass('d-none')
                    $('#half_cps_dormant').removeClass('d-none')
                    $('#year_cps_dormant').removeClass('d-none')
                }
            },

            changeProjectWiseRadio: function(ev){
                if($('[name="project-wise-radio"]:checked').val() == 'booking'){
                    $('.project_wise_booking_div').removeClass('d-none')
                    $('.project_wise_registration_div').addClass('d-none')
                    $('#project_wise_booking_registration_select').appendTo($('#project_wise_booking_select_div'))
                }else{
                    $('.project_wise_booking_div').addClass('d-none')
                    $('.project_wise_registration_div').removeClass('d-none')
                    $('#project_wise_booking_registration_select').appendTo($('#project_wise_registration_select_div'))
                }
            },

            changeClusterWiseRadio: function(ev){
                if($('[name="cluster-wise-radio"]:checked').val() == 'booking'){
                    $('.cluster_wise_booking_div').removeClass('d-none')
                    $('.cluster_wise_registration_div').addClass('d-none')
                    $('#cluster_wise_booking_registration_select').appendTo($('#cluster_wise_booking_select_div'))
                }else{
                    $('.cluster_wise_booking_div').addClass('d-none')
                    $('.cluster_wise_registration_div').removeClass('d-none')
                    $('#cluster_wise_booking_registration_select').appendTo($('#cluster_wise_registration_select_div'))
                }
            },

            changeRegionWiseRadio: function(ev){
                if($('[name="region-wise-radio"]:checked').val() == 'booking'){
                    $('.region_wise_booking_div').removeClass('d-none')
                    $('.region_wise_registration_div').addClass('d-none')
                    $('#region_wise_booking_registration_select').appendTo($('#region_wise_booking_select_div'))
                }else{
                    $('.region_wise_booking_div').addClass('d-none')
                    $('.region_wise_registration_div').removeClass('d-none')
                    $('#region_wise_booking_registration_select').appendTo($('#region_wise_registration_select_div'))
                }
            },

            changeClusterCheckbox: function(ev){
                var self = this;
                var cluster_ids = []
                for(var cluster of $('.cluster_checkbox:checked')){
                    cluster_ids.push(parseInt($(cluster).attr('cluster_id')))
                }
                this.rpc("/jupiter_dashboard_tres/get_last_6_month_cp_booking", {cluster_ids: cluster_ids}).then((result) => {
                    self.applyCpBookingChart(result)
                })
            },

            changeRegionSelect: function(ev){
                var self = this;
                var region_ids = []
                for(var option of document.getElementById('region_select').options){
                    if (option.selected){
                        region_ids.push(parseInt(option.getAttribute('region_id')))
                    }
                }
                this.rpc("/jupiter_dashboard_tres/get_cluster_select_data", {region_ids: region_ids}).then((result) => {
                    $('.cluster-select-div').empty().append(result)
                })
                this.rpc("/jupiter_dashboard_tres/get_last_6_month_cp_booking", {region_ids: region_ids}).then((result) => {
                    self.applyCpBookingChart(result)
                })
            },

            changeRadioActualBudget: function(ev){
                var self = this;
                if($('[name="comparison-value-radio"]:checked').val() == 'booking'){
                    var booking_type = 'number'
                    var registration_type = false
                    var type = 'booking'
                }else{
                    var booking_type = false
                    var registration_type = 'number'
                    var type = 'registration'
                }
                this.rpc("/jupiter_dashboard_tres/budget_actual_comparison", {'booking_type': booking_type, 'registration_type': registration_type}).then((result) => {
                    self.ActualBudgetComparison(result, type)
                })
            },

            changeProjectWiseSelect: function(ev){
                var self = this;
                var type = $('#project_wise_booking_select').val()
                var frequency = $('.project_wise_radio:checked').val()
                var project_ids = []
                $('.project-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        project_ids.push(parseInt($(obj).attr('project_id')))
                    }
                })
                var region_ids = []
                $('.cluster-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        region_ids.push(parseInt($(obj).attr('cluster_id')))
                    }
                })
                var parent_region = []
                $('.region-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        parent_region.push(parseInt($(obj).attr('region_id')))
                    }
                })
                var custom_range = $('#custom_date_range_project_booking_registration').prop('checked')
                var custom_start = false
                var custom_end = false
                if(custom_range){
                    custom_start = $('#project_booking_registrations_date_from').val()
                    custom_end = $('#project_booking_registrations_date_to').val()
                }
                var count_or_value = $('.project-radio-input:checked').val()
    //          'region_or_cluster': 'project'
                this.rpc("/jupiter_dashboard_tres/bookings_registrations_region_wise", {'frequency': frequency, 'region_ids': region_ids, 'count_or_value': count_or_value, 'region_or_cluster': 'project', 'parent_region': parent_region, 'project_ids': project_ids, 'custom_start': custom_start, 'custom_end': custom_end}).then((result) => {
                    if (type == 'gross'){
                        var data =  result[0][0]['data']
                    }else if (type == 'cancelled'){
                        var data =  result[0][1]['data']
                    }else {
                        var data =  result[0][2]['data']
                    }
                    self.applyProjectWiseBookingChart(result[2][type]['values'], result[2][type]['categories'])
                })
            },

            changeClusterWiseSelect: function(ev){
                var self = this;
                var type = $('#cluster_wise_booking_select').val()
                var frequency = $('.cluster_wise_radio:checked').val()
                var region_ids = []
                $('.cluster-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        region_ids.push(parseInt($(obj).attr('cluster_id')))
                    }
                })
                var parent_region = []
                $('.region-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        parent_region.push(parseInt($(obj).attr('region_id')))
                    }
                })
                var custom_range = $('#custom_date_range_cluster_booking_registration').prop('checked')
                var custom_start = false
                var custom_end = false
                if(custom_range){
                    custom_start = $('#cluster_booking_registrations_date_from').val()
                    custom_end = $('#cluster_booking_registrations_date_to').val()
                }
                var count_or_value = $('.cluster-radio-input:checked').val()
    //            'region_or_cluster': 'cluster'
                this.rpc("/jupiter_dashboard_tres/bookings_registrations_region_wise", {'frequency': frequency, 'region_ids': region_ids, 'count_or_value': count_or_value, 'region_or_cluster': 'cluster', 'parent_region': parent_region, 'custom_start': custom_start, 'custom_end': custom_end}).then((result) => {
                    if (type == 'gross'){
                        var data =  result[0][0]['data']
                    }else if (type == 'cancelled'){
                        var data =  result[0][1]['data']
                    }else {
                        var data =  result[0][2]['data']
                    }
                    self.applyClusterWiseBookingChart(data, result[1])
                })
            },

            changeRegionWiseSelect: function(ev){
                var self = this;
                var type = $('#region_wise_booking_select').val()
                var frequency = $('.region_wise_radio:checked').val()
                var region_ids = []
                $('.region-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        region_ids.push(parseInt($(obj).attr('region_id')))
                    }
                })
                var custom_range = $('#custom_date_range_booking_registration').prop('checked')
                var count_or_value = $('.region-radio-input:checked').val()
                var custom_from = false
                var custom_to = false
                if(custom_range){
                    custom_from = $('#booking_registrations_date_from').val()
                    custom_to = $('#booking_registrations_date_to').val()
                }
                this.rpc("/jupiter_dashboard_tres/bookings_registrations_region_wise", {'frequency': frequency, 'region_ids': region_ids, 'count_or_value': count_or_value, 'custom_from': custom_from, 'custom_to': custom_to}).then((result) => {
                    if (type == 'gross'){
                        var data =  result[0][0]['data']
                    }else if (type == 'cancelled'){
                        var data =  result[0][1]['data']
                    }else {
                        var data =  result[0][2]['data']
                    }
                    self.applyRegionWiseBookingChart(data, result[1])
                })
            },

            changeRadioProjectWise: function(ev){
                var self = this;
                var frequency = $('.project_wise_radio:checked').val()
                var type = $('#project_wise_booking_select').val()
                var count_or_value = $('.project-radio-input:checked').val()
                var project_ids = [.01]
                $('.project-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        project_ids.push(parseInt($(obj).attr('project_id')))
                    }
                })
                var region_ids = [.01]
                $('.cluster-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        region_ids.push(parseInt($(obj).attr('cluster_id')))
                    }
                })
                var parent_region = [.01]
                $('.region-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        parent_region.push(parseInt($(obj).attr('region_id')))
                    }
                })
                var custom_range = $('#custom_date_range_project_booking_registration').prop('checked')
                var custom_start = false
                var custom_end = false
                if(custom_range){
                    custom_start = $('#project_booking_registrations_date_from').val()
                    custom_end = $('#project_booking_registrations_date_to').val()
                }
    //          4. region_or_cluster = project
                this.rpc("/jupiter_dashboard_tres/bookings_registrations_region_wise", {'frequency': frequency, 'region_ids': region_ids, 'count_or_value': count_or_value, 'region_or_cluster': 'project', 'parent_region': parent_region, 'project_ids': project_ids, 'custom_start': custom_start, 'custom_end': custom_end}).then((result) => {
                    self.applyProjectWiseChart(result)
                    if (type == 'gross'){
                        var data =  result[0][0]['data']
                    }else if (type == 'cancelled'){
                        var data =  result[0][1]['data']
                    }else {
                        var data =  result[0][2]['data']
                    }
                    self.applyProjectWiseBookingChart(result[2][type]['values'], result[2][type]['categories'])
                    self.applyProjectWiseRegistrationChart(result[2]['registration']['values'], result[2]['registration']['categories'])
                })
            },

            changeRadioClusterWise: function(ev){
                var self = this;
                var frequency = $('.cluster_wise_radio:checked').val()
                var type = $('#cluster_wise_booking_select').val()
                var count_or_value = $('.cluster-radio-input:checked').val()
                var region_ids = [.01]
                $('.cluster-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        region_ids.push(parseInt($(obj).attr('cluster_id')))
                    }
                })
                var parent_region = [.01]
                $('.region-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        parent_region.push(parseInt($(obj).attr('region_id')))
                    }
                })
                var custom_range = $('#custom_date_range_cluster_booking_registration').prop('checked')
                var custom_start = false
                var custom_end = false
                if(custom_range){
                    custom_start = $('#cluster_booking_registrations_date_from').val()
                    custom_end = $('#cluster_booking_registrations_date_to').val()
                }
    //            'region_or_cluster': 'cluster'
                this.rpc("/jupiter_dashboard_tres/bookings_registrations_region_wise", {'frequency': frequency, 'region_ids': region_ids, 'count_or_value': count_or_value, 'region_or_cluster': 'cluster', 'parent_region': parent_region, 'custom_start': custom_start, 'custom_end': custom_end}).then((result) => {
                    self.applyClusterWiseChart(result)
                    if (type == 'gross'){
                        var data =  result[0][0]['data']
                    }else if (type == 'cancelled'){
                        var data =  result[0][1]['data']
                    }else {
                        var data =  result[0][2]['data']
                    }
                    self.applyClusterWiseBookingChart(data, result[1])
                    self.applyClusterWiseRegistrationChart(result[0][3]['data'], result[1])
                })
            },

            changeRadioRegionWise: function(ev){
                var self = this;
                var frequency = $('.region_wise_radio:checked').val()
                var type = $('#region_wise_booking_select').val()
                var count_or_value = $('.region-radio-input:checked').val()
                var region_ids = [.01]
                $('.region-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        region_ids.push(parseInt($(obj).attr('region_id')))
                    }
                })
                var custom_range = $('#custom_date_range_booking_registration').prop('checked')
                var custom_start = false
                var custom_end = false
                if(custom_range){
                    custom_start = $('#booking_registrations_date_from').val()
                    custom_end = $('#booking_registrations_date_to').val()
                }
                this.rpc("/jupiter_dashboard_tres/bookings_registrations_region_wise", {'frequency': frequency, 'region_ids': region_ids, 'count_or_value': count_or_value, 'custom_start': custom_start, 'custom_end': custom_end}).then((result) => {
                    self.applyRegionWiseChart(result)
                    if (type == 'gross'){
                        var data =  result[0][0]['data']
                    }else if (type == 'cancelled'){
                        var data =  result[0][1]['data']
                    }else {
                        var data =  result[0][2]['data']
                    }
                    self.applyRegionWiseBookingChart(data, result[1])
                    self.applyRegionWiseRegistrationChart(result[0][3]['data'], result[1])
                })
            },

    //        Graph 2 - AJAX request to the server to fetch data  processes chart
            changeRadioRegionWise2: function(ev){
                var self = this;
                var frequency = $('.region_wise_radio2:checked').val()
                var type = '';
                var count_or_value = $('.region-radio-input2:checked').val()
                var region_ids = [.01]
                $('.region-blocks2').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        region_ids.push(parseInt($(obj).attr('region_id')))
                    }
                })
                var custom_range = false
                var custom_start = false
                var custom_end = false

                this.rpc("/jupiter_dashboard_tres/bookings_registrations_region_wise2", {'frequency': frequency, 'region_ids': region_ids, 'count_or_value': count_or_value, 'custom_start': custom_start, 'custom_end': custom_end}).then((result) => {
                    self.applyRegionWiseChart2(result)
                    if (type == 'gross'){
                        var data =  result[0][0]['data']
                    }else if (type == 'cancelled'){
                        var data =  result[0][1]['data']
                    }else {
                        var data =  result[0][2]['data']
                    }
                })
            },

            applyProjectWiseBookingChart: function(data, labels){
                var options = {
                    series: data,
                    chart: {
                        type: 'pie',
                        height: '200'
                    },
                    labels: labels,
                    legend: {
                        position: 'left',
                        width: 150,
                        fontSize: '12px',
                    },
                    responsive: [{
                        breakpoint: 480,
                        options: {
                        }
                    }]
                };
                if ($("#project_wise_booking_chart").length > 0){
                    $("#project_wise_booking_chart").empty()
                    var chart = new ApexCharts(document.querySelector("#project_wise_booking_chart"), options);
                    chart.render();
                }
            },

            applyClusterWiseBookingChart: function(data, labels){
                var options = {
                    series: data,
                    chart: {
                        type: 'pie',
                        height: '200'
                    },
                    labels: labels,
                    legend: {
                        position: 'left',
                        width: 150,
                        fontSize: '12px',
                    },
                    responsive: [{
                        breakpoint: 480,
                        options: {
                        }
                    }]
                };
                if ($("#cluster_wise_booking_chart").length > 0){
                    $("#cluster_wise_booking_chart").empty()
                    var chart = new ApexCharts(document.querySelector("#cluster_wise_booking_chart"), options);
                    chart.render();
                }
            },

            applyRegionWiseBookingChart: function(data, labels){
                var options = {
                    series: data,
                    chart: {
                        type: 'pie',
                        height: '200'
                    },
                    labels: labels,
                    legend: {
                        position: 'left',
                        width: 150,
                        fontSize: '12px',
                    },
                    responsive: [{
                        breakpoint: 480,
                        options: {
                        }
                    }]
                };
                if ($("#region_wise_booking_chart").length > 0){
                    $("#region_wise_booking_chart").empty()
                    var chart = new ApexCharts(document.querySelector("#region_wise_booking_chart"), options);
                    chart.render();
                }
            },

    //        Graph 2
            applyRegionWiseBookingChart2: function(data, labels){
                var options = {
                    series: data,
                    chart: {
                        type: 'pie',
                        height: '200'
                    },
                    labels: labels,
                    legend: {
                        position: 'left',
                        width: 150,
                        fontSize: '12px',
                    },
                    responsive: [{
                        breakpoint: 480,
                        options: {
                        }
                    }]
                };
                if ($("#region_wise_booking_chart2").length > 0){
                    $("#region_wise_booking_chart2").empty()
                    var chart = new ApexCharts(document.querySelector("#region_wise_booking_chart2"), options);
                    chart.render();
                }
            },

            applyProjectWiseRegistrationChart: function(data, labels){
                var options = {
                    series: data,
                    chart: {
                        type: 'pie',
                        height: '200'
                    },
                    labels: labels,
                    legend: {
                        position: 'left',
                        width: 150,
                        fontSize: '12px',
                    },
                    responsive: [{
                        breakpoint: 480,
                        options: {
                        }
                    }]
                };
                if($("#project_wise_registration_chart").length > 0){
                    $("#project_wise_registration_chart").empty()
                    var chart = new ApexCharts(document.querySelector("#project_wise_registration_chart"), options);
                    chart.render();
                }
            },

            applyClusterWiseRegistrationChart: function(data, labels){
                var options = {
                    series: data,
                    chart: {
                        type: 'pie',
                        height: '200'
                    },
                    labels: labels,
                    legend: {
                        position: 'left',
                        width: 150,
                        fontSize: '12px',
                    },
                    responsive: [{
                        breakpoint: 480,
                        options: {
                        }
                    }]
                };
                if ($("#cluster_wise_registration_chart").length > 0){
                    $("#cluster_wise_registration_chart").empty()
                    var chart = new ApexCharts(document.querySelector("#cluster_wise_registration_chart"), options);
                    chart.render();
                }
            },

            applyRegionWiseRegistrationChart: function(data, labels){
                var options = {
                    series: data,
                    chart: {
                        type: 'pie',
                        height: '200'
                    },
                    labels: labels,
                    legend: {
                        position: 'left',
                        width: 150,
                        fontSize: '12px',
                    },
                    responsive: [{
                        breakpoint: 480,
                        options: {
                        }
                    }]
                };
                if ($("#region_wise_registration_chart").length > 0){
                    $("#region_wise_registration_chart").empty()
                    var chart = new ApexCharts(document.querySelector("#region_wise_registration_chart"), options);
                    chart.render();
                }
            },
            applyRegionWiseRegistrationChart2: function(data, labels){
                var options = {
                    series: data,
                    chart: {
                        type: 'pie',
                        height: '200'
                    },
                    labels: labels,
                    legend: {
                        position: 'left',
                        width: 150,
                        fontSize: '12px',
                    },
                    responsive: [{
                        breakpoint: 480,
                        options: {
                        }
                    }]
                };
                if ($("#region_wise_registration_chart2").length > 0){
                    $("#region_wise_registration_chart2").empty()
                    var chart = new ApexCharts(document.querySelector("#region_wise_registration_chart2"), options);
                    chart.render();
                }
            },

            applyProjectWiseChart: function(result){
                var table = `
                    <table class="table table-sm cp_booking_unit_table">
                        <thead>
                            <tr>
                                <th>Project</th>
                                <th class="text-right">Gross</th>
                                <th class="text-right">Cancelled</th>
                                <th class="text-right">Net</th>
                                <th class="text-right">Registration</th>
                            </tr>
                        </thead>
                        <tbody>
                `
                var categories = result[1]
                var index = 0
                for (var item of categories){
                    table += `<tr>
                       <td>${item}</td>
                       <td class="text-right">${result[0][0]['data'][index]}</td>
                       <td class="text-right">${result[0][1]['data'][index]}</td>
                       <td class="text-right">${result[0][2]['data'][index]}</td>
                       <td class="text-right">${result[0][3]['data'][index]}</td>
                       </tr>
                    `
                    index += 1;
                }
                table += `</tbody></table>`
                $("#project_wise_booking_registration").empty().append(table)
            },

            applyClusterWiseChart: function(result){
                var series = [
                {
                    'name': 'Gross',
                    'type': 'bar',
                    'data': result[0][0]['data']
                },
                {
                    'name': 'Cancelled',
                    'type': 'bar',
                    'data': result[0][1]['data']
                },
                {
                    'name': 'Net',
                    'type': 'bar',
                    'data': result[0][2]['data']
                },
                {
                    'name': 'Registration',
                    'type': 'bubble',
                    'data': result[0][3]['data']
                },
                ]
                var categories = result[1]
                var chart_height = 65 * result[0][0]['data'].length
                if (chart_height < 230){
                    chart_height = 230
                }
                var options = {
                    series: series,
                    chart: {
                        fontFamily: 'Poppins, sans-serif',
                        height: chart_height,
                        type: 'bar',
                        stacked: false,
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
                colors: ['#00a6fb', '#2e294e','#06d6a0',  '#ffffff00'],
                plotOptions: {
                    bar: {
                        horizontal: true,
                        columnWidth: '25%',
                        endingShape: 'rounded',
                    },
                },
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    width: [1, 1, 1, 2]
                },
                title: {
                    text: ' ',
                    align: 'left',
                    offsetX: 110
                },
                xaxis: {
                    categories: categories,
                    position: 'top',
                },
                yaxis: {
                    title: {
                        text: 'Count'
                    },
                    axisBorder: {
                        show: true,
                        color: '#008FFB'
                    },
                },
                tooltip: {
                    shared: true,
                    intersect: false,
                    custom: function({ series, seriesIndex, dataPointIndex, w }) {
                        const category = w.config.xaxis.categories[dataPointIndex];
                        let tooltipHtml = `<div class="custom-tooltip">
                            <div class="category">${category}</div>`;
                        w.config.series.forEach((s, index) => {
                            const markerClass = s.name.replace(/\s+/g, ''); // Remove spaces from series name for CSS class
                            tooltipHtml += `<div class="series-data">
                                <div class="marker ${markerClass}"></div>
                                <div>${s.name}: ${s.data[dataPointIndex]}</div>
                            </div>`;
                        });
                        tooltipHtml += `</div>`;
                        return tooltipHtml;
                    }
                },
                annotations: {
                    points: series[3].data.map((value, index) => {
                        return {
                            x: value,
                            y: categories[index],
                            seriesIndex: 3, // Index of the 'Registration' series
                            marker: {
                                size: 5, // Increased size for better visibility
                                fillColor: '#ea526f',
                                strokeColor: '#ea526f',
                                strokeWidth: 0,
                                shape: 'circle',
                                offsetY: 5,
                            },
                        };
                    }).filter(point => point.x > 0) // Ensure dots are added only where y > 0
                },
                legend: {
                    position: 'top',
                        floating: true,
                        horizontalAlign: 'center',
                        offsetX: 10,
                        offsetY: 0,
                    }
                };
                if ($("#cluster_wise_booking_registration").length > 0){
                    $("#cluster_wise_booking_registration").empty()
                    var chart = new ApexCharts(document.querySelector("#cluster_wise_booking_registration"), options);
                    chart.render();
                    $('#cluster_wise_booking_registration_legend').empty()
                    $('#cluster_wise_booking_registration .apexcharts-legend').appendTo($('#cluster_wise_booking_registration_legend'))
                    $('[seriesname="Registration"] .apexcharts-legend-marker').last().css('background', 'rgb(234 82 111)')
                }
            },

            applyRegionWiseChart: function(result){
                var options = {
                    series: result[0],
                    chart: {
                        fontFamily: 'Poppins, sans-serif',
                        height: 250,
                        type: 'line',
                        stacked: false,
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
                    colors: ['#00a6fb', '#2e294e','#06d6a0',  '#ea526f'],
                    plotOptions: {
                        bar: {
                            horizontal: false,
                            columnWidth: '25%',
                            endingShape: 'rounded'
                        },
                    },
                    dataLabels: {
                        enabled: false
                    },
                    stroke: {
                        width: [1, 1, 1, 2]
                    },
                    title: {
                        text: ' ',
                        align: 'left',
                        offsetX: 110
                    },
                    xaxis: {
                        categories: result[1],
                    },
                    yaxis: {
                        title: {
                            text: 'Count'
                        },axisBorder: {
                            show: true,
                            color: '#008FFB'
                        },
                    },
                    tooltip: {
                        fixed: {
                            enabled: true,
                            position: 'topLeft', // topRight, topLeft, bottomRight, bottomLeft
                            offsetY: 30,
                            offsetX: 60
                        },
                    },
                    legend: {
                        position: 'top',
                        floating: true,
                    }
                };
                if ($("#region_wise_booking_registration").length > 0){
                    $("#region_wise_booking_registration").empty()
                    var chart = new ApexCharts(document.querySelector("#region_wise_booking_registration"), options);
                    chart.render();
                }

            },

    //        Graph 2 chart configuration (Booking, Cancelled, and Registration) - ApexCharts
            applyRegionWiseChart2: function(result){
                var options = {
                    series: result[0],
                    chart: {
                        fontFamily: 'Poppins, sans-serif',
                        height: 250,
                        type: 'bar',
                        stacked: false,
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
                    colors: ['#00a6fb', '#2e294e','#06d6a0',  '#ea526f'],
                    plotOptions: {
                        bar: {
                            horizontal: false,
                            columnWidth: '25%',
                            endingShape: 'rounded'
                        },
                    },
                    dataLabels: {
                        enabled: false
                    },
                    stroke: {
                        width: [1, 1, 1, 2]
                    },
                    title: {
                        text: ' ',
                        align: 'left',
                        offsetX: 110
                    },
                    xaxis: {
                        categories: result[1],
                    },
                    yaxis: {
                        title: {
                            text: 'Count'
                        },axisBorder: {
                            show: true,
                            color: '#008FFB'
                        },
                    },
                    tooltip: {
                        enabled: true,
                        shared: false, // Individual tooltips for each bar
                        intersect: true, // Only show tooltip when hovering over a bar
                        custom: function({ series, seriesIndex, dataPointIndex, w }) {
                            const value = series[seriesIndex][dataPointIndex];
                            const category = w.globals.labels[dataPointIndex];
                            const seriesName = w.globals.seriesNames[seriesIndex];
                            const barColor = w.config.colors[seriesIndex];
                            return (
                                `<div class="tooltip-box" style="padding: 10px; background: #fff; color: #333; border: 1px solid ${barColor}; border-radius: 8px; width: auto; min-width: 80px; max-width: 250px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);">` +
                                // First Section: Date (category)
                                `<div style="font-weight: bold; color: ${barColor}; font-size: 13px; margin-bottom: 4px;">` +
                                `<span style="color: #888;">${category}</span>` +
                                `</div>` +
                                // Divider for aesthetics
                                `<div style="border-top: 1px solid #eee; margin-top: 2px; padding-top: 5px;">` +
                                `</div>` +
                                // Second Section: Series Name and Value in the same line
                                `<div style="display: flex; justify-content: flex-start; align-items: center; margin-bottom: 1px;">` +
                                `<span style="font-weight: bold; color: ${barColor}; margin-right: 5px;">${seriesName}:</span>` +
                                `<span style="font-size: 14px; color: #000;">${value}</span>` +
                                `</div>` +
                                '</div>'
                            );
                        }
                    },
                    legend: {
                        position: 'top',
                        floating: true,
                    }
                };
                if ($("#region_wise_booking_registration2").length > 0){
                    $("#region_wise_booking_registration2").empty()
                    var chart = new ApexCharts(document.querySelector("#region_wise_booking_registration2"), options);
                    chart.render();
                }
            },

            changeProject: function(ev){
                var self = this;
                if(ev){
                    if ($(ev.target).hasClass('active')){
                        $(ev.target).removeClass('active')
                    }else{
                        $(ev.target).addClass('active')
                    }
                }
                var project_ids = [.01]
                $('.project-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        project_ids.push(parseInt($(obj).attr('project_id')))
                    }
                })
                this.rpc("/jupiter_dashboard_tres/bookings_registrations", {'project': project_ids}).then((result) => {
                    self.applyProjectBookingRegistration(result)
                })
                self.changeRadioProjectWise()
            },

            changeCluster: function(ev){
                var self = this;
                if(ev){
                    if ($(ev.target).hasClass('active')){
                        $(ev.target).removeClass('active')
                    }else{
                        $(ev.target).addClass('active')
                    }
                }
                var cluster_ids = [.01]
                $('.cluster-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        cluster_ids.push(parseInt($(obj).attr('cluster_id')))
                    }
                })
                var region_ids = [.01]
                $('.region-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        region_ids.push(parseInt($(obj).attr('region_id')))
                    }
                })
                this.rpc("/jupiter_dashboard_tres/bookings_registrations", {'cluster': cluster_ids, 'region': region_ids}).then((result) => {
                    self.applyClusterBookingRegistration(result)
                    this.rpc("/jupiter_dashboard_tres/get_project_data", {'cluster': cluster_ids, 'region': region_ids}).then((result1) => {
                        $('#project-container').empty().append(result1)
                        self.applyProjectBookingRegistration(result)
                        self.changeRadioProjectWise()
                    })
                })
                self.changeRadioClusterWise()
            },

            changeRegion: function(ev){
                var self = this;
                if(ev){
                    if ($(ev.target).hasClass('active')){
                        $(ev.target).removeClass('active')
                    }else{
                        $(ev.target).addClass('active')
                    }
                }
                var region_ids = [.01]
                $('.region-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        region_ids.push(parseInt($(obj).attr('region_id')))
                    }
                })
                this.rpc("/jupiter_dashboard_tres/bookings_registrations", {'region': region_ids}).then((result) => {
                    self.applyRegionBookingRegistration(result)
                    self.changeRadioRegionWise()
                    this.rpc("/jupiter_dashboard_tres/get_cluster_data", {'region': region_ids}).then((result1) => {
                        $('#cluster-container').empty().append(result1)
                        self.applyClusterBookingRegistration(result)
                        self.changeRadioClusterWise()
                    })
                    this.rpc("/jupiter_dashboard_tres/get_project_data", {'region': region_ids}).then((result2) => {
                        $('#project-container').empty().append(result2)
                        self.applyProjectBookingRegistration(result)
                        self.changeRadioProjectWise()
                    })
                })
            },


    //        Graph 2 dashboard iii Process of selecting one or more Regions from the UI
            changeRegion2: function(ev){
                var self = this;
                if(ev){
                    if ($(ev.target).hasClass('active')){
                        $(ev.target).removeClass('active')
                    }else{
                        $(ev.target).addClass('active')
                    }
                }
                var region_ids2 = [.01]
                $('.region-blocks2').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        region_ids2.push(parseInt($(obj).attr('region_id')))
                    }
                })

               var frequency2 = $('.region_wise_radio2:checked').val();
                var type2 = '';
                var count_or_value2 = $('.region-radio-input2:checked').val();

                 var custom_range2 = false
                 var custom_start2 = false
                 var custom_end2 = false

                this.rpc("/jupiter_dashboard_tres/bookings_registrations_region_wise2", {'frequency': frequency2, 'region_ids': region_ids2, 'count_or_value': count_or_value2, 'custom_start': custom_start2, 'custom_end': custom_end2}).then((result) => {
                        self.applyRegionWiseChart2(result)
                        self.applyRegionWiseBookingChart2(result[0][0]['data'], result[1])
                        self.applyRegionWiseRegistrationChart2(result[0][1]['data'], result[1])
                    })
            },

            applyRegionBookingRegistration: function(result){
                $('#today_booking_gross_count').empty().append(result['today_booking_gross_count'])
                $('#week_booking_gross_count').empty().append(result['week_booking_gross_count'])
                $('#month_booking_gross_count').empty().append(result['month_booking_gross_count'])
                $('#year_booking_gross_count').empty().append(result['year_booking_gross_count'])
                $('#quarter_booking_gross_count').empty().append(result['quarter_booking_gross_count'])
                $('#half_booking_gross_count').empty().append(result['half_booking_gross_count'])

                $('#today_booking_gross_value').empty().append(result['today_booking_gross_value'])
                $('#week_booking_gross_value').empty().append(result['week_booking_gross_value'])
                $('#month_booking_gross_value').empty().append(result['month_booking_gross_value'])
                $('#year_booking_gross_value').empty().append(result['year_booking_gross_value'])
                $('#quarter_booking_gross_value').empty().append(result['quarter_booking_gross_value'])
                $('#half_booking_gross_value').empty().append(result['half_booking_gross_value'])

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

                $('#today_average_av').empty().append(result['today_average_av'])
                $('#week_average_av').empty().append(result['week_average_av'])
                $('#month_average_av').empty().append(result['month_average_av'])
                $('#quarter_average_av').empty().append(result['quarter_average_av'])
                $('#half_average_av').empty().append(result['half_average_av'])
                $('#year_average_av').empty().append(result['year_average_av'])
            },

            applyClusterBookingRegistration: function(result){
                $('#cluster_today_booking_gross_count').empty().append(result['today_booking_gross_count'])
                $('#cluster_week_booking_gross_count').empty().append(result['week_booking_gross_count'])
                $('#cluster_month_booking_gross_count').empty().append(result['month_booking_gross_count'])
                $('#cluster_year_booking_gross_count').empty().append(result['year_booking_gross_count'])
                $('#cluster_quarter_booking_gross_count').empty().append(result['quarter_booking_gross_count'])
                $('#cluster_half_booking_gross_count').empty().append(result['half_booking_gross_count'])

                $('#cluster_today_booking_gross_value').empty().append(result['today_booking_gross_value'])
                $('#cluster_week_booking_gross_value').empty().append(result['week_booking_gross_value'])
                $('#cluster_month_booking_gross_value').empty().append(result['month_booking_gross_value'])
                $('#cluster_year_booking_gross_value').empty().append(result['year_booking_gross_value'])
                $('#cluster_quarter_booking_gross_value').empty().append(result['quarter_booking_gross_value'])
                $('#cluster_half_booking_gross_value').empty().append(result['half_booking_gross_value'])

                $('#cluster_today_booking_count').empty().append(result['today_booking_count'])
                $('#cluster_week_booking_count').empty().append(result['week_booking_count'])
                $('#cluster_month_booking_count').empty().append(result['month_booking_count'])
                $('#cluster_year_booking_count').empty().append(result['year_booking_count'])
                $('#cluster_quarter_booking_count').empty().append(result['quarter_booking_count'])
                $('#cluster_half_booking_count').empty().append(result['half_booking_count'])

                $('#cluster_today_booking_value').empty().append(result['today_booking_value'])
                $('#cluster_week_booking_value').empty().append(result['week_booking_value'])
                $('#cluster_month_booking_value').empty().append(result['month_booking_value'])
                $('#cluster_year_booking_value').empty().append(result['year_booking_value'])
                $('#cluster_quarter_booking_value').empty().append(result['quarter_booking_value'])
                $('#cluster_half_booking_value').empty().append(result['half_booking_value'])

                $('#cluster_today_registration_count').empty().append(result['today_registration_count'])
                $('#cluster_week_registration_count').empty().append(result['week_registration_count'])
                $('#cluster_month_registration_count').empty().append(result['month_registration_count'])
                $('#cluster_year_registration_count').empty().append(result['year_registration_count'])
                $('#cluster_quarter_registration_count').empty().append(result['quarter_registration_count'])
                $('#cluster_half_registration_count').empty().append(result['half_registration_count'])

                $('#cluster_today_registration_value').empty().append(result['today_registration_value'])
                $('#cluster_week_registration_value').empty().append(result['week_registration_value'])
                $('#cluster_month_registration_value').empty().append(result['month_registration_value'])
                $('#cluster_year_registration_value').empty().append(result['year_registration_value'])
                $('#cluster_quarter_registration_value').empty().append(result['quarter_registration_value'])
                $('#cluster_half_registration_value').empty().append(result['half_registration_value'])

                $('#cluster_today_booking_cancelled_count').empty().append(result['today_booking_cancelled_count'])
                $('#cluster_week_booking_cancelled_count').empty().append(result['week_booking_cancelled_count'])
                $('#cluster_month_booking_cancelled_count').empty().append(result['month_booking_cancelled_count'])
                $('#cluster_year_booking_cancelled_count').empty().append(result['year_booking_cancelled_count'])
                $('#cluster_quarter_booking_cancelled_count').empty().append(result['quarter_booking_cancelled_count'])
                $('#cluster_half_booking_cancelled_count').empty().append(result['half_booking_cancelled_count'])

                $('#cluster_today_booking_cancelled_value').empty().append(result['today_booking_cancelled_value'])
                $('#cluster_week_booking_cancelled_value').empty().append(result['week_booking_cancelled_value'])
                $('#cluster_month_booking_cancelled_value').empty().append(result['month_booking_cancelled_value'])
                $('#cluster_year_booking_cancelled_value').empty().append(result['year_booking_cancelled_value'])
                $('#cluster_quarter_booking_cancelled_value').empty().append(result['quarter_booking_cancelled_value'])
                $('#cluster_half_booking_cancelled_value').empty().append(result['half_booking_cancelled_value'])

                $('#cluster_today_average_av').empty().append(result['today_average_av'])
                $('#cluster_week_average_av').empty().append(result['week_average_av'])
                $('#cluster_month_average_av').empty().append(result['month_average_av'])
                $('#cluster_quarter_average_av').empty().append(result['quarter_average_av'])
                $('#cluster_half_average_av').empty().append(result['half_average_av'])
                $('#cluster_year_average_av').empty().append(result['year_average_av'])
            },

            applyProjectBookingRegistration: function(result){
                $('#project_today_booking_gross_count').empty().append(result['today_booking_gross_count'])
                $('#project_week_booking_gross_count').empty().append(result['week_booking_gross_count'])
                $('#project_month_booking_gross_count').empty().append(result['month_booking_gross_count'])
                $('#project_year_booking_gross_count').empty().append(result['year_booking_gross_count'])
                $('#project_quarter_booking_gross_count').empty().append(result['quarter_booking_gross_count'])
                $('#project_half_booking_gross_count').empty().append(result['half_booking_gross_count'])

                $('#project_today_booking_gross_value').empty().append(result['today_booking_gross_value'])
                $('#project_week_booking_gross_value').empty().append(result['week_booking_gross_value'])
                $('#project_month_booking_gross_value').empty().append(result['month_booking_gross_value'])
                $('#project_year_booking_gross_value').empty().append(result['year_booking_gross_value'])
                $('#project_quarter_booking_gross_value').empty().append(result['quarter_booking_gross_value'])
                $('#project_half_booking_gross_value').empty().append(result['half_booking_gross_value'])

                $('#project_today_booking_count').empty().append(result['today_booking_count'])
                $('#project_week_booking_count').empty().append(result['week_booking_count'])
                $('#project_month_booking_count').empty().append(result['month_booking_count'])
                $('#project_year_booking_count').empty().append(result['year_booking_count'])
                $('#project_quarter_booking_count').empty().append(result['quarter_booking_count'])
                $('#project_half_booking_count').empty().append(result['half_booking_count'])

                $('#project_today_booking_value').empty().append(result['today_booking_value'])
                $('#project_week_booking_value').empty().append(result['week_booking_value'])
                $('#project_month_booking_value').empty().append(result['month_booking_value'])
                $('#project_year_booking_value').empty().append(result['year_booking_value'])
                $('#project_quarter_booking_value').empty().append(result['quarter_booking_value'])
                $('#project_half_booking_value').empty().append(result['half_booking_value'])

                $('#project_today_registration_count').empty().append(result['today_registration_count'])
                $('#project_week_registration_count').empty().append(result['week_registration_count'])
                $('#project_month_registration_count').empty().append(result['month_registration_count'])
                $('#project_year_registration_count').empty().append(result['year_registration_count'])
                $('#project_quarter_registration_count').empty().append(result['quarter_registration_count'])
                $('#project_half_registration_count').empty().append(result['half_registration_count'])

                $('#project_today_registration_value').empty().append(result['today_registration_value'])
                $('#project_week_registration_value').empty().append(result['week_registration_value'])
                $('#project_month_registration_value').empty().append(result['month_registration_value'])
                $('#project_year_registration_value').empty().append(result['year_registration_value'])
                $('#project_quarter_registration_value').empty().append(result['quarter_registration_value'])
                $('#project_half_registration_value').empty().append(result['half_registration_value'])

                $('#project_today_booking_cancelled_count').empty().append(result['today_booking_cancelled_count'])
                $('#project_week_booking_cancelled_count').empty().append(result['week_booking_cancelled_count'])
                $('#project_month_booking_cancelled_count').empty().append(result['month_booking_cancelled_count'])
                $('#project_year_booking_cancelled_count').empty().append(result['year_booking_cancelled_count'])
                $('#project_quarter_booking_cancelled_count').empty().append(result['quarter_booking_cancelled_count'])
                $('#project_half_booking_cancelled_count').empty().append(result['half_booking_cancelled_count'])

                $('#project_today_booking_cancelled_value').empty().append(result['today_booking_cancelled_value'])
                $('#project_week_booking_cancelled_value').empty().append(result['week_booking_cancelled_value'])
                $('#project_month_booking_cancelled_value').empty().append(result['month_booking_cancelled_value'])
                $('#project_year_booking_cancelled_value').empty().append(result['year_booking_cancelled_value'])
                $('#project_quarter_booking_cancelled_value').empty().append(result['quarter_booking_cancelled_value'])
                $('#project_half_booking_cancelled_value').empty().append(result['half_booking_cancelled_value'])

                $('#project_today_average_av').empty().append(result['today_average_av'])
                $('#project_week_average_av').empty().append(result['week_average_av'])
                $('#project_month_average_av').empty().append(result['month_average_av'])
                $('#project_quarter_average_av').empty().append(result['quarter_average_av'])
                $('#project_half_average_av').empty().append(result['half_average_av'])
                $('#project_year_average_av').empty().append(result['year_average_av'])
            },

            ActualBudgetComparison: function(result, type){
                if (type == 'booking'){
                    var colors = ['#ff742e', '#2ec4b6']
                    var budget_data = result['booking_budgets']
                    var actual_data = result['bookings']
                }else{
                    var colors = ['#1e96fc', '#00af54']
                    var budget_data = result['registration_budgets']
                    var actual_data = result['registrations']
                }
                var options = {
                    series: [
                        {
                            name: "Budget",
                            data: budget_data
                        },
                        {
                            name: "Actual",
                            data: actual_data
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
                    colors: colors,
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
                        text: ' ',
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
                        horizontalAlign: 'center',
                        floating: true,
                        offsetY: 0,
                        offsetX: -5
                    }
                };
                if ($("#actual_vs_budget_chart").length > 0){
                    $("#actual_vs_budget_chart").empty()
                    var chart = new ApexCharts(document.querySelector("#actual_vs_budget_chart"), options);
                    chart.render();
                }
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
                if ($("#cp_count_chart").length > 0){
                    $("#cp_count_chart").empty()
                    var chart = new ApexCharts(document.querySelector("#cp_count_chart"), options);
                    chart.render();
                }
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
                    colors: ['#1e96fc'],
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
                        text: " ",
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
                if ($("#cp_chart").length > 0){
                    $("#cp_chart").empty()
                    var chart = new ApexCharts(document.querySelector("#cp_chart"), options);
                    chart.render();
                }
            },

            ManPowerProductivityRadialChart: function(result){
                var options = {
                    series: [result],
                    chart: {
                        height: 300,
                        type: 'radialBar',
                        offsetY: -20,
                        sparkline: {
                            enabled: true
                        }
                    },
                    plotOptions: {
                        radialBar: {
                            startAngle: -90,
                            endAngle: 90,
                            track: {
                                background: "#e7e7e7",
                                strokeWidth: '97%',
                                margin: 5, // margin is in pixels
                                dropShadow: {
                                    enabled: true,
                                    top: 2,
                                    left: 0,
                                    color: '#999',
                                    opacity: 1,
                                    blur: 2
                                }
                            },
                            dataLabels: {
                                name: {
                                    show: true
                                },
                                value: {
                                    offsetY: -40,
                                    fontSize: '20px',
                                    formatter: function(val){return val}
                                }
                            }
                        }
                    },
                    grid: {
                        padding: {
                            top: -10
                        }
                    },
                    fill: {
                        type: 'gradient',
                        gradient: {
                            shade: 'light',
                            shadeIntensity: 0.4,
                            inverseColors: false,
                            opacityFrom: 1,
                            opacityTo: 1,
                            stops: [0, 50, 53, 91]
                        },
                    },
                    labels: ['Productivity'],
                };
                if ($("#man_power_radial_chart").length > 0){
                    $("#man_power_radial_chart").empty()
                    var chart = new ApexCharts(document.querySelector("#man_power_radial_chart"), options);
                    chart.render();
                }
            },

            ManPowerProductivityRegionChart: function(result){
                var options = {
                    series: [
                        {
                            name: "Productivity",
                            data: result['data']
                        }
                    ],
                    chart: {
                        fontFamily: 'Poppins, sans-serif',
                        height: 400,
                        type: 'bar',
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
                    colors: ['#1e96fc'],
                    stroke: {
                      curve: 'smooth'
                    },
                    title: {
                        text: " ",
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
                        categories: result['categories'],
                        title: {
                            text: 'Region'
                        }
                    },
                    yaxis: {
                        title: {
                            text: 'Productivity'
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
                if($("#man_power_region_chart").length > 0){
                    $("#man_power_region_chart").empty()
                    var chart = new ApexCharts(document.querySelector("#man_power_region_chart"), options);
                    chart.render();
                }
            },

            ManPowerProductivityClusterChart: function(result){
                var options = {
                    series: [
                        {
                            name: "Productivity",
                            data: result['data']
                        }
                    ],
                    chart: {
                        fontFamily: 'Poppins, sans-serif',
                        height: 350,
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
                    colors: ['#138496'],
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
                        text: " ",
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
                        categories: result['categories'],
                        title: {
                            text: 'Cluster'
                        },
                        labels: {
                            formatter: function(value, index) {
                                if (typeof value === 'string') {
                                    return value.length > 6 ? value.substring(0, 6) + '...' : value;
                                }
                                return value;
                            }
                        }
                    },
                    tooltip: {
                        y: {
                            formatter: function(val, opts) {
                                return `${val}`;
                            }
                        },
                        x: {
                            formatter: function(value, opts) {
                                // Return the full category name for the tooltip
                                const categoryIndex = opts.dataPointIndex;
                                const categories = result['categories'];
                                return categories[categoryIndex] || value;
                            }
                        }
                    },
                    yaxis: {
                        title: {
                            text: 'Productivity'
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
                if($("#man_power_cluster_chart").length > 0){
                    $("#man_power_cluster_chart").empty()
                    var chart = new ApexCharts(document.querySelector("#man_power_cluster_chart"), options);
                    chart.render();
                }
            },

            WalkInRegionWise: function(result){
                if ($("#walk_in_region_wise").length > 0){
                    $("#walk_in_region_wise").empty()
                    Highcharts.chart('walk_in_region_wise', {
                        chart: {
                            type: 'column',
                            style: {
                                fontFamily: 'Poppins, sans-serif',
                              fontSize: '15px',
                              height: 320
                            }
                        },
                        title: {
                            text: ''
                        },
                        xAxis: {
                            categories: result['categories'],
                            labels: {
                                formatter: function () {
                                    // Truncate the label to 6 characters and append "..." if needed
                                    return this.value.length > 6 ? this.value.substring(0, 6) + '...' : this.value;
                                }
                            }
                        },
                        yAxis: [{
                            min: 0,
                            title: {
                                text: 'Count'
                            }
                        }],
                        legend: {
                            shadow: false,
                            floating: false,
                            align: 'center',
                            verticalAlign: 'bottom',
                            x: -2,
                            y: 10,
                        },
                        tooltip: {
                            shared: true,
                            formatter: function () {
                                var tooltip = '<b>' + this.x + '</b><br/>'; // Display the category

                                // Variables to hold the series values and conversion percentages
                                var walkInValue, bookingValue, conversionValue;

                                this.points.forEach(function (point) {
                                    if (point.series.name === 'Walk In') {
                                        walkInValue = point.y;
                                    } else if (point.series.name === 'Booking') {
                                        bookingValue = point.y;
                                    }

                                    // Fetch conversion percentage if both values are available
                                    if (walkInValue !== undefined && bookingValue !== undefined) {
                                        var index = point.point.index;
                                        conversionValue = result['conversion'][index];
                                    }
                                });

                                // Append Walk In, Booking, and Conversion to tooltip
                                if (walkInValue !== undefined) {
                                    tooltip += '<span style="color:#2ec4b6;">&#9679;</span> Walk In: ' + walkInValue + '<br/>';
                                }
                                if (bookingValue !== undefined) {
                                    tooltip += '<span style="color:#114b5f;">&#9679;</span> Booking: ' + bookingValue + '<br/>';
                                }
                                if (conversionValue !== undefined) {
                                    tooltip += '<span style="color:red;">&#9679;</span> Conversion: ' + conversionValue + '%<br/>';
                                }

                                return tooltip;
                            }
                        },
                        plotOptions: {
                            column: {
                                grouping: false,
                                shadow: false,
                                borderWidth: 0
                            }
                        },
                        series: [{
                            name: 'Walk In',
                            color: '#2ec4b6',
                            data: result['walk_in'],
                            pointPadding: result['width'][0],
                            pointPlacement: 0
                        }, {
                            name: 'Booking',
                            color: '#114b5f',
                            data: result['booking'],
                            pointPadding: result['width'][1],
                            pointPlacement: 0
                        }]
                    });
                }
            },

            CpBookingUnitsRegionWise: function(result, label){
                var options = {
                    series: [
                        {
                            name: "Count",
                            data: result['data']
                        }
                    ],
                    chart: {
                        fontFamily: 'Poppins, sans-serif',
                        height: 350,
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
                    colors: ['#156064'],
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
                        text: " ",
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
                        categories: result['categories'],
                        title: {
                            text: label
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
                if ($("#cp_booking_units_region_wise").length > 0){
                    $("#cp_booking_units_region_wise").empty()
                    var chart = new ApexCharts(document.querySelector("#cp_booking_units_region_wise"), options);
                    chart.render();
                }
            },

            async onMounted() {
                var self = this;
        this.setupEventListeners();

    //      user based dashboard project configuration
                    this.rpc('/jupiter_dashboard_tres/get_project_configuration_data', {}).then((result) => {
    //                    if (!result[0]){
    //                    $('#region_1_dashboard').remove()
    //                    $('#region_2_dashboard').remove()
    //                    $('#region_3_dashboard').remove()
    //                    }
    //                    if (!result[1]){
    //                    $('#cluster_1_dashboard').remove()
    //                    $('#cluster_2_dashboard').remove()
    //                    }
    //                    if (!result[2]){
    //                    $('#project_1_dashboard').remove()
    //                    $('#project_2_dashboard').remove()
    //                    }
    //                    $('#region_1_dashboard').removeClass('d-none')
    //                    $('#region_2_dashboard').removeClass('d-none')
    //                    $('#region_3_dashboard').removeClass('d-none')
    //                    $('#cluster_1_dashboard').removeClass('d-none')
    //                    $('#cluster_2_dashboard').removeClass('d-none')
    //                    $('#project_1_dashboard').removeClass('d-none')
    //                    $('#project_2_dashboard').removeClass('d-none')

                        if (result[0]){
                        $('#region_1_dashboard').removeClass('d-none')
                        $('#region_2_dashboard').removeClass('d-none')
                        $('#region_3_dashboard').removeClass('d-none')
                        }
                        if (result[1]){
                        $('#cluster_1_dashboard').removeClass('d-none')
                        $('#cluster_2_dashboard').removeClass('d-none')
                        }
                        if (result[2]){
                        $('#project_1_dashboard').removeClass('d-none')
                        $('#project_2_dashboard').removeClass('d-none')
                        }

                    })

                    this.rpc('/jupiter_dashboard_tres/get_region_data', {}).then((result) => {
                        $('#region-container').empty().append(result)

                        const today = new Date();
                        const firstDayPrevMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1);
                        const lastDayPrevMonth = new Date(today.getFullYear(), today.getMonth(), 0);
                        const formatDate = (date) => {
                            const year = date.getFullYear();
                            const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
                            const day = String(date.getDate()).padStart(2, '0');
                            return `${year}-${month}-${day}`;
                        };
                        $('#manpower_date_from').val(formatDate(firstDayPrevMonth));
                        $('#manpower_date_to').val(formatDate(lastDayPrevMonth));
                        $('#booking_registrations_date_from').val(formatDate(firstDayPrevMonth));
                        $('#booking_registrations_date_to').val(formatDate(lastDayPrevMonth));
                        $('#cluster_booking_registrations_date_from').val(formatDate(firstDayPrevMonth));
                        $('#cluster_booking_registrations_date_to').val(formatDate(lastDayPrevMonth));
                        $('#project_booking_registrations_date_from').val(formatDate(firstDayPrevMonth));
                        $('#project_booking_registrations_date_to').val(formatDate(lastDayPrevMonth));
                        $('#cp_booking_date_from').val(formatDate(firstDayPrevMonth));
                        $('#cp_booking_date_to').val(formatDate(lastDayPrevMonth));
                        $('#top_20_cp_date_from').val(formatDate(firstDayPrevMonth));
                        $('#top_20_cp_date_to').val(formatDate(lastDayPrevMonth));
                    })
                    this.rpc('/jupiter_dashboard_tres/get_region_data2', {}).then((result) => {
                        $('#region-container2').empty().append(result)

                        const today = new Date();
                        const firstDayPrevMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1);
                        const lastDayPrevMonth = new Date(today.getFullYear(), today.getMonth(), 0);
                        const formatDate = (date) => {
                            const year = date.getFullYear();
                            const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
                            const day = String(date.getDate()).padStart(2, '0');
                            return `${year}-${month}-${day}`;
                        };


                var frequency2 = $('.region_wise_radio2:checked').val();
                var type2 = '';
                var count_or_value2 = $('.region-radio-input2:checked').val();
                var region_ids2 = [.01];

                $('.region-blocks2').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        region_ids2.push(parseInt($(obj).attr('region_id')))
                    }
                })
                 var custom_range2 = false
                 var custom_start2 = false
                 var custom_end2 = false
                    this.rpc("/jupiter_dashboard_tres/bookings_registrations_region_wise2", {'frequency': frequency2, 'region_ids': region_ids2, 'count_or_value': count_or_value2, 'custom_start': custom_start2, 'custom_end': custom_end2}).then((result) => {
                        self.applyRegionWiseChart2(result)
                        self.applyRegionWiseBookingChart2(result[0][0]['data'], result[1])
                        self.applyRegionWiseRegistrationChart2(result[0][1]['data'], result[1])
                    })

                    })
                    this.rpc('/jupiter_dashboard_tres/get_cluster_data', {}).then((result) => {
                        $('#cluster-container').empty().append(result)
                    })
                    this.rpc('/jupiter_dashboard_tres/get_project_data', {}).then((result) => {
                        $('#project-container').empty().append(result)
                    })
                    var region_ids = []
                $('.region-blocks').each(function(i, obj) {
                    if($(obj).hasClass('active')){
                        region_ids.push(parseInt($(obj).attr('region_id')))
                    }
                })
                    console.log('/jupiter_dashboard_tres/bookings_registrations4');
                    this.rpc('/jupiter_dashboard_tres/bookings_registrations', {}).then((result) => {
                        $('.quarter_label').empty().append(result['quarter_label'])
                        $('.half_label').empty().append(result['half_label'])
                        $('.year_label').empty().append(result['year_label'])
                        self.applyRegionBookingRegistration(result)
                        self.applyClusterBookingRegistration(result)
                        self.applyProjectBookingRegistration(result)

                        $('.today_booking_link').attr('report_attr', result['today_booking_attrs']);
                        $('.week_booking_link').attr('report_attr', result['week_booking_attrs']);
                        $('.month_booking_link').attr('report_attr', result['month_booking_attrs']);
                        $('.year_booking_link').attr('report_attr', result['year_booking_attrs']);
                        $('.quarter_booking_link').attr('report_attr', result['quarter_booking_attrs']);
                        $('.half_booking_link').attr('report_attr', result['half_booking_attrs']);

                        $('.today_registration_link').attr('report_attr', result['today_registration_attrs']);
                        $('.week_registration_link').attr('report_attr', result['week_registration_attrs']);
                        $('.month_registration_link').attr('report_attr', result['month_registration_attrs']);
                        $('.year_registration_link').attr('report_attr', result['year_registration_attrs']);
                        $('.quarter_registration_link').attr('report_attr', result['quarter_registration_attrs']);
                        $('.half_registration_link').attr('report_attr', result['half_registration_attrs']);

                        $('#today_booking_cp_domain').attr('domain', result['today_booking_cp_domain']);
                        $('#week_booking_cp_domain').attr('domain', result['week_booking_cp_domain']);
                        $('#month_booking_cp_domain').attr('domain', result['month_booking_cp_domain']);
                        $('#quarter_booking_cp_domain').attr('domain', result['quarter_booking_cp_domain']);
                        $('#half_booking_cp_domain').attr('domain', result['half_booking_cp_domain']);
                        $('#year_booking_cp_domain').attr('domain', result['year_booking_cp_domain']);
                    })
                    this.rpc("/jupiter_dashboard_tres/bookings_registrations_region_wise", {'frequency': 'month'}).then((result) => {
                        self.applyRegionWiseChart(result)
                        self.applyRegionWiseBookingChart(result[0][0]['data'], result[1])
                        self.applyRegionWiseRegistrationChart(result[0][3]['data'], result[1])
                    })
    //                'region_or_cluster': 'cluster'
                    this.rpc("/jupiter_dashboard_tres/bookings_registrations_region_wise", {'frequency': 'month', 'region_or_cluster': 'cluster'}).then((result) => {
                        self.applyClusterWiseChart(result)
                        self.applyClusterWiseBookingChart(result[0][0]['data'], result[1])
                        self.applyClusterWiseRegistrationChart(result[0][3]['data'], result[1])
                    })
    //                 'region_or_cluster': 'project'
                    this.rpc("/jupiter_dashboard_tres/bookings_registrations_region_wise", {'frequency': 'month', 'region_or_cluster': 'project'}).then((result) => {
                        self.applyProjectWiseChart(result)
                        self.applyProjectWiseBookingChart(result[2]['gross']['values'], result[2]['gross']['categories'])
                        self.applyProjectWiseRegistrationChart(result[2]['registration']['values'], result[2]['registration']['categories'])
                    })
                    this.rpc("/jupiter_dashboard_tres/budget_actual_comparison", {'registration_type': false}).then((result) => {
                        self.ActualBudgetComparison(result, 'booking')
                    })
                    this.rpc('/jupiter_dashboard_tres/cp_booked_count', {}).then((result) => {
                        $('#today_booking_cp_count').empty().append(result['today_booking_cp_count'])
                        $('#week_booking_cp_count').empty().append(result['week_booking_cp_count'])
                        $('#month_booking_cp_count').empty().append(result['month_booking_cp_count'])
                        $('#year_booking_cp_count').empty().append(result['year_booking_cp_count'])
                        $('#quarter_booking_cp_count').empty().append(result['quarter_booking_cp_count'])
                        $('#half_booking_cp_count').empty().append(result['half_booking_cp_count'])
                    })
                    this.rpc('/jupiter_dashboard_tres/get_cp_count', {}).then((result) => {
                        $('#month_cps').empty().append(result['month_cps'])
                        $('#quarter_cps').empty().append(result['quarter_cps'])
                        $('#half_cps').empty().append(result['half_cps'])
                        $('#year_cps').empty().append(result['year_cps'])

                        $('#month_cps_active').empty().append(result['month_cps_active'])
                        $('#quarter_cps_active').empty().append(result['quarter_cps_active'])
                        $('#half_cps_active').empty().append(result['half_cps_active'])
                        $('#year_cps_active').empty().append(result['year_cps_active'])

                        $('#month_cps_dormant').empty().append(result['month_cps_dormant'])
                        $('#quarter_cps_dormant').empty().append(result['quarter_cps_dormant'])
                        $('#half_cps_dormant').empty().append(result['half_cps_dormant'])
                        $('#year_cps_dormant').empty().append(result['year_cps_dormant'])

                        $('#month_cp_domain').attr('domain', result['month_cp_domain']);
                        $('#quarter_cp_domain').attr('domain', result['quarter_cp_domain']);
                        $('#half_cp_domain').attr('domain', result['half_cp_domain']);
                        $('#year_cp_domain').attr('domain', result['year_cp_domain']);

                        $('#month_cp_active_domain').attr('active_domain', result['month_cp_active_domain']);
                        $('#quarter_cp_active_domain').attr('active_domain', result['quarter_cp_active_domain']);
                        $('#half_cp_active_domain').attr('active_domain', result['half_cp_active_domain']);
                        $('#year_cp_active_domain').attr('active_domain', result['year_cp_active_domain']);

                        $('#month_cp_active_domain').attr('dormant_domain', result['month_cps_dormant_domain']);
                        $('#quarter_cp_active_domain').attr('dormant_domain', result['quarter_cps_dormant_domain']);
                        $('#half_cp_active_domain').attr('dormant_domain', result['half_cps_dormant_domain']);
                        $('#year_cp_active_domain').attr('dormant_domain', result['year_cps_dormant_domain']);

                        self.applyCpCountChart(result)
                    })
                    this.rpc('/jupiter_dashboard_tres/get_last_6_month_cp_booking', {}).then((result) => {
                        self.applyCpBookingChart(result)
                    })
                    this.rpc('/jupiter_dashboard_tres/get_region_select_data', {}).then((result) => {
                        $('#region_select').empty().append(result)
                        $('#region_select').select2()
                    })
                    this.rpc('/jupiter_dashboard_tres/get_cluster_select_data', {}).then((result) => {
                        $('.cluster-select-div').empty().append(result)
                    })
                    this.rpc("/jupiter_dashboard_tres/sales_inventory", {'region_wise': false, 'project_wise': true, 'project_region': false}).then((result) => {
                        self.projectOrRegionFlatStatus(result, true, true)
                    })
                    this.rpc('/jupiter_dashboard_tres/get_region', {}).then((result) => {
                        $('#region_selection .dropdown-menu').empty().append(result[0])
                        $('#walk_in_region_selection .dropdown-menu').empty().append(result[0])
                        $('#configuration_select').empty().append(result[1])
                        $('#configuration_select').select2()
                    })
                    this.rpc('/jupiter_dashboard_tres/get_cluster', {}).then((result) => {
                        $('#cluster_select_div').empty().append(result)
                        $('#cluster_select').select2()
                    })
                    this.rpc('/jupiter_dashboard_tres/walk_in_get_cluster', {}).then((result) => {
                        $('#walk_in_cluster_select_div').empty().append(result)
                        $('#walk_in_cluster_select').select2()
                    })
                    this.rpc('/jupiter_dashboard_tres/get_top_20_cp', {}).then((result) => {
                        $('#cp_tbody').empty().append(result)
                    })
                    $('.manpower_loader').removeClass('invisible')
                    this.rpc("/jupiter_dashboard_tres/manpower_productivity", {frequency: 'month'}).then((result) => {
    //                    self.ManPowerProductivityRadialChart(result[0])
                        $('#man_power_radial_chart').empty().append(result[0])
                        self.ManPowerProductivityRegionChart(result[1])
                        self.ManPowerProductivityClusterChart(result[2])
                        $('#manpower_project_tbody').empty().append(result[3])
                        $('.manpower_loader').addClass('invisible')

                    })
                    $('#walk_in_region_loader').show()
                    $('.walk_in_region_div table').css({'filter': 'blur(4px)'})
                    this.rpc('/jupiter_dashboard_tres/walk_in_data', {}).then((result) => {
                        if(result == 'disable'){
                            $('#walk_in_conversion_row').addClass('d-none')
                        }else{
                            self.WalkInRegionWise(result)
                            $('#walk_in_region_loader').hide()
                            $('.walk_in_region_div table').css({'filter': 'unset'})
    //                        $('#walk_in_conversion_row').removeClass('d-none')
                        }
                    })
                    $('#walk_in_project_loader').show()
                    $('.walk_in_project_div table').css({'filter': 'blur(4px)'})
                    this.rpc("/jupiter_dashboard_tres/walk_in_data", {'model': 'project'}).then((result) => {
                        if(result == 'disable'){
                            $('#walk_in_conversion_row').addClass('d-none')
                        }else{
                            $('#walk_in_project_tbody').empty().append(result)
                            $('#walk_in_project_loader').hide()
                            $('.walk_in_project_div table').css({'filter': 'unset'})
    //                        $('#walk_in_conversion_row').removeClass('d-none')
                        }
                    })
                    this.rpc("/jupiter_dashboard_tres/cp_booking_units_region_wise", {'model': 'region'}).then((result) => {
                        self.CpBookingUnitsRegionWise(result, 'Region')
                    })
                })
            },
}

// Register the action
registry.category("actions").add("jupiter_dashboard_tres", JupiterDashboardTres);
