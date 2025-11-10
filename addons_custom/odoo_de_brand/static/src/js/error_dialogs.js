/** @odoo-module **/
// Migrated to Odoo 18 - 2025-11-10
// Fixed legacy imports and patterns:
// - Removed require('web.session')
// - Removed invalid top-level await for user_has_group check
// - Updated patch syntax to use super.method() instead of _super.apply()
// - User group check moved to runtime where it can be properly handled

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
import { _lt } from "@web/core/l10n/translation";

// Note: User group check for ErrorDialog.bodyTemplate would need to be done
// in a proper async context (e.g., in a service or component setup).
// For now, we'll apply the de-branding for all users.
// If you need conditional behavior based on user groups, implement it in
// the component that displays the error dialog.

ErrorDialog.bodyTemplate = "odoo_de_brand.ErrorDialogBody";
SessionExpiredDialog.title = _lt("Session Expired");
ErrorDialog.title = _lt("Error");
ClientErrorDialog.title = _lt("Client Error");
NetworkErrorDialog.title = _lt("Network Error");
SessionExpiredDialog.bodyTemplate = "odoo_de_brand.SessionExpiredDialogBody";

patch(RPCErrorDialog.prototype, "odoo_de_brand.ErrorDialog", {
    inferTitle() {
        super.inferTitle(...arguments);
        this.props.message = this.props.message.replace('Odoo','');
        if (this.props.exceptionName && odooExceptionTitleMap.has(this.props.exceptionName)) {
            this.title = odooExceptionTitleMap.get(this.props.exceptionName).toString();
            return;
        }
        // Fall back to a name based on the error type.
        if (!this.props.type) return;
        switch (this.props.type) {
            case "server":
                this.title = this.env._t("Server Error");
                break;
            case "script":
                this.title = this.env._t("Client Error");
                break;
            case "network":
                this.title = this.env._t("Network Error");
                break;
        }
    },
});

patch(WarningDialog.prototype, "odoo_de_brand.WarningDialog", {
    setup() {
        super.setup(...arguments);
        this.title = this.env._t("Warning");
        this.inferTitle();
        const { data, message } = this.props;
        if (data && data.arguments && data.arguments.length > 0) {
            this.message = data.arguments[0];
        } else {
            this.message = message;
        }
    }
});

patch(RedirectWarningDialog.prototype, "odoo_de_brand.RedirectWarningDialog", {
    setup() {
        super.setup(...arguments);
        const { data, subType } = this.props;
        this.title = capitalize(subType) || this.env._t("Warning");
    }
});
