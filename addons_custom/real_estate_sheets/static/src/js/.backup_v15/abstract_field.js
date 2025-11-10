odoo.define('real_estate_sheets.abstract_fields', function (require) {
"use strict";
    var abstract_fields = require('web.AbstractField');

    abstract_fields.include({
        _onKeydown: function (ev) {
            var self = this;
            this._super.apply(this, arguments);
            switch (ev.which) {
                case $.ui.keyCode.TAB:
                    if(['evaluation.sheet.line', 'budget.sheet.line'].includes(this.model) && this.name == 'others'){
                        $('[name="tab_identifier"]').val(this.recordData.line_identifier)
                    }
                    break;
            }
        }
    })
})