odoo.define('real_estate_sheets.relational_fields', function(require) {
"use strict";

    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var registry = require('web.field_registry');
    var rpc = require('web.rpc');
    var _t = core._t;
    var Dialog = require('web.Dialog');
    var relational_fields = require('web.relational_fields');

    relational_fields.FieldMany2One.include({
        _onFieldChanged: function (event) {
            var res = this._super();
            var self = this;
            if(this.model == "budget.sheet" && this.name == "project_id"){
                rpc.query({
                    model: "budget.sheet",
                    method: "get_evaluation_id",
                    args: [event.data.changes.project_id.id],
                }).then(function(result) {
                    if(result){
                        var message = _t("Do you want to update data from evaluation sheet?");
                        var def;
                        def = new Promise(function (resolve, reject) {
                            var dialog = Dialog.confirm(self, message, {
                                title: _t("Confirmation"),
                                buttons: [{
                                    text: _t('Update Project Info Only'),
                                    close: true,
                                    click: () => {
                                        $('input[name="evaluation_sheet"]').val('')
                                        $('input[name="evaluation_sheet"]').change()
                                        $('input[name="evaluation_sheet"]').val(result)
                                        $('input[name="evaluation_sheet"]').change()
                                    },
                                },
                                {
                                    text: _t('Update All Data'),
                                    close: true,
                                    click: () => {
                                        $('input[name="evaluation_sheet"]').val('')
                                        $('input[name="evaluation_sheet"]').change()
                                        $('input[name="evaluation_sheet"]').val('update_all_from_evaluation')
                                        $('input[name="evaluation_sheet"]').change()
                                    },
                                },
                                {
                                    text: _t('No'),
                                    classes: 'btn-primary',
                                    close: true,
                                    click: reject,
                                }],
                                cancel_callback: reject,
                            });
                            dialog.on('closed', def, reject);
                        });
                        return def;
                    }
                });
            }
            return res;

        },
    });
});