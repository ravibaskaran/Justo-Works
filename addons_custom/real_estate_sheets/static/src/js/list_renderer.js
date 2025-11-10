/** @odoo-module **/

/**
 * List Renderer Extension for Real Estate Sheets
 * Customizes list view rendering for evaluation and budget sheets
 *
 * Handles:
 * - Dynamic cost column headers from cost_sheet_header element
 * - Site head man power focus/focusout behavior with tab identifier
 * - Custom aggregate cell rendering with text attributes
 */

import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";
import { onMounted } from "@odoo/owl";

patch(ListRenderer.prototype, {
    setup() {
        super.setup(...arguments);

        // Setup event listeners after mounting
        onMounted(() => {
            this.setupCustomEventListeners();
        });
    },

    /**
     * Setup custom event listeners for site head man power inputs
     */
    setupCustomEventListeners() {
        const inputs = this.el?.querySelectorAll('input.site_head_man_power');
        if (inputs) {
            inputs.forEach(input => {
                input.addEventListener('focusin', this.onSiteHeadFocus.bind(this));
            });
        }
    },

    /**
     * Handle focus on site head man power input
     * Manages tab identifier for copy/paste functionality
     */
    onSiteHeadFocus(ev) {
        const tabIdentifier = document.querySelector('[name="tab_identifier"]');
        if (!tabIdentifier) return;

        // Trigger change event
        tabIdentifier.dispatchEvent(new Event('change'));

        // Set up focus out handler
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
    },

    /**
     * Render header cell with dynamic cost column handling
     *
     * NOTE: In Odoo 18, header rendering may need to be done via templates
     * This is a compatibility shim that may need adjustment based on actual
     * Odoo 18 list view implementation.
     */
    getHeaderCellContent(column) {
        // Get default content
        let content = super.getHeaderCellContent?.(column);

        // Handle cost_col_ fields
        if (column.name && column.name.includes('cost_col_')) {
            const costHeader = document.querySelector('.cost_sheet_header');
            if (costHeader) {
                const values = costHeader.textContent.split('~');
                const columnIndex = parseInt(column.name[column.name.length - 1]) - 1;
                if (values[columnIndex]) {
                    return values[columnIndex];
                }
            }
        }

        return content;
    },

    /**
     * Get aggregate cell content with custom text
     *
     * NOTE: Odoo 18 may handle aggregates differently.
     * This method may need adjustment based on the actual API.
     */
    getAggregateValue(column) {
        const value = super.getAggregateValue?.(column);

        // Add custom text from column attributes if available
        if (column.attrs && column.attrs.text) {
            return column.attrs.text;
        }

        return value;
    }
});

/*
 * MIGRATION NOTES:
 * ================
 *
 * This file requires testing and potential refinement because:
 *
 * 1. List view rendering in Odoo 18 may use different methods/APIs
 * 2. Header and aggregate rendering might be template-based now
 * 3. Event handling may need to be done via OWL directives instead of jQuery
 * 4. The original _renderAggregateCells created DOM elements with jQuery -
 *    This needs to be adapted to OWL's reactive rendering
 *
 * Testing Checklist:
 * - [ ] Cost column headers display correctly from cost_sheet_header
 * - [ ] Site head man power focus/focusout behavior works
 * - [ ] Tab identifier is set correctly for copy operations
 * - [ ] Aggregate cells show custom text when specified
 * - [ ] No console errors related to list rendering
 *
 * If issues occur, consider:
 * - Creating a custom list view controller instead of patching
 * - Using OWL templates for custom rendering
 * - Implementing via field components rather than renderer patches
 */
