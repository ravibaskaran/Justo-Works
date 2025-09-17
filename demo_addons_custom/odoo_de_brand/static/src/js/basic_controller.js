odoo.define('real_estate_sheets.basic_controller', function(require) {
"use strict";

    var BasicController = require('web.BasicController');
    var FormController = require('web.FormController');
    var core = require('web.core');
    var _t = core._t;
    var Dialog = require('web.Dialog');

    BasicController.include({

        canBeRemoved: function () {
            var self = this;
            if(this.isDirty()){
                var message = _t("The record has been modified, your changes will be discarded. Do you want to proceed?");
                var def;
                def = new Promise(function (resolve, reject) {
                    var dialog = Dialog.confirm(self, message, {
                        title: _t("Warning"),
                        confirm_callback: resolve.bind(self, true),
                        cancel_callback: reject,
                    });
                    dialog.on('closed', def, reject);
                });
                return def;
            }else{
                return this.saveChanges(this.handle);
            }
        },
    })

    FormController.include({
        _onBeforeUnload: function () {
            // this._urgentSave(this.handle);
        },
    })
})