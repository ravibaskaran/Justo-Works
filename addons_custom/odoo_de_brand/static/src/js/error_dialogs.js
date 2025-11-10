/** @odoo-module **/

/**
 * Error Dialog De-branding for Odoo 18
 * Removes Odoo branding from error messages and dialog titles
 */

import { RPCErrorDialog } from "@web/core/errors/error_dialogs";
import { odooExceptionTitleMap } from "@web/core/errors/error_dialogs";
import { WarningDialog } from "@web/core/errors/error_dialogs";
import { RedirectWarningDialog } from "@web/core/errors/error_dialogs";
import { ErrorDialog } from "@web/core/errors/error_dialogs";
import { SessionExpiredDialog } from "@web/core/errors/error_dialogs";
import { ClientErrorDialog } from "@web/core/errors/error_dialogs";
import { NetworkErrorDialog } from "@web/core/errors/error_dialogs";
import { patch } from "@web/core/utils/patch";
import { capitalize } from "@web/core/utils/strings";
import { session } from "@web/session";
import { _t, _lt } from "@web/core/l10n/translation";

// De-brand dialog titles
SessionExpiredDialog.title = _lt("Session Expired");
ErrorDialog.title = _lt("Error");
ClientErrorDialog.title = _lt("Client Error");
NetworkErrorDialog.title = _lt("Network Error");
SessionExpiredDialog.bodyTemplate = "odoo_de_brand.SessionExpiredDialogBody";

// Conditionally set error dialog body template for non-system users
// Note: In Odoo 18, we cannot use top-level await, so we set this statically
// If you need conditional logic, it should be done inside the component setup
ErrorDialog.bodyTemplate = "odoo_de_brand.ErrorDialogBody";

// Patch RPC Error Dialog to remove "Odoo" branding from messages
patch(RPCErrorDialog.prototype, {
    inferTitle() {
        super.inferTitle(...arguments);

        // Remove "Odoo" branding from error messages
        if (this.props.message) {
            this.props.message = this.props.message.replace(/Odoo/g, '');
        }

        // Use custom exception titles if available
        if (this.props.exceptionName && odooExceptionTitleMap.has(this.props.exceptionName)) {
            this.title = odooExceptionTitleMap.get(this.props.exceptionName).toString();
            return;
        }

        // Fall back to type-based titles
        if (!this.props.type) return;

        switch (this.props.type) {
            case "server":
                this.title = _t("Server Error");
                break;
            case "script":
                this.title = _t("Client Error");
                break;
            case "network":
                this.title = _t("Network Error");
                break;
        }
    },
});

// Patch Warning Dialog for consistent title handling
patch(WarningDialog.prototype, {
    setup() {
        super.setup(...arguments);
        this.title = _t("Warning");
        this.inferTitle();

        // Extract message from data if available
        const { data, message } = this.props;
        if (data && data.arguments && data.arguments.length > 0) {
            this.message = data.arguments[0];
        } else {
            this.message = message;
        }
    }
});

// Patch Redirect Warning Dialog for consistent title handling
patch(RedirectWarningDialog.prototype, {
    setup() {
        super.setup(...arguments);
        const { data, subType } = this.props;
        this.title = capitalize(subType) || _t("Warning");
    }
});

/*
 * MIGRATION NOTES:
 * ================
 *
 * This module removes Odoo branding from error dialogs and messages.
 *
 * Changes from original:
 * - Removed top-level await (not supported in ES modules)
 * - Changed require('web.session') → import { session }
 * - Use _t() from @web/core/l10n/translation
 * - Updated super method calls to use super.method() syntax
 *
 * Templates Required:
 * - odoo_de_brand.ErrorDialogBody
 * - odoo_de_brand.SessionExpiredDialogBody
 *
 * These templates should be defined in XML files to customize
 * the error dialog appearance without Odoo branding.
 */
