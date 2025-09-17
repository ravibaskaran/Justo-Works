/** @odoo-module **/

import { UserMenu } from "@web/webclient/user_menu/user_menu";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
const userMenuRegistry = registry.category("user_menuitems");
var session = require('web.session');
var rpc = require('web.rpc');
import { WebClient } from "@web/webclient/webclient";

patch(UserMenu.prototype, "odoo_de_brand.UserMenu", {
    setup() {
        this._super.apply(this, arguments);
        userMenuRegistry.remove("odoo_account");
        userMenuRegistry.remove("documentation");
        userMenuRegistry.remove("support");
    },
});

patch(WebClient.prototype, 'odoo_de_brand.WebClient', {
    setup() {
        this._super.apply(this, arguments);
        var self = this;
        var domain = session.user_context.allowed_company_ids;
        self.title.setParts({ zopenerp: "" });
        rpc.query({
            fields: ['name','id',],
            domain: [['id', 'in', domain]],
            model: 'res.company',
            method: 'search_read',
        }).then(function (result) {
            self.title.setParts({ zopenerp: result[0].name });
        });
    }
});