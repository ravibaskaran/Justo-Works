odoo.define('real_estate_sheets.button_generate', function(require) {
"use strict";

    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var registry = require('web.field_registry');
    var rpc = require('web.rpc');
    var _t = core._t;
    var Dialog = require('web.Dialog');

    var ButtonGenerateWidget = AbstractField.extend({
        events: _.extend({}, AbstractField.prototype.events, {
            'click': '_onClicked',
        }),
        description: "",

        isSet: function () {
            return true;
        },

        _render: function () {
            var $button = $('<button>Generate Month</button>', {
                type: 'button',
            }).addClass('btn btn-sm btn-secondary o_button_generate_toggle px-3 py-2');
            this.$el.html($button);
        },

        _onClicked: function (event) {
            var self = this;
            if(this.name == "commission_generate_button"){
                if($('select[name="retainer_month"]').val() == 'false' || $('select[name="forecast_month"]').val() == 'false'){
                    var message = _t("Please select No. of Months and No. of Months(Forecast)");
                    var def;
                    def = new Promise(function (resolve, reject) {
                        var dialog = Dialog.alert(self, message, {
                            title: _t("Warning"),
                            cancel_callback: reject,
                        });
                        dialog.on('closed', def, reject);
                    });
                    return def;
                }
                if(this.recordData.sales_forecast_lines.count > 0){
                    var message = _t("Already generated, your changes will be discarded. Do you want to proceed?");
                    var def;
                    def = new Promise(function (resolve, reject) {
                        var dialog = Dialog.confirm(self, message, {
                            title: _t("Confirmation"),
                            confirm_callback: function () {
                                if(self.value){
                                    self._setValue(false)
                                }
                                else{
                                    self._setValue(true)
                                }
                            },
                            cancel_callback: reject,
                        });
                        dialog.on('closed', def, reject);
                    });
                    return def;
                }
            }
            if(this.value){
                this._setValue(false)
            }
            else{
                this._setValue(true)
            }
        },
    });

    registry.add("generate_button_toggle", ButtonGenerateWidget);
});
