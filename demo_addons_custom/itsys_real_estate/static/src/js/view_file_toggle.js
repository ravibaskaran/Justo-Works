odoo.define('real_estate_sheets.view_file_toggle', function(require) {
"use strict";

    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var registry = require('web.field_registry');
    var rpc = require('web.rpc');
    var _t = core._t;
    var Dialog = require('web.Dialog');
    const ajax = require('web.ajax');
    let modal_window = `
        <div id="viewFileToggleModal" class="attachment_modal_file_toggle">
          <span class="view_file_toggle_close" onclick="$('#viewFileToggleModal').remove()">&times;</span>
          <div class="attachment_content_file_toggle" id="img_area_file_toggle"/>
        </div>
    `

    var ViewFileToggle = AbstractField.extend({
        events: _.extend({}, AbstractField.prototype.events, {
            'click': '_onClickView',
            'click .view_file_toggle_close': '_onClickClose',
        }),
        description: "",

        isSet: function () {
            return true;
        },

        _render: function () {
            var $button = $('<button/>', {
                type: 'button',
            }).addClass('btn fa fa-eye o_view_file_toggle p-0 p-0');
            ajax.jsonRpc('/get_attachment_file_url', 'call', {'line_id': this.recordData.id, 'model': this.model}).then((result) => {
                if(result){
                    this.$el.html($button);
                }
            })
        },

        _onClickClose: function(ev) {
            $('#viewFileToggleModal').css('display', 'none')
        },

        _onClickView: function (event) {
            ajax.jsonRpc('/get_attachment_file_url', 'call', {'line_id': this.recordData.id, 'model': this.model}).then((result) => {
                if(result && $('.o_cp_action_menus').length == 0){
                    $(".o_form_view").append(modal_window);
                    $("#viewFileToggleModal").modal({
                        keyboard: false,
                    });
                    $('#img_area_file_toggle').empty()
                    $('#img_area_file_toggle').append(result)
                }
            });
        },
    });

    registry.add("view_file_toggle", ViewFileToggle);
});
