/** @odoo-module **/

/*
* File Upload Security Validation
* Migrated to Odoo 18 OWL - 2025-11-10
*
* Validates file uploads for:
* - File size (max 1MB configurable)
* - File type (jpg, jpeg, png, xlsx, xls, csv, pdf, txt)
* - Filename length (max 40 characters)
*/

import { patch } from "@web/core/utils/patch";
import { FileUploader } from "@web/views/fields/file_handler";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

// Default maximum file size: 1MB
let securityUpdateMaxUploadSize = 1 * 1024 * 1024;

// Allowed file extensions regex
const allowedExtensionsRegex = /(\.jpg|\.jpeg|\.png|\.xlsx|\.xls|\.csv|\.pdf|\.txt)$/i;

// Filename character limit
const FILENAME_LIMIT = 40;

// Patch FileUploader to add security validation
patch(FileUploader.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
        this.notification = useService("notification");

        // Load max file size from configuration
        this.loadMaxFileSize();
    },

    async loadMaxFileSize() {
        try {
            const result = await this.orm.call(
                'ir.attachment',
                'get_max_upload_fsize',
                ['security_update.max_upload_fsize']
            );
            if (result) {
                securityUpdateMaxUploadSize = result;
            }
        } catch (error) {
            console.warn('Could not load max file size config, using default:', error);
        }
    },

    async uploadFiles(files) {
        // Validate each file before upload
        for (const file of files) {
            const validation = this.validateFile(file);
            if (!validation.valid) {
                this.notification.add(validation.message, {
                    title: validation.title,
                    type: "danger",
                });
                return; // Stop upload if any file is invalid
            }
        }

        // All files valid, proceed with upload
        return super.uploadFiles(...arguments);
    },

    validateFile(file) {
        // Check file size
        if (file.size > securityUpdateMaxUploadSize) {
            return {
                valid: false,
                title: _t("File upload"),
                message: _t(
                    "The selected file exceeds the maximum file size of %s.",
                    this.humanFileSize(securityUpdateMaxUploadSize)
                ),
            };
        }

        // Check file extension
        const filename = file.name;
        const extension = filename.substr(filename.lastIndexOf("."));
        const isAllowed = allowedExtensionsRegex.test(extension);

        if (!isAllowed) {
            return {
                valid: false,
                title: _t("Invalid File Type"),
                message: _t(
                    "Allowed file extensions are:\n.jpg\n.jpeg\n.png\n.xlsx\n.xls\n.csv\n.pdf\n.txt"
                ),
            };
        }

        // Check filename length
        if (filename.length > FILENAME_LIMIT) {
            return {
                valid: false,
                title: _t("Invalid File Name"),
                message: _t(
                    "Filename exceeds the maximum character limit of %s.",
                    FILENAME_LIMIT
                ),
            };
        }

        return { valid: true };
    },

    humanFileSize(bytes) {
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        if (bytes === 0) return '0 Byte';
        const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
        return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
    },
});
