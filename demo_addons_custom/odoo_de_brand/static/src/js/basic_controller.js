/** @odoo-module **/

/**
 * Form Controller Extensions for Odoo 18
 * - Adds confirmation dialog when closing modified forms
 * - Disables auto-save on page unload
 */

import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        this.dialog = useService("dialog");
    },

    /**
     * Check if record can be removed
     * Shows confirmation dialog if record has unsaved changes
     */
    async canBeRemoved() {
        const model = this.model;

        // Check if form has unsaved changes
        if (model && model.root && model.root.isDirty) {
            return new Promise((resolve, reject) => {
                this.dialog.add(ConfirmationDialog, {
                    title: _t("Warning"),
                    body: _t("The record has been modified, your changes will be discarded. Do you want to proceed?"),
                    confirm: () => resolve(true),
                    confirmLabel: _t("Discard"),
                    cancel: () => reject(),
                    cancelLabel: _t("Stay"),
                });
            });
        }

        // No unsaved changes, allow removal
        return true;
    },

    /**
     * Prevent auto-save on page unload/reload
     * Override to disable _urgentSave behavior
     */
    beforeUnload(ev) {
        // Intentionally disable auto-save on page unload
        // Original Odoo behavior was to call _urgentSave(this.handle)
        // which could cause unwanted saves when user navigates away

        // If you want to add a browser warning for unsaved changes:
        // if (this.model?.root?.isDirty) {
        //     ev.preventDefault();
        //     ev.returnValue = '';
        //     return '';
        // }
    }
});

/*
 * MIGRATION NOTES:
 * ================
 *
 * Changes from Odoo 15:
 * - BasicController → FormController (more specific)
 * - Dialog.confirm → ConfirmationDialog service
 * - isDirty() → model.root.isDirty (property access)
 * - _onBeforeUnload → beforeUnload (method name change)
 * - _urgentSave commented out (prevents auto-save)
 *
 * Behavior:
 * - Shows confirmation when closing/navigating away from modified form
 * - Prevents automatic saving on page unload
 * - User must explicitly save or discard changes
 *
 * Testing:
 * - Modify a form and try to close/navigate away
 * - Verify confirmation dialog appears
 * - Verify changes are not auto-saved on page reload
 */