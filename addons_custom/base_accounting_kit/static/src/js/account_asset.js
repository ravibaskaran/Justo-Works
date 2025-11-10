/** @odoo-module **/

/**
 * Account Asset Depreciation Lines Toggler Widget for Odoo 18
 *
 * Shows a toggle button on depreciation and installment lines for posted/unposted status.
 * When clicked, calls the create_move method on account.asset.depreciation.line model.
 *
 * Note: This widget is specific to account.asset.depreciation.line model.
 */

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { _t } from "@web/core/l10n/translation";

export class AccountAssetWidget extends Component {
    static template = "base_accounting_kit.DeprecLinesToggler";
    static props = {
        ...standardFieldProps,
    };

    /**
     * Get button state based on record data
     */
    get buttonState() {
        const record = this.props.record.data;

        if (record.move_posted_check) {
            return {
                className: 'o_is_posted',
                title: _t('Posted'),
                disabled: true,
            };
        } else if (record.move_check) {
            return {
                className: 'o_unposted',
                title: _t('Accounting entries waiting for manual verification'),
                disabled: true,
            };
        } else {
            return {
                className: '',
                title: _t('Unposted'),
                disabled: false,
            };
        }
    }

    /**
     * Handle button click - trigger create_move action
     */
    onClick(event) {
        event.stopPropagation();

        if (!this.buttonState.disabled) {
            this.props.record.model.orm.call(
                this.props.record.resModel,
                'create_move',
                [[this.props.record.resId]],
                {}
            ).then(() => {
                // Reload the record to update the button state
                this.props.record.load();
            }).catch((error) => {
                console.error('Error creating move:', error);
            });
        }
    }
}

AccountAssetWidget.displayName = "Depreciation Lines Toggler";

registry.category("fields").add("deprec_lines_toggler", AccountAssetWidget);
