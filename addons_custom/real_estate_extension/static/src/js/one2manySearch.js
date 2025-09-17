odoo.define('rp_search_one2many_v13.search_section_and_note_backend', function (require) {
    "use strict";

    var SectionAndNoteListRenderer = require('account.section_and_note_backend')

    SectionAndNoteListRenderer.include({
        events: _.extend({
            'keyup .oe_search_input': '_onKeyUp',
            'change .search_select_one2many': '_onKeyUp'
        }, SectionAndNoteListRenderer.prototype.events),

        /**
         * We want to add .o_section_and_note_list_view on the table to have stronger CSS.
         *
         * @override
         * @private
         */
        _renderView: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$('.o_list_table').addClass('o_section_and_note_list_view');
                if (self.arch.tag == 'tree' && self.$el.hasClass('o_list_view') && self.arch.attrs.search_by_fields == '1') {
                    var search = '<input type="text" class="oe_search_input pl-2 mb-1 oe_edit_only" placeholder="Search...">';
                    var row_count = '<span class="oe_row_count oe_edit_only">Total Row: '+ self.state.data.length+'</span>';
                    self.$el.find('table').addClass('oe_table_search');
                    var search_fields = `
                        <select class='search_select_one2many oe_edit_only'
                            style="width: 10%;
                            float: left;
                            height: 30px;
                            border-top-left-radius: 10px;
                            border-bottom-left-radius: 10px;
                            border: 1px solid rgb(204, 204, 204);
                            padding-left: 3px;">
                    `
                    var table_th = self.$el.find('table thead tr th:not(.o_list_record_remove_header)')
                    $(table_th).each(function(i, th){
                    console.log(th, 'th', i)
                        search_fields += '<option value="' + $(th).attr('data-name') + '">' + ($(th).attr('title') || $(th).text()) + '</option>'
                    })
                    search_fields += '</option>'

                    var $search = $(search).css('border', '1px solid #ccc')
                    .css('width', '50%')
                    .css('border-radius', '10px')
                    .css('height', '30px')
                    .css('float', 'left')
                    .css('border-top-left-radius', '0')
                    .css('border-bottom-left-radius', '0')
                    var $row_count = $(row_count).css('float', 'right')
                    .css('margin-top', '4px')
                    .css('color', '#666666');

                    self.$el.prepend($search);
                    self.$el.prepend(search_fields);
                    self.$el.prepend($row_count);
                }
            });
        },

        /**
         * @private
         * @param {keyEvent} event
         */
        _onKeyUp: function (event) {
            if($('.oe_search_input').length > 0){
                var value = $('.oe_search_input').val().toLowerCase();
                var count_row = 0;
                var $el = $(this.$el)
                var td_to_search = $('.search_select_one2many').val()
                $(".oe_table_search tr.o_data_row:not(tfoot tr)").filter(function() {
                    $(this).toggle($(this).find('[name="' + td_to_search + '"]').text().toLowerCase().indexOf(value) > -1)
                    count_row = $(this).text().toLowerCase().indexOf(value) > -1 ? count_row+1 : count_row
                });
                $el.find('.oe_row_count').text('')
                $el.find('.oe_row_count').text('Total Row: ' + count_row)
            }
        },

        confirmUpdate: function (state, id, fields, ev) {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
            self._onKeyUp()
            })
        },
    });
});
