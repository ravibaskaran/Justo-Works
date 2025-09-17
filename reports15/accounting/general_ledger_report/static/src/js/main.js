odoo.define('general_ledger_report.report_general_ledger', function (require) {
'use strict';

    var core = require('web.core');
    var framework = require('web.framework');
    var stock_report_generic = require('reports_script.report_generic');
    var QWeb = core.qweb;
    var _t = core._t;
    var rpc = require('web.rpc');

    var Report = stock_report_generic.extend({
        events: {
            'click .o_general_action': '_onClickAction',
            'click #excel_print': 'printExcel',
            'click #direct_print': 'directPrint',
             },

        directPrint: function() {
            var panel = document.getElementById("wrapwrap");
            var landscape_print = document.getElementById("landscape_print");
            var printWindow = window.open('', '', '');
            if(landscape_print){
                printWindow.document.write('<html><style  type="text/css">@page { size: 35cm 25cm !important;margin: 1cm 1cm 1.55cm .8cm !important; }.text-center {text-align: center !important;}.text-right{text-align: right !important;}.text-left {text-align: left !important;} .daybook-table tr td{word-break: break-all; !important }</style><head><link rel="stylesheet" href="/general_ledger_report/static/src/css/bootstrap.css" />');
                printWindow.document.write('</head><body >');
                printWindow.document.write(panel.innerHTML);
                printWindow.document.write('</body></html>');
            }else{
                printWindow.document.write('<html><style>@page { size: portrait ; }.text-center {text-align: center !important;}.text-right{text-align: right !important;}.text-left {text-align: left !important;}</style><head><link rel="stylesheet" href="/general_ledger_report/static/src/css/bootstrap.css" />');
                printWindow.document.write('</head><body >');
                printWindow.document.write(panel.innerHTML);
                printWindow.document.write('</body></html>');
            }
            printWindow.document.close();
            setTimeout(function () {
                printWindow.print();
            }, 500);
            return false;
         },

        printExcel: function() {
            var fst_heading =$(":header")[0];
            var name = fst_heading.textContent || fst_heading.innerText;
            var divdiv=document.getElementById('wrapwrap');
            var tright=divdiv.getElementsByClassName('text-right');
            for (var i = 0; i < tright.length; i++) {
                var tr=tright[i].parentElement;
                var td_in_tr=tr.getElementsByTagName('TD');
                if(td_in_tr.length!=0 && tright[i]!= td_in_tr[0]){
                    tright[i].setAttribute("style","mso-number-format:0\.00;");
                }
            }
            var obj=document.getElementById('logo_company');
            var img_parent = obj.parentNode;
            img_parent.removeChild (obj);
            var table=document.getElementById('wrapwrap').innerHTML;
            var table1="<html><style>.text-center {text-align: center !important;}.text-right{text-align: right !important;}.text-left {text-align: left !important;}</style><body><table>"+table+"</table></body></html>";
            var myBlob = new Blob([table1], {
                type: 'application/vnd.ms-excel'
            });
            img_parent.appendChild (obj);
            var url = window.URL.createObjectURL(myBlob);
            var a = document.createElement("a");
            document.body.appendChild(a);
            a.href = url;
            a.download = name+'.xls';
            a.click();
            //adding some delay in removing the dynamically created link solved the problem in FireFox
            setTimeout(function() {
                window.URL.revokeObjectURL(url);
            }, 0);
        },

        get_html: function() {
            var self = this;
            var url = window.location.href
            console.log('self',self,$('.o_control_panel >.o_cp_left > .o_cp_buttons > div.o_list_buttons.o_panel_report_buttons'));
            var args = [
                this.given_context.searchDateFrom,
                this.given_context.searchDateTo,
                this.given_context.report_account,
                this.given_context.searchInitial,
                this.given_context.report_branch,
                this.given_context.daySummary,
                this.given_context.breadcrumbs,
                this.given_context.monthSummary,
                this.given_context.monthTotal,
            ];
            return this._rpc({
                model: 'report.general_ledger_report.report_general_ledger',
                method: 'get_html',
                args: args,
                context: this.given_context,
            })
            .then(function (result) {
                self.data = result;
            });
        },

        set_html: function() {
            var self = this;
            return this._super().then(function () {
                self.$('.o_content').html(self.data.lines);
                self.renderSearch();
                self.update_cp();
            });
        },

        update_cp: function () {
            var status = {
                cp_content: {
                    $buttons: this.$buttonPrint,
                    $searchview_buttons: this.$searchView
                },
            };
            return this.updateControlPanel(status);
        },

        renderSearch: function () {
            this.$buttonPrint = $(QWeb.render('general_ledger_report.button'));
            this.$buttonPrint.find('.o_pdf_print').on('click', this._onClickPrint.bind(this));
            this.$searchView = $(QWeb.render('general_ledger_report.report_search', _.omit(this.data, 'lines')));
            this.$searchView.find('.o_general_ledger_day_summary').on('change', this._onChangeDay.bind(this));
            this.$searchView.find('.o_general_ledger_month_summary').on('change', this._onChangeMonth.bind(this));
            this.$buttonPrint.find('.o_panel_get_report').on('click', this._onClickGetReport.bind(this));
            if ($('#s2id_account_ids').length==0){
                this.$searchView.find('.o_general_ledger_account').select2();
                var date = new Date();
                var month = String(date.getMonth() + 1).padStart(2, '0');
                var year = date.getFullYear();
                var now_date = String(date.getDate()).padStart(2, '0');
                if(month >=0 & month <=3){
                    var fyear = year-1
                    var from_date = '01/04/'+fyear;
                    var to_date =  now_date+'/'+month+'/'+year;
                }
                else{
                    var from_date = '01/04/'+year;
                    var to_date = now_date+'/'+month+'/'+year;
                }
                $(this.$searchView.find('#date_from')).val(from_date)
                $(this.$searchView.find('#date_to')).val(to_date)
                $(this.$searchView.find('#date_from')).datepicker({'dateFormat': 'dd/mm/yy'});
                $(this.$searchView.find('#date_to')).datepicker({'dateFormat': 'dd/mm/yy'});
            }
        },

        _onClickPrint: function (ev) {
            var self = this
            var report = document.getElementById('wrapwrap').outerHTML;
            console.log('fhoefhhoehegheogheoih')
            rpc.query({
                model: 'general.ledger.pdf',
                method: 'get_pdf_report',
                kwargs: {report:report},
            }).then(function (result){
                var reportname = 'general_ledger_report.general_ledger_pdf?docids=' + result;
                var action = {
                'type': 'ir.actions.report',
                'report_type': 'qweb-pdf',
                'report_name': reportname,
                'report_file': 'general_ledger_report.general_ledger_pdf',
            };
            return self.do_action(action);
            });
        },

        _onClickGetReport: function (ev) {
            var date_from = document.getElementById('date_from').value;
            var date_to =document.getElementById('date_to').value;
            var farray = date_from.split("/")
            if(farray.length == 3){
                var fyl = farray[2].length;
                var fm = farray[1]
                var fy = farray[2];
                var fd = farray[0];
                var fnan_date = fm+'/'+fd+'/'+fy;
                var fget_date = new Date(fnan_date) !== "Invalid Date" && !isNaN(new Date(fnan_date));
                var fdate = new Date(fnan_date).getDate();
            }
            var tarray = date_to.split("/")
            if(tarray.length == 3){
                var tyl = tarray[2].length;
                var td = tarray[0];
                var tm = tarray[1];
                var ty = tarray[2];
                var tnan_date = tm+'/'+td+'/'+ty;
                var tget_date = new Date(tnan_date) !== "Invalid Date" && !isNaN(new Date(tnan_date));
                var tdate = new Date(tnan_date).getDate();
            }
            if (farray.length == 3 && fget_date == true && fyl == 4 && fdate == fd){
                const dateArray = date_from.split("/");
                var month = dateArray[1];
                var year = dateArray[2];
                var now_date = dateArray[0];
                this.given_context.searchDateFrom = +year+'-'+month+'-'+now_date;
                if (tarray.length == 3 && tget_date == true && tyl == 4 && tdate == td){
                    const dateArray = date_to.split("/");
                    var month = dateArray[1];
                    var year = dateArray[2];
                    var now_date = dateArray[0];
                    this.given_context.searchDateTo = +year+'-'+month+'-'+now_date;
                }
                else{
                    $.alert({
                        title: 'Alert!',
                        content: 'Please Enter Correct Date To Format',
                        onDestroy: function() {
                            $('.o_general_ledger_date_to').focus();
                        }
                    });
                }
            }
            else{
                $.alert({
                    title: 'Alert!',
                    content: 'Please Enter Correct Date From Format',
                    onDestroy: function() {
                        $('.o_general_ledger_date_from').focus();
                    }
                });
            }
            var initial = document.getElementById('opening_balance');
            if (initial) {
                this.given_context.searchInitial = initial.checked;
            }
            var day_summary = document.getElementById('day_summary');
            if (day_summary) {
                this.given_context.daySummary = day_summary.checked;
            }
            var month_summary = document.getElementById('month_summary');
            if (month_summary) {
                this.given_context.monthSummary = month_summary.checked;
            }
            var month_total = document.getElementById('month_total');
            if (month_total) {
                this.given_context.monthTotal = month_total.checked;
            }
            var flag = 0;
            var report_account = []
            var account_ids = document.getElementById('account_ids');
            for(var option of document.getElementById('account_ids').options){
                if (option.selected){
                    report_account.push(option.getAttribute('data-type'))
                }
            }
            this.given_context.report_account = report_account;
            var report_branch = []
            if(document.getElementById('branch_ids')){
                for(var option of document.getElementById('branch_ids').options){
                    if (option.selected){
                        report_branch.push(option.getAttribute('data-type'))}
                    }
                if (report_branch) {
                    this.given_context.report_branch = report_branch;
                }
            }
            if (date_from && date_to){
                document.getElementById('date_from').style.border= "1px solid #cccccc";
                document.getElementById('date_from').style.borderLeft= "3px solid cadetblue";
                document.getElementById('date_to').style.border= "1px solid #cccccc";
                document.getElementById('date_to').style.borderLeft= "3px solid cadetblue";
                document.getElementById('date_from_star').style.display= "none";
                document.getElementById('date_to_star').style.display= "none";
            }
            else if(date_from && !date_to){
                document.getElementById('date_from').style.border= "1px solid #cccccc";
                document.getElementById('date_from').style.borderLeft= "3px solid cadetblue";
                document.getElementById('date_to').style.border = "1px solid red";
                document.getElementById('date_to').style.borderLeft= "3px solid red";
                document.getElementById('date_from_star').style.display= "none";
                document.getElementById('date_to_star').style.display= "unset";
                document.getElementById('date_to').focus();
                var flag = 1;
            }
            else if(date_to && !date_from){
                document.getElementById('date_to').style.border= "1px solid #cccccc";
                document.getElementById('date_to').style.borderLeft= "3px solid cadetblue";
                document.getElementById('date_from').style.border = "1px solid red";
                document.getElementById('date_from').style.borderLeft= "3px solid red";
                document.getElementById('date_from_star').style.display= "unset";
                document.getElementById('date_to_star').style.display= "none";
                document.getElementById('date_from').focus();
                var flag = 1;
            }
            else{
                document.getElementById('date_from').style.border = "1px solid red";
                document.getElementById('date_to').style.border = "1px solid red";
                document.getElementById('date_to').style.borderLeft= "3px solid red";
                document.getElementById('date_from').style.borderLeft= "3px solid red";
                document.getElementById('date_from_star').style.display= "unset";
                document.getElementById('date_to_star').style.display= "unset";
                document.getElementById('date_from').focus();
                var flag = 1;
            }
            if(flag==1){
                return false;
            }
            this._reload();
        },

        _onChangeDay: function(ev){
            var day = document.getElementById('day_summary');
            if (day.checked){
                $('.o_general_ledger_month_summary').prop('checked', false);
                 $('.month_total').removeClass('d-none');
            }
            else{
                $('.month_total').removeClass('d-none');
            }
        },

        _onChangeMonth: function(ev){
            var month = document.getElementById('month_summary');
            if (month.checked){
                $('.o_general_ledger_day_summary').prop('checked', false);
                $('.o_general_ledger_month_total').prop('checked', false);
                $('.month_total').addClass('d-none');
            }
            else{
                $('.month_total').removeClass('d-none');
                $('.o_general_ledger_month_total').prop('checked', false);
            }
        },

        _reload: function () {
            var self = this;
            return this.get_html().then(function () {
                self.$('.o_content').html(self.data.lines);
            });
        },

        _onClickAction: function (ev) {
            ev.preventDefault();
            return this.do_action({
                type: 'ir.actions.act_window',
                res_model: $(ev.currentTarget).data('model'),
                res_id: $(ev.currentTarget).data('res-id'),
                context: {
                    'active_id': $(ev.currentTarget).data('res-id')
                },
                views: [[$(ev.currentTarget).data('form'), 'form']],
                target: 'current'
            });
        },

    });
    core.action_registry.add('report_general_ledger', Report);
    return Report;
});
