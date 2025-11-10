/** @odoo-module **/

/**
 * View File Toggle Field for Odoo 18
 * Displays an eye button to preview attached files in a modal
 */

import { Component, onMounted, useState, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks";

export class ViewFileToggleField extends Component {
    static template = "real_estate_sheets.ViewFileToggleField";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            hasAttachment: false,
            isModalOpen: false,
            fileContent: "",
        });

        onMounted(() => {
            this.checkAttachment();
        });
    }

    /**
     * Check if the record has an attachment
     */
    async checkAttachment() {
        try {
            const result = await this.rpc("/get_attachment_file_url", {
                line_id: this.props.record.resId,
                model: this.props.record.resModel,
            });

            if (result) {
                this.state.hasAttachment = true;
            }
        } catch (error) {
            console.error("Error checking attachment:", error);
        }
    }

    /**
     * Handle view button click
     */
    async onClickView(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        try {
            const result = await this.rpc("/get_attachment_file_url", {
                line_id: this.props.record.resId,
                model: this.props.record.resModel,
            });

            if (result) {
                this.state.fileContent = result;
                this.state.isModalOpen = true;
            }
        } catch (error) {
            console.error("Error fetching attachment:", error);
        }
    }

    /**
     * Close the modal
     */
    onClickClose() {
        this.state.isModalOpen = false;
        this.state.fileContent = "";
    }
}

ViewFileToggleField.displayName = "View File Toggle";

registry.category("fields").add("view_file_toggle", ViewFileToggleField);
