/** @odoo-module **/

/**
 * Competition Sheet List Controller Extension
 * Adds Import button for competition.sheet model
 */

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(ListController.prototype, {
    setup() {
        super.setup(...arguments);
        this.action = useService("action");
    },

    /**
     * Handle Import button click
     */
    onClickCompetitionSheetImport(ev) {
        this.action.doAction({
            name: 'Import',
            type: 'ir.actions.act_window',
            res_model: 'competition.sheet.import',
            target: 'new',
            views: [[false, 'form']],
        });
    },

    /**
     * Get action menu items with custom Import button
     */
    get actionMenuItems() {
        const menuItems = super.actionMenuItems;

        // Add Import button for competition.sheet model
        if (this.props.resModel === 'competition.sheet') {
            return {
                ...menuItems,
                other: [
                    ...(menuItems.other || []),
                    {
                        key: 'import_competition_sheet',
                        description: 'Import',
                        callback: () => this.onClickCompetitionSheetImport(),
                    }
                ]
            };
        }

        return menuItems;
    }
});