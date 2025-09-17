odoo.define('rnd_register.form_controller', function (require) {
"use strict";

    var FormController = require('web.FormController');
    var rpc = require('web.rpc');

    FormController.include({
        events: _.extend(FormController.prototype.events, {
            'click #beta_direct_pdf_rnd': 'beta_direct_pdf_rnd',
        }),

        beta_direct_pdf_rnd : function(ev){
            var self = this
            var report = document.getElementById('wrapwrap').outerHTML;
            rpc.query({
                    model: 'rnd_register.pdf',
                    method: 'get_pdf_report',
                    kwargs: {report:report},
                }).then(function (result){
                var reportname = 'rnd_register.rnd_register_pdf?docids=' + result;
                var action = {
                'type': 'ir.actions.report',
                'report_type': 'qweb-pdf',
                'report_name': reportname,
                'report_file': 'rnd_register.rnd_register_pdf',
            };
            return self.do_action(action);
            });
        },


    })
})