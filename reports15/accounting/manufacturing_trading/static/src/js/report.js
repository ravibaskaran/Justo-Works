odoo.define('manufacturing_trading.form_controller', function (require) {
"use strict";

    var FormController = require('web.FormController');
    var rpc = require('web.rpc');

    FormController.include({
        events: _.extend(FormController.prototype.events, {
            'click .o_general_ledger_action': 'beta_general_ledger_action',
            'click #o_general_ledger_pdf_action': 'beta_general_ledger_pdf_action',
        }),

        beta_general_ledger_pdf_action : function(ev){
            var self = this
            var report = document.getElementById('wrapwrap').outerHTML;
            rpc.query({
                    model: 'trading.pdf',
                    method: 'get_pdf_report',
                    kwargs: {report:report},
                }).then(function (result){
                var reportname = 'manufacturing_trading.trading_pdf?docids=' + result;
                var action = {
                'type': 'ir.actions.report',
                'report_type': 'qweb-pdf',
                'report_name': reportname,
                'report_file': 'manufacturing_trading.trading_pdf',
            };
            return self.do_action(action);
            });
        },

        beta_general_ledger_action: function (ev) {
            ev.preventDefault();
            return this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'beta.general.ledger',
                context: {default_day_summary: false,
                    default_date_from:$(ev.currentTarget).data('date-from'),
                    default_date_to:$(ev.currentTarget).data('date-to'),
                    default_account_ids:[(0,0,$(ev.currentTarget).data('res-id'))],
                    branch_id:$(ev.currentTarget).data('branch-ids')
                },
                views: [[false, 'form']],
                target: 'current'
            }).then(function(){
                $('.o_panel_get_report_beta').click();
            })
        },
    })
})