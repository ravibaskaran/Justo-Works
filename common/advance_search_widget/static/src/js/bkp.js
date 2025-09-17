odoo.define('product.autocomplete.many2one', function (require) {
    'use strict';
    
    var FieldMany2One = require('web.relational_fields').FieldMany2One;
    var core = require('web.core');
    // var Autocomplete = require('partner.autocomplete.core');
    var rpc = require('web.rpc');
    var field_registry = require('web.field_registry');
    
    var _t = core._t;
    console.log('product.autocomplete.many2one');
    var ProductField = FieldMany2One.extend({
    //    jsLibs: [
    //        '/partner_autocomplete/static/lib/jsvat.js'
    //    ],
    
        /**
         * @override
         */
       init: function () {
           this._super.apply(this, arguments);
           this.limit = 10;
           this.autoCompleteFields = {'stock':'Stock','uom':'Unit','price':'Price','batch':'Batch'}
       },
    
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
    
        /**
         * Action : create popup form with pre-filled values from Autocomplete
         *
         * @param {Object} company
         * @returns {Deferred}
         * @private
         */
    //    _createPartner: function (company) {
    //        var self = this;
    //        self.$('input').val('');
    //
    //        return Autocomplete.getCreateData(company).then(function (data){
    //            var context = {
    //                'default_is_company': true
    //            };
    //            _.each(data.company, function (val, key) {
    //                context['default_' + key] = val && val.id ? val.id : val;
    //            });
    //
    //            // if(data.company.street_name && !data.company.street_number) context.default_street_number = '';
    //            if (data.logo) context.default_image = data.logo;
    //
    //            return self._searchCreatePopup("form", false, context);
    //        });
    //    },
    
        /**
         * Returns the display_name from a string which contains it but was altered
         * as a result of the show_vat option.
         * Note that the split is done on a 'figuredash', not a standard dash.
         *
         * @private
         * @param {string} value
         * @returns {string} display_name without TaxID
         */
        // _getDisplayNameWithoutVAT: function (value) {
        //     return value.split(' ‒ ')[0];
        // },
    
        /**
         * Modify autocomplete results rendering
         * Add logo in the autocomplete results if logo is provided
         *
         * @private
         */
        _modifyAutompleteRendering: function (){
            var api = this.$input.data('ui-autocomplete');
    
    
    
            // FIXME: bugfix to prevent traceback in mobile apps due to override
            // of Many2one widget with native implementation.
            if (!api) {
                return;
            }
    
    
            api._renderItem = function(ul, item){
    
            //    rpc.query({
            //         model: 'product.product',
            //         method:'get_product_data',
            //         args: [item.id],
            //         }).then(function(result){
            //             item.qty=result
    //                    console.log("QTY",item.qty)
    
    // 
                    // });
                    //    console.log("QTY2",item.classname,);
    
    
                    ul.addClass('o_product_autocomplete_dropdown');
    
                console.log('_modifyAutompleteRendering fields',this.autoCompleteFields);
    
                    var $name = $('<a/>')["html"](item.label);
                   var $qty = $('<a/>')["html"](item.stock);
                   var $uom = $('<a/>')["html"](item.uom);
                   var $price = $('<a/>')["html"](item.price);
                   var $batch = $('<a/>')["html"](item.batch);
                //    var $table = "<table style='border:1px solid black'><tr><td>"+item.label+"</td><td>Stock</td><td>Batch</td></tr></table>"
    
                //    $a.append($b);
                //    $a.append($c);
    
    
                    if (item.logo){
                        var $img = $('<img/>').attr('src', item.logo);
                        $a.append($img);
                    }
    
                    return $("<li></li>")
                    .data("item.autocomplete",item)
                    .append($name,$qty,$uom,$price,$batch)
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
        // _searchSuggestions: function (search_val) {
        //     var def = $.Deferred();
    
        //     if (Autocomplete.isOnline()) {
        //         var self = this;
    
        //         Autocomplete.autocomplete(search_val).then(function (suggestions) {
        //             var choices = [];
        //             if (suggestions && suggestions.length) {
        //                 _.each(suggestions, function (suggestion) {
        //                     var label = '<i class="fa fa-magic text-muted"/> ';
        //                     label += _.str.sprintf('%s, <span class="text-muted">%s</span>', suggestion.label, suggestion.description);
    
        //                     choices.push({
        //                         label: label,
        //                         action: function () {
        //                             self._createPartner(suggestion);
        //                         },
        //                         logo: suggestion.logo,
        //                         classname: 'o_partner_autocomplete_dropdown_item',
        //                     });
        //                 });
        //             }
    
        //             def.resolve(choices);
        //         });
        //     } else {
        //         def.resolve([]);
        //     }
    
        //     return def;
        // },
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
                console.log('search_val :',search_val,'domain :',domain,'limit :',self.limit + 1,'context :',context);
                self._rpc({
                    // model: self.field.relation,
                    // method: "name_search",
                    model: "product.product",
                    method: "name_search_custom",
                    
                    kwargs: {
                        name: search_val,
                        args: domain,
                        operator: "like",
                        limit: self.limit + 1,
                        context: context,
                    }}).then(function (result) {
                    // possible selections for the m2o
                    console.log('result :',result);
                    // console.log('result :',values);
                    // alert('pause here !');
                    var values = _.map(result, function (x) {
                        // x[1] = self._getDisplayName(x[1]);
                        return {
                            label: _.str.escapeHTML(x[1].trim()) || data.noDisplayContent,
                            value: x[1],
                            name: x[1],
                            id: x[0],
                            stock:x[2],
                            uom:x[3],
                            price:x[4],
                            batch:x[5],
                        };
                    });
    
                    // search more... if more results than limit
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
                        });
                    }
    
                    resolve(values);
                });
            });
            this.orderer.add(def);
            return def;
        },
    });
    
    
    
    
    
    
    field_registry.add('product_many2one', ProductField);
    
    return ProductField;
    });

