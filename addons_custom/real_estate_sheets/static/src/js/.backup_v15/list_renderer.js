odoo.define('real_estate_sheets.list_renderer', function(require) {
"use strict";

    var ListRenderer = require("web.ListRenderer");
    var config = require("web.config");
    var field_utils = require("web.field_utils");

    ListRenderer.include({
        events: _.extend({}, ListRenderer.prototype.events, {
            'focusin input.site_head_man_power': '_onSiteHeadFocus',
        }),

        _renderHeaderCell: function (node) {
            var res = this._super(node);
            if(res[0].dataset.name.includes('cost_col_')){
                var field_name = res[0].dataset.name
                var values = $('.cost_sheet_header').text().split('~');
                $(res).text(values[parseInt(field_name[field_name.length-1])-1])
            }
            return res
        },

        _onSiteHeadFocus: function(ev){
            $('[name="tab_identifier"]').change()
            $(ev.target).focusout(function(){
                if($('[name="tab_identifier"]').val() == 'copied'){
                    $(ev.target).click()
                    $('[name="tab_identifier"]').val('')
                    $('[name="tab_identifier"]').change()
                }
            })
        },

        _renderAggregateCells: function (aggregateValues) {
            var self = this;

            return _.map(this.columns, function (column) {
                var $cell = $('<td>');
                if (config.isDebug()) {
                    $cell.addClass(column.attrs.name);
                }
                if (column.attrs.editOnly) {
                    $cell.addClass('oe_edit_only');
                }
                if (column.attrs.readOnly) {
                    $cell.addClass('oe_read_only');
                }
                if(column.attrs.text) {
                    $cell.text(column.attrs.text);
                }


                if (column.attrs.name in aggregateValues) {
                    var field = self.state.fields[column.attrs.name];
                    var value = aggregateValues[column.attrs.name].value;
                    var help = aggregateValues[column.attrs.name].help;
                    var formatFunc = field_utils.format[column.attrs.widget];
                    if (!formatFunc) {
                        formatFunc = field_utils.format[field.type];
                    }
                    var formattedValue = formatFunc(value, field, {
                        escape: true,
                        digits: column.attrs.digits ? JSON.parse(column.attrs.digits) : undefined,
                    });
                    $cell.addClass('o_list_number').attr('title', help).html(formattedValue);
                }


//                if(["evaluation.sheet.line","budget.sheet.line"].includes(self.state.model) && column.attrs.name == 'total_revenue'){
//                    if($('span.balance_amount_profit_loss').length > 0){
//                        if(column.aggregate){
//                        console.log($('span.balance_amount_profit_loss'),column.aggregate.value,parseFloat($('span.balance_amount_profit_loss').text()),'fjfjfj')
//                            var sum_revenue = parseFloat(column.aggregate.value) + parseFloat($('span.balance_amount_profit_loss').text().replace(',',''))
//                            $cell.text(sum_revenue.toFixed(2))
//                        }
//                    }
//                }
                return $cell;
            });
        },
    });
})