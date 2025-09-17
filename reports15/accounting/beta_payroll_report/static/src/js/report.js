odoo.define('beta_payroll_report.report', function (require) {
"use strict";

    var FormController = require('web.FormController');
    var rpc = require('web.rpc');

    FormController.include({
        events: _.extend(FormController.prototype.events, {
            'click .beta_redirect_action' : 'beta_redirect_action',
        }),


        beta_redirect_action: function(ev){
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

    })
})