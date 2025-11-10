/** @odoo-module **/
// Migrated to Odoo 18 OWL - 2025-11-10
// Original: Odoo 15 BasicController/FormController extension
// Changes:
// - odoo.define → @odoo-module
// - BasicController.include → patch on FormController
// - Dialog.confirm → confirmation dialog service
// - Updated to use OWL framework patterns
//
// Purpose: Prevent form auto-save on close and show confirmation dialog
// when navigating away with unsaved changes

import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

patch(FormController.prototype, "odoo_de_brand.FormController", {

    /**
     * Override canBeRemoved to show confirmation dialog when form has unsaved changes
     */
    async canBeRemoved() {
        if (this.model.root.isDirty) {
            return new Promise((resolve, reject) => {
                this.dialogService.add(ConfirmationDialog, {
                    title: _t("Warning"),
                    body: _t("The record has been modified, your changes will be discarded. Do you want to proceed?"),
                    confirm: () => resolve(true),
                    cancel: () => reject(),
                });
            });
        } else {
            // If no changes, proceed normally
            return super.canBeRemoved(...arguments);
        }
    },

    /**
     * Override beforeUnload to prevent auto-save on browser close/reload
     * This is intentionally left empty to disable the urgent save behavior
     */
    beforeUnload(ev) {
        // Intentionally empty - prevents auto-save on window close/reload
        // The original implementation called this._urgentSave(this.handle)
        // which we want to prevent according to the module requirements

        // If there are unsaved changes, browser will show native confirmation
        if (this.model.root.isDirty) {
            ev.preventDefault();
            ev.returnValue = '';
        }
    },
});
