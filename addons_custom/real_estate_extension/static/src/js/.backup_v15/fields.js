odoo.define('security_update.fields', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields').AbstractFieldBinary;
    var core = require('web.core');
    console.log("security_update.fields");
    var _t = core._t;
    var utils = require('web.utils');
    var rpc = require('web.rpc');
    var security_update_max_upload_fsize = 1 * 1024 * 1024; // 1Mb

    rpc.query({
        model: 'ir.attachment',
        method: 'get_max_upload_fsize',
        args: ['security_update.max_upload_fsize'],
    }).then(function (result) {
    if (result){
        security_update_max_upload_fsize = result
        }
    });

    basic_fields.include({
        on_file_change: function (e) {
            var self = this;
            var file_node = e.target;
            var allowedExtensionsRegx = /(\.jpg|\.jpeg|\.png|\.xlsx|\.xls|\.csv|\.pdf|\.txt)$/i;
            if ((this.useFileAPI && file_node.files.length) || (!this.useFileAPI && $(file_node).val() !== '')) {
                if (this.useFileAPI) {
                    var file = file_node.files[0];
                    var filename = file.name;
                    var filename_limit = 40;
                    var extension = filename.substr(filename.lastIndexOf("."));
                    var isAllowed = allowedExtensionsRegx.test(extension);
                    if (file.size > security_update_max_upload_fsize) {
                        var msg = _t("The selected file exceed the maximum file size of %s.");
                        this.displayNotification({ title: _t("File upload"), message: _.str.sprintf(msg, utils.human_size(security_update_max_upload_fsize)), type: 'danger' });
                        return false;
                    }
                    if (!isAllowed) {
                        var msg = _t("Allowed file extensions are:\n.jpg\n.jpeg\n.png\n.xlsx\n.xls\n.csv\n.pdf\n.txt");
                        this.displayNotification({ title: _t("Invalid File Type"), message: msg, type: 'danger' });
                        return false;
                    }

                    if (file.name.length > filename_limit) {
                        var msg = _t("Exceed the maximum character limit of %s.");
                        this.displayNotification({ title: _t("Invalid File Name"), message: _.str.sprintf(msg,filename_limit), type: 'danger' });
                        return false;
                    }
                    utils.getDataURLFromFile(file).then(function (data) {
                        data = data.split(',')[1];
                        self.on_file_uploaded(file.size, file.name, file.type, data);
                    });
                } else {
                    this.$('form.o_form_binary_form').submit();
                }
                this.$('.o_form_binary_progress').show();
                this.$('button').hide();
            }
        },
    });
})