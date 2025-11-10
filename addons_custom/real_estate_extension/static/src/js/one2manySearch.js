/** @odoo-module **/

/*
* One2Many Search Widget
* Migrated to Odoo 18 OWL - 2025-11-10
*
* Adds search functionality to one2many list views:
* - Search input field
* - Field selector dropdown
* - Row count display
* - Live filtering
*/

import { patch } from "@web/core/utils/patch";
import { ListRenderer } from "@web/views/list/list_renderer";

patch(ListRenderer.prototype, {
    /**
     * Override _renderView to add search functionality
     * @override
     */
    async _renderView() {
        await super._renderView(...arguments);

        // Only add search if attribute is set in view
        const searchEnabled = this.props.archInfo?.search_by_fields === '1';

        if (searchEnabled && this.el && this.el.classList.contains('o_list_view')) {
            this._addSearchWidget();
        }
    },

    /**
     * Add search widget to the list view
     */
    _addSearchWidget() {
        const table = this.el.querySelector('table');
        if (!table) return;

        // Add CSS class for styling
        table.classList.add('oe_table_search');

        // Create search elements
        const searchContainer = document.createElement('div');
        searchContainer.className = 'o_one2many_search_container';
        searchContainer.style.cssText = 'display: flex; margin-bottom: 10px; align-items: center;';

        // Row count display
        const rowCount = document.createElement('span');
        rowCount.className = 'oe_row_count oe_edit_only';
        rowCount.style.cssText = 'margin-left: auto; margin-top: 4px; color: #666666;';
        rowCount.textContent = `Total Rows: ${this.props.list.records.length}`;

        // Field selector dropdown
        const selectField = document.createElement('select');
        selectField.className = 'search_select_one2many oe_edit_only';
        selectField.style.cssText = `
            width: 200px;
            height: 30px;
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
            border: 1px solid #ccc;
            padding-left: 3px;
        `;

        // Populate field options from table headers
        const headers = table.querySelectorAll('thead tr th:not(.o_list_record_remove_header)');
        headers.forEach(th => {
            const fieldName = th.dataset.name;
            const fieldLabel = th.getAttribute('title') || th.textContent.trim();
            if (fieldName) {
                const option = document.createElement('option');
                option.value = fieldName;
                option.textContent = fieldLabel;
                selectField.appendChild(option);
            }
        });

        // Search input
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.className = 'oe_search_input oe_edit_only';
        searchInput.placeholder = 'Search...';
        searchInput.style.cssText = `
            width: 300px;
            height: 30px;
            border: 1px solid #ccc;
            border-radius: 10px;
            border-top-left-radius: 0;
            border-bottom-left-radius: 0;
            padding-left: 8px;
            margin-left: -1px;
        `;

        // Add event listeners
        searchInput.addEventListener('keyup', () => this._filterRows(searchInput, selectField, rowCount));
        selectField.addEventListener('change', () => this._filterRows(searchInput, selectField, rowCount));

        // Assemble search widget
        searchContainer.appendChild(rowCount);
        searchContainer.appendChild(selectField);
        searchContainer.appendChild(searchInput);

        // Insert before table
        table.parentNode.insertBefore(searchContainer, table);

        // Store references for later use
        this._searchInput = searchInput;
        this._selectField = selectField;
        this._rowCount = rowCount;
    },

    /**
     * Filter table rows based on search input
     */
    _filterRows(searchInput, selectField, rowCount) {
        if (!searchInput || !selectField) return;

        const searchValue = searchInput.value.toLowerCase();
        const selectedField = selectField.value;
        const table = this.el.querySelector('.oe_table_search');

        if (!table) return;

        const rows = table.querySelectorAll('tr.o_data_row:not(tfoot tr)');
        let visibleCount = 0;

        rows.forEach(row => {
            const fieldCell = row.querySelector(`[name="${selectedField}"]`);
            if (fieldCell) {
                const cellText = fieldCell.textContent.toLowerCase();
                const matches = cellText.indexOf(searchValue) > -1;

                row.style.display = matches ? '' : 'none';
                if (matches) visibleCount++;
            }
        });

        // Update row count
        if (rowCount) {
            rowCount.textContent = `Total Rows: ${visibleCount}`;
        }
    },

    /**
     * Re-apply search filter after record updates
     * @override
     */
    async onRecordSaved() {
        await super.onRecordSaved(...arguments);

        // Re-apply filter if search is active
        if (this._searchInput && this._selectField && this._rowCount) {
            setTimeout(() => {
                this._filterRows(this._searchInput, this._selectField, this._rowCount);
            }, 100);
        }
    },
});