29-04-2022

odoo.define('product.autocomplete.many2one', function (require) {
'use strict';

var FieldMany2One = require('web.relational_fields').FieldMany2One;
var core = require('web.core');
// var Autocomplete = require('partner.autocomplete.core');
var rpc = require('web.rpc');
var field_registry = require('web.field_registry');

var _t = core._t;
// console.log('product.autocomplete.many2one');
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
    //    console.log('this.name',this.name);
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
        }

        api._renderItem = function(ul, item){
            // var class_names = ""
            ul.addClass(item.class_names);
            var li = "<li></li>"
             console.log('item.lable :',item.label );

            if (item.label == "Name"){
                var li = '<li class="ui-state-disabled"></li>'
                console.log("li",li);
            }
            var $name = $('<a/>')["html"](item.label);
            if (item.active){
//                var li = '<li class="ui-state-focus"></li>'
               var $name = $('<a class="ui-state-active" />')["html"](item.label);
                console.log("item.active",item.active);
            }
            // console.log("item",item);
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
                    limit: self.limit + 1,
                    context: context,
                    adv_fields:autoCompleteFields_dict,
                }}).then(function (result) {
                // possible selections for the m2o
                // console.log('result :',result);
                // console.log('result :',values);
                // alert('pause here !');
                var values = _.map(result, function (x) {
                    // x[1] = self._getDisplayName(x[1]);
                    return {
                        label: _.str.escapeHTML(x[1].trim()) || data.noDisplayContent,
                        value: x[1],
                        name: x[1],
                        id: x[0],
                        class_names: x[2],
                        active: x[3],
                        other_fields:x[4],

                    };
                });

                // console.log('value',values);



                // search more... if more results than limit
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
                    });
                }

                resolve(values);
            });
        });
        this.orderer.add(def);
        return def;
    },
});

field_registry.add('advance_search_many2one', ProductField);

return ProductField;
});




    