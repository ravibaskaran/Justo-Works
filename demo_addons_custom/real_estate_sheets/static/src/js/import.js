/** @odoo-module alias=real_estate_sheets.ListController **/

import ListController from 'web.ListController';

ListController.include({
    events: _.extend({}, ListController.prototype.events, {
        'click .import_competition_sheet': 'onClickCompetitionSheetImport',
    }),

    onClickCompetitionSheetImport: function(ev) {
        this.do_action({
            name: 'Import',
            type: 'ir.actions.act_window',
            res_model: 'competition.sheet.import',
            target: 'new',
            views: [[false, 'form']],
        })
    },

    renderButtons: function ($node) {
        this._super.apply(this, arguments);
        if(this.modelName && this.modelName == 'competition.sheet'){
            this.$buttons.append($(`
                <button type="object" class="btn btn-primary import_competition_sheet">
                    Import
                </button>
            `))
        }
    },
})