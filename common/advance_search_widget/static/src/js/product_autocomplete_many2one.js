odoo.define('product.autocomplete.many2one', function (require) {
'use strict';

var FieldMany2One = require('web.relational_fields').FieldMany2One;
var core = require('web.core');
// var Autocomplete = require('partner.autocomplete.core');
var rpc = require('web.rpc');

var field_registry = require('web.field_registry');

var _t = core._t;


var ProductField = FieldMany2One.extend({


    /**
     * @override
     */
   init: function () {
       this._super.apply(this, arguments);
       this.limit = 10;
    //    console.log("attrs :",this.attrs);
    //    console.log("attrs :",this.name);
       this.autoCompleteFields = this.attrs.adv_fields;
       this.SearchFields = this.attrs.search_fields;
       this.focus_next = 'focus_next' in this.attrs ? JSON.parse(this.attrs.focus_next) : true;
//        console.log('this.focus_next',this.focus_next);
       // {'stock':'Stock','uom':'Unit','price':'Price','batch':'Batch'}
       // console.log(JSON.parse('{"stock":"Stock","uom":"Unit","price":"Price","batch":"Batch"}'));

   },


    /**
     * Modify autocomplete results rendering
     * Add logo in the autocomplete results if logo is provided
     *
     * @private
     */
    _modifyAutompleteRendering: function (){
        var api = this.$input.data('ui-autocomplete');

        // console.log('api :',api);
        // console.log('this.name :',this.name);

        // FIXME: bugfix to prevent traceback in mobile apps due to override
        // of Many2one widget with native implementation.
        if (!api) {
            return;
        }else{
//        console.log("api",api);

        }

        api._renderItem = function(ul, item){
            // var class_names = "" 
            ul.addClass(item.class_names);
            var li = "<li></li>"
//             console.log('item.lable :',item.label );

            if (item.is_header){
                var li = '<li class="adv_head_cls" ></li>'

            }
            var $name = $('<a/>')["html"](item.label);

            var $other_fields = ''

            if (item.other_fields){
                // console.log("stock");
               var $other_fields = item.other_fields;
            }

            if (item.logo){
                var $img = $('<img/>').attr('src', item.logo);
                $a.append($img);
            }

            return $(li)
                    .data("item.autocomplete",item)
                    .append($name,$other_fields)
                    .appendTo(ul)
                    .addClass(item.classname);


        };


    },

    /**
     * @override
     * @private
     */
    _renderEdit: function (){
        this._super.apply(this, arguments);
        this._modifyAutompleteRendering();
    },

    /**
     * Query Autocomplete and add results to the popup
     *
     * @override
     * @param search_val {string}
     * @returns {Deferred}
     * @private
     */

    _search: function (search_val) {
        // alert("search");
        var self = this;
        var def = new Promise(function (resolve, reject) {
            var context = self.record.getContext(self.recordParams);
            var domain = self.record.getDomain(self.recordParams);

            // Add the additionalContext
            _.extend(context, self.additionalContext);

            var blacklisted_ids = self._getSearchBlacklist();
            if (blacklisted_ids.length > 0) {
                domain.push(['id', 'not in', blacklisted_ids]);
            }
            // console.log('search_val :',search_val,'domain :',domain,'limit :',self.limit + 1,'context :',context);
            var autoCompleteFields_dict = self.autoCompleteFields;
            var SearchFields_dict = self.SearchFields;
            var field_name = self.name;

            // console.log('_modifyAutompleteRendering fields',autoCompleteFields_dict);
            self._rpc({
                // model: self.field.relation,
                // method: "name_search",
                model: "advance.search",
                method: "name_search_custom",

                kwargs: {
                    name: search_val,
                    field_name: field_name,
                    args: domain,
                    operator: "like",
                    model:self.field.relation,
                    limit: self.limit,
                    context: context,
                    adv_fields:autoCompleteFields_dict,
                    search_fields:SearchFields_dict,
                }}).then(function (result) {
                var values = _.map(result, function (x) {
                    // x[1] = self._getDisplayName(x[1]);
                    return {
                        label: _.str.escapeHTML(x[1].trim()) || data.noDisplayContent,
                        value: x[1],
                        name: x[1],
                        id: x[0],
                        class_names: x[2],
                        is_header: x[3],
                        other_fields:x[4],

                    };
                });

                // console.log('value',values);



                // search more... if more results than limit
//                console.log(values.length-1 , self.limit);
                if (values.length > self.limit) {
                    values = self._manageSearchMore(values, search_val, domain, context);
                }
                var create_enabled = self.can_create && !self.nodeOptions.no_create;
                // quick create
                var raw_result = _.map(result, function (x) { return x[1]; });
                if (create_enabled && !self.nodeOptions.no_quick_create &&
                    search_val.length > 0 && !_.contains(raw_result, search_val)) {
                    values.push({

                        label: _.str.sprintf(_t('Create "%s"'),
                            $('<span />').text(search_val).html()),
                        action: self._quickCreate.bind(self, search_val),
                        classname: 'o_m2o_dropdown_option'
                    });
                }
                // create and edit ...
                if (create_enabled && !self.nodeOptions.no_create_edit) {
                    var createAndEditAction = function () {
                        // Clear the value in case the user clicks on discard
                        self.$('input').val('');
                        return self._searchCreatePopup("form", false, self._createContext(search_val));
                    };
                    values.push({
                        label: _t("Create and Edit..."),
                        action: createAndEditAction,
                        classname: 'o_m2o_dropdown_option',
                    });
                } else if (values.length === 0) {
                    values.push({
                        label: _t("No results to show..."),
                        classname: 'advance_search_no_result'
                    });
                }

                resolve(values);
            });
        });
        this.orderer.add(def);
        return def;
    },

    /**
     * @private
     * @param {Object} values
     * @param {string} search_val
     * @param {Object} domain
     * @param {Object} context
     * @returns {Object}
     */
    _manageSearchMore: function (values, search_val, domain, context) {
        var self = this;
        values = values.slice(0, this.limit);
        values.push({
            label: _t("Search More..."),
            action: function () {
                var prom;
                if (search_val !== '') {
                    prom = self._rpc({
                        model: self.field.relation,
                        method: 'name_search',
                        kwargs: {
                            name: search_val,
                            args: domain,
                            operator: "ilike",
                            limit: self.SEARCH_MORE_LIMIT,
                            context: context,
                        },
                    });
                }
                Promise.resolve(prom).then(function (results) {
                    var dynamicFilters;
                    if (results) {
                        var ids = _.map(results, function (x) {
                            return x[0];
                        });
                        dynamicFilters = [{
                            description: _.str.sprintf(_t('Quick search: %s'), search_val),
                            domain: [['id', 'in', ids]],
                        }];
                    }
                    self._searchCreatePopup("search", false, {}, dynamicFilters);
                });
            },
            classname: 'o_m2o_dropdown_option',
        });
        return values;
    },


    /**
     * @private
     */
    _bindAutoComplete: function () {
        var self = this;
        var focus_next = self.focus_next;
        // avoid ignoring autocomplete="off" by obfuscating placeholder, see #30439
        if ($.browser.chrome && this.$input.attr('placeholder')) {
            this.$input.attr('placeholder', function (index, val) {
                return val.split('').join('\ufeff');
            });
        }
        this.$input.autocomplete({
            source: function (req, resp) {
                _.each(self._autocompleteSources, function (source) {
                    // Resets the results for this source
                    source.results = [];

                    // Check if this source should be used for the searched term
                    if (!source.validation || source.validation.call(self, req.term)) {
                        source.loading = true;

                        // Wrap the returned value of the source.method with a promise
                        // So event if the returned value is not async, it will work
                        Promise.resolve(source.method.call(self, req.term)).then(function (results) {
                            source.results = results;
                            source.loading = false;
                            resp(self._concatenateAutocompleteResults());
                        });
                    }
                });
            },
            select: function (event, ui) {
                console.log("item select ");
                // we do not want the select event to trigger any additional
                // effect, such as navigating to another field.
                if (focus_next == false){
                    event.stopImmediatePropagation();
                    event.preventDefault();
                }

                var item = ui.item;
                self.floating = false;
                if (item.id) {
                    self.reinitialize({id: item.id, display_name: item.name});
                } else if (item.action) {
                    item.action();
                }
                return false;
            },
            focus: function (event) {
                $('.adv_head_cls').removeClass('ui-menu-item');
                $('.adv_head_cls').children().each(function( index ) {
                    var width = $($('.adv_search_autocomplete_dropdown li:first-child').children()[index]).css('width');
                    $($('.adv_head_cls').children()[index]).css('display', 'inline-block')
                    $($('.adv_head_cls').children()[index]).css('width', width)
                })
                event.preventDefault(); // don't automatically select values on focus
            },
            open: function (event) {
                self._onScroll = function (ev) {
                    if (ev.target !== self.$input.get(0) && self.$input.hasClass('ui-autocomplete-input')) {
                        self.$input.autocomplete('close');
                    }
                };
                window.addEventListener('scroll', self._onScroll, true);
            },
            close: function (event) {
                // it is necessary to prevent ESC key from propagating to field
                // root, to prevent unwanted discard operations.
                if (event.which === $.ui.keyCode.ESCAPE) {
                    console.log("$.ui.keyCode.ESCAPE");
                    event.stopPropagation();
                }
                if (self._onScroll) {
                    window.removeEventListener('scroll', self._onScroll, true);
                }
            },
            autoFocus: true,
            html: true,
            minLength: 0,
            delay: this.AUTOCOMPLETE_DELAY,
        });
        this.$input.autocomplete("option", "position", { my : "left top", at: "left bottom" });
        this.autocomplete_bound = true;
    },
    /**
     * @private
     *
     * @param {OdooEvent} ev
     */
    _onInputKeyup: function (ev) {
        if (ev.which === $.ui.keyCode.ENTER || ev.which === $.ui.keyCode.TAB) {
            // If we pressed enter or tab, we want to prevent _onInputFocusout from
            // executing since it would open a M2O dialog to request
            // confirmation that the many2one is not properly set.
            // It's a case that is already handled by the autocomplete lib.
            return;
        }
        this.isDirty = true;
        if (this.$input.val() === "") {
            this.reinitialize(false);
        } else if (this._getDisplayName(this.m2o_value) !== this.$input.val()) {
            this.floating = true;
            this._updateExternalButton();
        }
    },

});



field_registry.add('advance_search_many2one', ProductField);

return ProductField;
});
