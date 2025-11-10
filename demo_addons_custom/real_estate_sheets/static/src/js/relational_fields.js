/** @odoo-module **/

/**
 * Relational Fields Extension for Real Estate Sheets
 * Adds evaluation sheet update dialog for budget.sheet project changes
 */

import { Many2OneField } from "@web/views/fields/many2one/many2one_field";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(Many2OneField.prototype, {
    setup() {
        super.setup(...arguments);
        this.rpc = useService("rpc");
        this.dialog = useService("dialog");
    },

    /**
     * Handle field value changes
     */
    async onChange(value) {
        const result = await super.onChange(value);

        // Handle project_id changes on budget.sheet
        if (this.props.record.resModel === "budget.sheet" && this.props.name === "project_id") {
            if (value && value[0]) {
                const projectId = value[0];

                try {
                    const evalId = await this.rpc("/web/dataset/call_kw", {
                        model: "budget.sheet",
                        method: "get_evaluation_id",
                        args: [projectId],
                        kwargs: {},
                    });

                    if (evalId) {
                        this.showEvaluationUpdateDialog(evalId);
                    }
                } catch (error) {
                    console.error("Error fetching evaluation ID:", error);
                }
            }
        }

        return result;
    },

    /**
     * Show confirmation dialog for evaluation sheet update
     */
    showEvaluationUpdateDialog(evalId) {
        this.dialog.add(ConfirmationDialog, {
            title: _t("Confirmation"),
            body: _t("Do you want to update data from evaluation sheet?"),
            confirm: () => this.updateEvaluationSheet(evalId, false),
            confirmLabel: _t("Update Project Info Only"),
            cancel: () => {}, // Do nothing on cancel
            cancelLabel: _t("No"),
            // Add custom button for "Update All Data"
            extraButtons: [{
                text: _t("Update All Data"),
                classes: "btn-secondary",
                close: true,
                click: () => this.updateEvaluationSheet('update_all_from_evaluation', true),
            }],
        });
    },

    /**
     * Update evaluation sheet field
     */
    updateEvaluationSheet(value, isUpdateAll) {
        const record = this.props.record;

        // Trigger evaluation_sheet field update
        if (record.fields.evaluation_sheet) {
            record.update({
                evaluation_sheet: isUpdateAll ? 'update_all_from_evaluation' : value
            });
        }
    }
});