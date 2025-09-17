/** @odoo-module **/

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
const session = require('web.session');
import { _lt } from "@web/core/l10n/translation";

if (!await session.user_has_group('base.group_system')){
    ErrorDialog.bodyTemplate = "odoo_de_brand.ErrorDialogBody";
}
SessionExpiredDialog.title = _lt("Session Expired");
ErrorDialog.title = _lt("Error");
ClientErrorDialog.title = _lt("Client Error");
NetworkErrorDialog.title = _lt("Network Error");
SessionExpiredDialog.bodyTemplate = "odoo_de_brand.SessionExpiredDialogBody";

patch(RPCErrorDialog.prototype, "odoo_de_brand.ErrorDialog", {
    inferTitle() {
        this._super.apply(this, arguments);
        this.props.message = this.props.message.replace('Odoo','')
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
        this._super.apply(this, arguments);
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
        this._super.apply(this, arguments);
        const { data, subType } = this.props;
        this.title = capitalize(subType) || this.env._t("Warning");
    }
});

