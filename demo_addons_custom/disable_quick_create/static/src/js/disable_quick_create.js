/** @odoo-module **/

import { Many2OneField } from "@web/views/fields/many2one/many2one_field";
import { patch } from "@web/core/utils/patch";

// Cache for models with quick create disabled
let modelsCache = [];
let modelsCachePromise = null;

/**
 * Patch Many2OneField to disable quick create functionality globally
 * and specifically for models with disable_create_edit flag
 */
patch(Many2OneField.prototype, {
    /**
     * Override get relation to disable quick create
     */
    get relation() {
        const relation = super.relation;

        // Always disable quick create for all Many2One fields
        if (this.props.record && this.props.record.fieldNames) {
            // Set no_quick_create option to true
            if (!this.props.noQuickCreate) {
                // Force disable quick create
                return {
                    ...relation,
                    noQuickCreate: true,
                };
            }
        }

        return relation;
    },

    /**
     * Setup method to initialize field options
     */
    setup() {
        super.setup(...arguments);

        // Ensure no_quick_create is always enabled
        if (this.props.record && this.props.record.resModel) {
            // Additional logic can be added here if needed
            // to check against specific models from ir.model
        }
    },
});
