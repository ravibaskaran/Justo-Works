odoo.define('beta_reports_base.form_controller', function (require) {
"use strict";

    var FormController = require('web.FormController');
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var FormView = require('web.FormView');

    FormController.include({
        events: _.extend(FormController.prototype.events, {
            'click #beta_excel_print': 'beta_excel_print',
            'click #beta_direct_print': 'beta_direct_print',
            'click .o_beta_report_action': 'beta_click_action',
            'click #beta_excel_print_daybook_co_op': 'beta_excel_print_daybook_co_op',
            'click #beta_excel_print_rnd_register': 'beta_excel_print_rnd_register',
            'click #beta_excel_profit_and_loss': 'beta_excel_profit_and_loss',
            'click #o_profit_loss_balance_sheet_pdf_action': 'beta_profit_loss_balance_pdf',
        }),

        beta_profit_loss_balance_pdf : function(ev){
            var self = this
            var report = document.getElementById('wrapwrap').outerHTML;
            rpc.query({
                    model: 'profit.reports.pdf',
                    method: 'get_pdf_report',
                    kwargs: {report:report},
                }).then(function (result){
                var reportname = 'profit_loss_balance_sheet.profit_reports_pdf?docids=' + result;
                var action = {
                'type': 'ir.actions.report',
                'report_type': 'qweb-pdf',
                'report_name': reportname,
                'report_file': 'profit_loss_balance_sheet.profit_reports_pdf',
            };
            return self.do_action(action);
            });
        },

        willRestore: function (shouldReload) {
            this._super.apply(this, arguments);
            console.log('this',this)
            const models = ["beta.payroll.report","beta.manufacturing.trading","beta.partner.ledger","beta.trial.balance","beta.daybook.co.op","beta.profit.loss.balance.sheet","rnd.register","beta.day.book","beta.cash.book","beta.general.ledger","beta.partner.ledger","appointment"];
            if (models.includes(this.modelName))
            {
                this.mode = 'edit';
            }
            else
            {
                this.mode = this.model.isNew(this.handle) ? 'edit' : 'readonly';
            }
            return this._setMode(this.mode);
        },

        beta_click_action: function (ev) {
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

        beta_direct_print: function(ev) {
            var mode='iframe';
            var close=mode=="popup";
            var options={mode:mode,popClose:close};
            $('#wrapwrap').printArea(options);
        },

        beta_excel_print: function(ev) {
            var name = $('.beta_main_panel').attr('report')
            var divdiv=document.getElementById('wrapwrap');
            if (divdiv){
                var tright=divdiv.getElementsByClassName('text-right');
                for (var i = 0; i < tright.length; i++) {
                    var tr=tright[i].parentElement;
                    var td_in_tr=tr.getElementsByTagName('TD');
                    if(td_in_tr.length!=0 && tright[i]!= td_in_tr[0]){
                        var number_style = tright[i].getAttribute("style") + "mso-number-format:0\.00;"
                        tright[i].setAttribute("style", number_style);
                    }
                }
                var obj=document.getElementById('logo_company');
                if (obj){
                    var img_parent = obj.parentNode;
                    img_parent.removeChild (obj);
                }
                var table=document.getElementById('wrapwrap').innerHTML;
                var table1="<html><style>.text-center {text-align: center !important;}.text-right{text-align: right !important;}.text-left {text-align: left !important;}</style><body><table>"+table+"</table></body></html>";
                var myBlob = new Blob([table1], {
                    type: 'application/vnd.ms-excel'
                });
                if (obj){
                    img_parent.appendChild (obj);
                }
                var url = window.URL.createObjectURL(myBlob);
                var a = document.createElement("a");
                document.body.appendChild(a);
                a.href = url;
                a.download = name+'.xls';
                a.click();
                setTimeout(function() {
                    window.URL.revokeObjectURL(url);
                }, 0);
            }
        },

        // Daybook Co Op
        beta_excel_print_daybook_co_op : function(ev){
            var fst_heading =$(":header")[0];
            var name = "Daybook Co-Operative"
            var divdiv=document.getElementById('wrapwrap');
            var tright=divdiv.getElementsByClassName('text-right');
            for (var i = 0; i < tright.length; i++) {
                var tr=tright[i].parentElement;
                var td_in_tr=tr.getElementsByTagName('TD');
                if(td_in_tr.length!=0 && tright[i]!= td_in_tr[0]){
                    tright[i].setAttribute("style","mso-number-format:0\.00;");
                }
            }

            // Purpose → Notes: To remove logo from the table while downloading excel
            var obj = document.getElementById('logo_company');
            var img_parent = obj.parentNode;
            img_parent.removeChild(obj);

            // Purpose → Notes: To Treat two table as one to get a beter result
            var orginal = $("#wrapwrap").html()

            $(".container_div").each(function(i, container_div){
                var td_1 = $(container_div).find(".div_1").html();
                var td_2 = $(container_div).find(".div_2").html();
                var td_3 = $(container_div).find(".div_3").html();
                var receipt_td = $(container_div).find(".receipt_div").html();
                var payment_td = $(container_div).find(".payment_div").html();

                // Purpose → Notes: Combining all 3 table into one table
                var new_tab = "<table><tr><td>"+receipt_td+"</td><td>"+payment_td+"</td></tr><tr><td>"+td_1+"</td><td>"+td_2+"</td></tr><tr>"+td_3+"</tr></table>"
                $(container_div).find(".div_1").parent().html(new_tab);
            })
            var table=document.getElementById('wrapwrap').innerHTML;
            var table1="<html><style>.text-center {text-align: center !important;}.text-right{text-align: right !important;}.text-left {text-align: left !important;}</style><body><table>"+table+"</table></body></html>";
            var myBlob = new Blob([table1], {
                type: 'application/vnd.ms-excel'
            });

            // Purpose → Notes To append removed logo back
            img_parent.appendChild(obj);
            $("#wrapwrap").html(orginal);
            var url = window.URL.createObjectURL(myBlob);
            var a = document.createElement("a");
            document.body.appendChild(a);
            a.href = url;

            // Purpose → Notes: Download Excel with given name
            a.download = name+'.xls';
            a.click();

            // Purpose → Notes: adding some delay in removing the dynamically created link solved the problem in FireFox
            setTimeout(function() {
                window.URL.revokeObjectURL(url);
            }, 0);
        },

        // R&D Register
        beta_excel_print_rnd_register: function(ev){
            var fst_heading =$(":header")[0];
            var name = "R & D Report"
            var divdiv=document.getElementById('wrapwrap');
            var tright=divdiv.getElementsByClassName('text-right');
            for (var i = 0; i < tright.length; i++) {
                var tr=tright[i].parentElement;
                var td_in_tr=tr.getElementsByTagName('TD');
                if(td_in_tr.length!=0 && tright[i]!= td_in_tr[0]){
                    tright[i].setAttribute("style", tright[i].getAttribute('style')+';mso-number-format:0\.00;');
                }
            }
            var obj=document.getElementById('logo_company');
            var img_parent = obj.parentNode;
            img_parent.removeChild (obj);
            var parent1 = $("#tabl1-id").parent();
            var parent_table1 = $("#tabl1-id").parent().html();
            var parent2 = $("#tabl2-id").parent();
            var parent_table2 = $("#tabl2-id").parent().html();
            var td_1 = $("#tabl-td1").html();
            var td_2 = $("#tabl-td2").html();
            var td_3 = $("#tabl-td3").html();
            var td_4 = $("#tabl-td4").html();
            var new_table = "<table><tr><td>"+td_1+"</td>"+"<td>"+td_2+"</td></tr><tr><td>"+td_3+"</td>"+"<td>"+td_4+"</td></tr></table>";
            $("#tabl1-id").parent().html(new_table);
            var table=document.getElementById('wrapwrap').innerHTML;
            var table1="<html><style>.text-center {text-align: center !important;}.text-right{text-align: right !important;}.text-left {text-align: left !important;}</style><body><div>"+table+"</div></body></html>";
            var myBlob = new Blob([table1], {
                type: 'application/vnd.ms-excel'
            });
            img_parent.appendChild (obj);
            parent1.html(parent_table1);
            var url = window.URL.createObjectURL(myBlob);
            var a = document.createElement("a");
            document.body.appendChild(a);
            a.href = url;
            a.download = name+'.xls';
            a.click();

            //Purpose : adding some delay in removing the dynamically created link solved the problem in FireFox
            setTimeout(function() {
                window.URL.revokeObjectURL(url);
            }, 0);
        },

        // Profit and Loss and Balance Sheet
        beta_excel_profit_and_loss: function(ev){
            var fst_heading =$(":header")[0];
            var name = fst_heading.textContent || fst_heading.innerText;
            if ($('h4.mt20.mb20').length > 0){
                name = $('h4.mt20.mb20')[0].innerText
            }
            var divdiv=document.getElementById('wrapwrap');
            var tright=divdiv.getElementsByClassName('text-right');
            for (var i = 0; i < tright.length; i++) {
                var tr=tright[i].parentElement;
                var td_in_tr=tr.getElementsByTagName('TD');
                if(td_in_tr.length!=0 && tright[i]!= td_in_tr[0]){
                    tright[i].setAttribute("style", tright[i].getAttribute('style')+';mso-number-format:0\.00;');
                }
            }
            var obj=document.getElementById('logo_company');
            var img_parent = obj.parentNode;
            img_parent.removeChild (obj);
            var parent1 = $("#tabl1-id").parent();
            var parent_table1 = $("#tabl1-id").parent().html();
            var parent2 = $("#tabl2-id").parent();
            var parent_table2 = $("#tabl2-id").parent().html();
            var td_1 = $("#tabl-td1").html();
            var td_2 = $("#tabl-td2").html();
            var td_3 = $("#tabl-td3").html();
            var td_4 = $("#tabl-td4").html();
            var new_table = "<table><tr><td>"+td_1+"</td>"+"<td>"+td_2+"</td></tr><tr><td>"+td_3+"</td>"+"<td>"+td_4+"</td></tr></table>";
            $("#tabl1-id").parent().html(new_table);
            var table=document.getElementById('wrapwrap').innerHTML;
            var table1="<html><style>.text-center {text-align: center !important;}.text-right{text-align: right !important;}.text-left {text-align: left !important;}</style><body><table>"+table+"</table></body></html>";
            var myBlob = new Blob([table1], {
                type: 'application/vnd.ms-excel'
            });
            img_parent.appendChild (obj);
            parent1.html(parent_table1);
            var url = window.URL.createObjectURL(myBlob);
            var a = document.createElement("a");
            document.body.appendChild(a);
            a.href = url;
            a.download = name+'.xls';
            a.click();

            // Purpose : adding some delay in removing the dynamically created link solved the problem in FireFox
            setTimeout(function() {
                window.URL.revokeObjectURL(url);
            }, 0);
        },

    })

})