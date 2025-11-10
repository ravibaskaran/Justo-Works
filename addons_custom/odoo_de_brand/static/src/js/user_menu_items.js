/** @odoo-module **/
// Migrated to Odoo 18 - 2025-11-10
// Fixed legacy imports:
// - Removed require('web.session') and require('web.rpc')
// - Updated patch syntax to remove _super calls
// - Using services properly in setup methods

import { UserMenu } from "@web/webclient/user_menu/user_menu";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { WebClient } from "@web/webclient/webclient";

const userMenuRegistry = registry.category("user_menuitems");

patch(UserMenu.prototype, "odoo_de_brand.UserMenu", {
    setup() {
        super.setup(...arguments);
        userMenuRegistry.remove("odoo_account");
        userMenuRegistry.remove("documentation");
        userMenuRegistry.remove("support");
    },
});

patch(WebClient.prototype, 'odoo_de_brand.WebClient', {
    setup() {
        super.setup(...arguments);

        const user = useService("user");
        const rpc = useService("rpc");
        const companyService = useService("company");

        // Get current company from service
        const currentCompany = companyService.currentCompany;
        if (currentCompany) {
            this.title.setParts({ zopenerp: currentCompany.name });
        } else {
            // Fallback: fetch company data via RPC
            const allowedCompanyIds = user.context.allowed_company_ids || [];
            if (allowedCompanyIds.length > 0) {
                rpc('/web/dataset/call_kw/res.company/search_read', {
                    model: 'res.company',
                    method: 'search_read',
                    args: [],
                    kwargs: {
                        fields: ['name', 'id'],
                        domain: [['id', 'in', allowedCompanyIds]],
                    }
                }).then((result) => {
                    if (result && result.length > 0) {
                        this.title.setParts({ zopenerp: result[0].name });
                    }
                });
            }
        }
    }
});
