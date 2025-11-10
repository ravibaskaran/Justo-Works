/** @odoo-module **/
/**
 * Migrated from Odoo 15 to Odoo 18 OWL - 2025-11-10
 * Changes:
 * - Converted odoo.define to @odoo-module
 * - Changed from include() to patch()
 * - Updated import paths for Odoo 18
 */

import { patch } from "@web/core/utils/patch";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component } from "@odoo/owl";

// Patch all field components to add custom TAB key handler
patch(Component.prototype, {
    _onKeydown(ev) {
        super._onKeydown?.(ev);

        switch (ev.which) {
            case $.ui.keyCode.TAB:
                if (this.props.record && this.props.record.resModel &&
                    ['evaluation.sheet.line', 'budget.sheet.line'].includes(this.props.record.resModel) &&
                    this.props.name === 'others') {
                    const recordData = this.props.record.data;
                    if (recordData.line_identifier) {
                        $('[name="tab_identifier"]').val(recordData.line_identifier);
                    }
                }
                break;
        }
    }
});
