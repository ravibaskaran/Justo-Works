/** @odoo-module **/

/**
 * Generate Button Widget for Real Estate Sheets
 * Toggle button for generating monthly data with validation
 */

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

export class ButtonGenerateWidget extends Component {
    static template = "real_estate_sheets.ButtonGenerateWidget";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.dialog = useService("dialog");
    }

    /**
     * Handle button click event
     */
    async onClicked(event) {
        event.stopPropagation();

        const record = this.props.record.data;
        const fieldName = this.props.name;

        // Special validation for commission generation
        if (fieldName === "commission_generate_button") {
            const retainerMonth = record.retainer_month;
            const forecastMonth = record.forecast_month;

            // Check if months are selected
            if (!retainerMonth || retainerMonth === 'false' ||
                !forecastMonth || forecastMonth === 'false') {
                this.dialog.add(AlertDialog, {
                    title: _t("Warning"),
                    body: _t("Please select No. of Months and No. of Months(Forecast)"),
                });
                return;
            }

            // Check if already generated
            if (record.sales_forecast_lines && record.sales_forecast_lines.count > 0) {
                this.dialog.add(ConfirmationDialog, {
                    title: _t("Confirmation"),
                    body: _t("Already generated, your changes will be discarded. Do you want to proceed?"),
                    confirm: () => this.toggleValue(),
                    confirmLabel: _t("Yes"),
                    cancel: () => {},
                    cancelLabel: _t("No"),
                });
                return;
            }
        }

        // Toggle the field value
        this.toggleValue();
    }

    /**
     * Toggle the boolean field value
     */
    toggleValue() {
        const currentValue = this.props.record.data[this.props.name];
        this.props.record.update({
            [this.props.name]: !currentValue
        });
    }

    /**
     * Get button label
     */
    get buttonLabel() {
        return _t("Generate Month");
    }
}

ButtonGenerateWidget.displayName = "Generate Button Toggle";

registry.category("fields").add("generate_button_toggle", ButtonGenerateWidget);
