/** @odoo-module **/
/**
 * Migrated from Odoo 15 to Odoo 18 OWL - 2025-11-10
 * Changes:
 * - Converted odoo.define to @odoo-module
 * - Changed from include() to patch()
 * - Updated import paths for Odoo 18
 * - Converted RPC to use rpc service
 * - Updated Dialog to use dialog service
 * - Converted to proper OWL patterns
 */

import { Many2OneField } from "@web/views/fields/many2one/many2one_field";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

patch(Many2OneField.prototype, {
    setup() {
        super.setup(...arguments);
        this.rpc = useService("rpc");
        this.dialog = useService("dialog");
    },

    async onChange(value) {
        const result = await super.onChange?.(value);

        if (this.props.record.resModel === "budget.sheet" &&
            this.props.name === "project_id" &&
            value && value.id) {

            try {
                const evaluationId = await this.rpc("/web/dataset/call_kw", {
                    model: "budget.sheet",
                    method: "get_evaluation_id",
                    args: [[value.id]],
                    kwargs: {},
                });

                if (evaluationId) {
                    await new Promise((resolve, reject) => {
                        this.dialog.add(
                            {
                                title: _t("Confirmation"),
                                body: _t("Do you want to update data from evaluation sheet?"),
                                confirm: () => {
                                    // Update Project Info Only - default action
                                    resolve();
                                },
                                cancel: reject,
                            },
                            {
                                confirmLabel: _t("Update Project Info Only"),
                                cancelLabel: _t("No"),
                                customButtons: [
                                    {
                                        text: _t("Update All Data"),
                                        classes: "btn-primary",
                                        close: true,
                                        click: () => {
                                            $('input[name="evaluation_sheet"]').val('');
                                            $('input[name="evaluation_sheet"]').change();
                                            $('input[name="evaluation_sheet"]').val('update_all_from_evaluation');
                                            $('input[name="evaluation_sheet"]').change();
                                            resolve();
                                        },
                                    },
                                ],
                                onConfirm: () => {
                                    $('input[name="evaluation_sheet"]').val('');
                                    $('input[name="evaluation_sheet"]').change();
                                    $('input[name="evaluation_sheet"]').val(evaluationId);
                                    $('input[name="evaluation_sheet"]').change();
                                },
                            }
                        );
                    });
                }
            } catch (error) {
                console.error("Error fetching evaluation ID:", error);
            }
        }

        return result;
    },
});
