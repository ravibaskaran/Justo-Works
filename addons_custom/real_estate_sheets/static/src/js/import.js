/** @odoo-module **/
/**
 * Migrated from Odoo 15 to Odoo 18 OWL - 2025-11-10
 * Changes:
 * - Updated from include() to patch()
 * - Changed imports to Odoo 18 paths
 * - Updated do_action to use action service
 * - Converted to proper OWL Component patterns
 */

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";

patch(ListController.prototype, {

    setup() {
        super.setup(...arguments);
        this.actionService = this.env.services.action;
    },

    onClickCompetitionSheetImport(ev) {
        this.actionService.doAction({
            name: 'Import',
            type: 'ir.actions.act_window',
            res_model: 'competition.sheet.import',
            target: 'new',
            views: [[false, 'form']],
        });
    },

    getStaticButton() {
        const buttons = super.getStaticButton ? super.getStaticButton() : [];

        if (this.props.resModel === 'competition.sheet') {
            buttons.push({
                type: 'button',
                className: 'btn btn-primary import_competition_sheet',
                text: 'Import',
                onClick: () => this.onClickCompetitionSheetImport(),
            });
        }

        return buttons;
    },
});
