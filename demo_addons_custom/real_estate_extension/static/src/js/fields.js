/** @odoo-module **/

/**
 * Binary Field File Upload Security Extension for Odoo 18
 * Adds file upload validation for size, type, and filename length
 */

import { BinaryField } from "@web/views/fields/binary/binary_field";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { humanSize } from "@web/core/utils/numbers";

// Default max upload file size (1MB)
let securityUpdateMaxUploadFsize = 1 * 1024 * 1024;

patch(BinaryField.prototype, {
    setup() {
        super.setup(...arguments);
        this.notification = useService("notification");
        this.rpc = useService("rpc");

        // Fetch max upload file size from configuration
        this.fetchMaxUploadSize();
    },

    /**
     * Fetch maximum upload file size from configuration
     */
    async fetchMaxUploadSize() {
        try {
            const result = await this.rpc("/web/dataset/call_kw", {
                model: 'ir.attachment',
                method: 'get_max_upload_fsize',
                args: ['security_update.max_upload_fsize'],
                kwargs: {},
            });

            if (result) {
                securityUpdateMaxUploadFsize = result;
            }
        } catch (error) {
            console.error("Error fetching max upload file size:", error);
        }
    },

    /**
     * Validate file before upload
     * Checks: file size, file type, filename length
     */
    async onFileChange(ev) {
        const file = ev.target.files[0];
        if (!file) {
            return super.onFileChange(ev);
        }

        // Allowed file extensions
        const allowedExtensionsRegx = /(\.jpg|\.jpeg|\.png|\.xlsx|\.xls|\.csv|\.pdf|\.txt)$/i;
        const filename = file.name;
        const filenameLimit = 40;
        const extension = filename.substr(filename.lastIndexOf("."));

        // Check file size
        if (file.size > securityUpdateMaxUploadFsize) {
            const msg = _t("The selected file exceed the maximum file size of %s.");
            this.notification.add(
                msg.replace('%s', humanSize(securityUpdateMaxUploadFsize)),
                {
                    title: _t("File upload"),
                    type: 'danger'
                }
            );
            ev.target.value = ''; // Clear the input
            return false;
        }

        // Check file extension
        if (!allowedExtensionsRegx.test(extension)) {
            const msg = _t("Allowed file extensions are:\n.jpg\n.jpeg\n.png\n.xlsx\n.xls\n.csv\n.pdf\n.txt");
            this.notification.add(msg, {
                title: _t("Invalid File Type"),
                type: 'danger'
            });
            ev.target.value = ''; // Clear the input
            return false;
        }

        // Check filename length
        if (filename.length > filenameLimit) {
            const msg = _t("Exceed the maximum character limit of %s.");
            this.notification.add(
                msg.replace('%s', filenameLimit.toString()),
                {
                    title: _t("Invalid File Name"),
                    type: 'danger'
                }
            );
            ev.target.value = ''; // Clear the input
            return false;
        }

        // All validations passed, proceed with upload
        return super.onFileChange(ev);
    }
});