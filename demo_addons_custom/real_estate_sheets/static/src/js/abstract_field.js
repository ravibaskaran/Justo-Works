/** @odoo-module **/

/**
 * Abstract Field Extension for Real Estate Sheets
 * Adds TAB key handling for evaluation and budget sheet lines
 */

import { Field } from "@web/views/fields/field";
import { patch } from "@web/core/utils/patch";

patch(Field.prototype, {
    /**
     * Handle keydown events, specifically TAB key for sheet lines
     */
    onKeydown(ev) {
        super.onKeydown?.(ev);

        // Handle TAB key for evaluation and budget sheet lines
        if (ev.key === 'Tab') {
            const record = this.props.record;

            if (record && ['evaluation.sheet.line', 'budget.sheet.line'].includes(record.resModel)) {
                if (this.props.name === 'others') {
                    // Set tab identifier for line tracking
                    const tabIdentifier = document.querySelector('[name="tab_identifier"]');
                    if (tabIdentifier && record.data.line_identifier) {
                        tabIdentifier.value = record.data.line_identifier;
                    }
                }
            }
        }
    }
});