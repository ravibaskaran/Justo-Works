odoo.define('cash_book.form_controller', function (require) {
"use strict";

    var FormController = require('web.FormController');
    var rpc = require('web.rpc');

    FormController.include({
        events: _.extend(FormController.prototype.events, {
            'click #cash_book_pdf_action': 'beta_cash_book_pdf_action',
        }),

        beta_cash_book_pdf_action : function(ev){
            var self = this
            var report = document.getElementById('wrapwrap').outerHTML;
            rpc.query({
                    model: 'cash.book.pdf',
                    method: 'get_pdf_report',
                    kwargs: {report:report},
                }).then(function (result){
                var reportname = 'cash_book.cash_book_pdf?docids=' + result;
                var action = {
                'type': 'ir.actions.report',
                'report_type': 'qweb-pdf',
                'report_name': reportname,
                'report_file': 'cash_book.cash_book_pdf',
            };
            return self.do_action(action);
            });
        },

    })
})