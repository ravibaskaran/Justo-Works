/** @odoo-module **/
/**
 * Migrated from Odoo 15 to Odoo 18 OWL - 2025-11-10
 * Changes:
 * - Converted odoo.define to @odoo-module
 * - Converted AbstractField.extend to OWL Component class
 * - Updated Dialog to use dialog service
 * - Converted events to OWL event handlers
 * - Updated to use standardFieldProps
 * - Converted _setValue to props.record.update
 * - Registered with registry.category("fields")
 */

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { _t } from "@web/core/l10n/translation";

export class ButtonGenerateWidget extends Component {
    static template = "real_estate_sheets.ButtonGenerateWidget";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.dialog = useService("dialog");
    }

    get isCommissionButton() {
        return this.props.name === "commission_generate_button";
    }

    async onClick(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        if (this.isCommissionButton) {
            // Validate required fields
            const retainerMonth = document.querySelector('select[name="retainer_month"]');
            const forecastMonth = document.querySelector('select[name="forecast_month"]');

            if (retainerMonth?.value === 'false' || forecastMonth?.value === 'false') {
                await this.dialog.add(
                    {
                        title: _t("Warning"),
                        body: _t("Please select No. of Months and No. of Months(Forecast)"),
                    }
                );
                return;
            }

            // Check if already generated
            const recordData = this.props.record.data;
            if (recordData.sales_forecast_lines && recordData.sales_forecast_lines.count > 0) {
                const confirmed = await new Promise((resolve) => {
                    this.dialog.add(
                        {
                            title: _t("Confirmation"),
                            body: _t("Already generated, your changes will be discarded. Do you want to proceed?"),
                            confirm: () => resolve(true),
                            cancel: () => resolve(false),
                        },
                        {
                            confirmLabel: _t("Yes"),
                            cancelLabel: _t("No"),
                        }
                    );
                });

                if (!confirmed) {
                    return;
                }
            }
        }

        // Toggle the value
        const newValue = !this.props.record.data[this.props.name];
        await this.props.record.update({ [this.props.name]: newValue });
    }
}

ButtonGenerateWidget.template = "real_estate_sheets.ButtonGenerateWidget";

// Register the component in the fields registry
registry.category("fields").add("generate_button_toggle", ButtonGenerateWidget);
