/** @odoo-module **/

/*
* Migrated to Odoo 18 OWL - 2025-11-10
*/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks";

export class ViewFileToggleField extends Component {
    static template = "itsys_real_estate.ViewFileToggleField";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            hasAttachment: false,
            showModal: false,
            fileContent: ""
        });

        // Check if file exists
        this.checkAttachment();
    }

    async checkAttachment() {
        try {
            const result = await this.rpc("/get_attachment_file_url", {
                line_id: this.props.record.resId,
                model: this.props.record.resModel
            });

            if (result) {
                this.state.hasAttachment = true;
            }
        } catch (error) {
            console.error("Error checking attachment:", error);
        }
    }

    async onClickView(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        try {
            const result = await this.rpc("/get_attachment_file_url", {
                line_id: this.props.record.resId,
                model: this.props.record.resModel
            });

            if (result) {
                this.state.fileContent = result;
                this.state.showModal = true;
            }
        } catch (error) {
            console.error("Error loading attachment:", error);
        }
    }

    onClickClose(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        this.state.showModal = false;
        this.state.fileContent = "";
    }
}

// Register the field widget
registry.category("fields").add("view_file_toggle", ViewFileToggleField);
