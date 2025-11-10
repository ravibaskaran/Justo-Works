/** @odoo-module **/

/**
 * De-brand User Menu for Odoo 18
 * Removes Odoo-specific menu items and replaces browser title with company name
 */

import { UserMenu } from "@web/webclient/user_menu/user_menu";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
import { WebClient } from "@web/webclient/webclient";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";

const userMenuRegistry = registry.category("user_menuitems");

// Remove Odoo branding menu items
patch(UserMenu.prototype, {
    setup() {
        super.setup(...arguments);

        // Remove Odoo-specific menu items
        userMenuRegistry.remove("odoo_account");
        userMenuRegistry.remove("documentation");
        userMenuRegistry.remove("support");
    },
});

// Replace browser title with company name
patch(WebClient.prototype, {
    setup() {
        super.setup(...arguments);
        this.rpc = useService("rpc");

        // Set browser title to company name
        this.updateBrowserTitle();
    },

    /**
     * Update browser title with current company name
     */
    async updateBrowserTitle() {
        try {
            const companyIds = session.user_context.allowed_company_ids;

            if (companyIds && companyIds.length > 0) {
                const companies = await this.rpc("/web/dataset/call_kw", {
                    model: 'res.company',
                    method: 'search_read',
                    args: [
                        [['id', 'in', companyIds]]
                    ],
                    kwargs: {
                        fields: ['name', 'id'],
                    },
                });

                if (companies && companies.length > 0) {
                    this.title.setParts({ zopenerp: companies[0].name });
                } else {
                    this.title.setParts({ zopenerp: "" });
                }
            }
        } catch (error) {
            console.error("Error updating browser title:", error);
            this.title.setParts({ zopenerp: "" });
        }
    }
});