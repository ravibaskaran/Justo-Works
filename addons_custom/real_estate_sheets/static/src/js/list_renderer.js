/** @odoo-module **/
/**
 * Migrated from Odoo 15 to Odoo 18 OWL - 2025-11-10
 * Changes:
 * - Converted odoo.define to @odoo-module
 * - Changed from include() to patch()
 * - Updated import paths for Odoo 18
 * - Converted jQuery event handlers to OWL patterns
 * - Updated field formatting to use modern utilities
 * - Preserved all custom logic for header rendering and aggregate cells
 */

import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { formatFloat, formatMonetary } from "@web/views/fields/formatters";
import { onMounted, onPatched, useRef } from "@odoo/owl";

patch(ListRenderer.prototype, {
    setup() {
        super.setup(...arguments);
        this.rootRef = useRef("root");

        onMounted(() => {
            this._setupEventHandlers();
        });

        onPatched(() => {
            this._setupEventHandlers();
        });
    },

    _setupEventHandlers() {
        if (!this.rootRef.el) return;

        // Setup focus handler for site_head_man_power inputs
        const inputs = this.rootRef.el.querySelectorAll('input.site_head_man_power');
        inputs.forEach(input => {
            input.addEventListener('focusin', this._onSiteHeadFocus.bind(this));
        });
    },

    _onSiteHeadFocus(ev) {
        const tabIdentifier = document.querySelector('[name="tab_identifier"]');
        if (tabIdentifier) {
            tabIdentifier.dispatchEvent(new Event('change'));

            const target = ev.target;
            const focusOutHandler = () => {
                if (tabIdentifier.value === 'copied') {
                    target.click();
                    tabIdentifier.value = '';
                    tabIdentifier.dispatchEvent(new Event('change'));
                }
                target.removeEventListener('focusout', focusOutHandler);
            };

            target.addEventListener('focusout', focusOutHandler);
        }
    },

    /**
     * Override to customize header cell rendering for cost columns
     */
    getHeaderCellTitle(column) {
        const title = super.getHeaderCellTitle(column);

        // Check if this is a cost column
        if (column.name && column.name.includes('cost_col_')) {
            const costSheetHeader = document.querySelector('.cost_sheet_header');
            if (costSheetHeader) {
                const values = costSheetHeader.textContent.split('~');
                const fieldName = column.name;
                const index = parseInt(fieldName[fieldName.length - 1]) - 1;
                if (values[index]) {
                    return values[index];
                }
            }
        }

        return title;
    },

    /**
     * Override to customize aggregate cell rendering
     */
    getAggregateValue(column) {
        const aggregateValues = this.props.list.aggregates || {};

        if (!aggregateValues[column.name]) {
            // Handle custom text attribute
            if (column.attrs && column.attrs.text) {
                return column.attrs.text;
            }
            return super.getAggregateValue?.(column) || '';
        }

        const field = this.props.list.fields[column.name];
        const aggregateData = aggregateValues[column.name];
        const value = aggregateData.value;

        // Format the value based on field type and widget
        let formattedValue;
        if (column.widget === 'monetary' || field.type === 'monetary') {
            formattedValue = formatMonetary(value, {
                field: field,
                digits: column.digits,
            });
        } else if (field.type === 'float') {
            formattedValue = formatFloat(value, {
                field: field,
                digits: column.digits,
            });
        } else {
            formattedValue = super.getAggregateValue?.(column) || value;
        }

        return formattedValue;
    },
});
