/** @odoo-module **/

/**
 * One2Many Search Extension for Odoo 18
 * Adds search and filter functionality to One2Many list views
 * with section and note support
 */

import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";
import { onMounted, onPatched } from "@odoo/owl";

patch(ListRenderer.prototype, {
    setup() {
        super.setup(...arguments);

        onMounted(() => {
            this.addSearchFunctionality();
        });

        onPatched(() => {
            this.addSearchFunctionality();
        });
    },

    /**
     * Add search input and filter functionality to list view
     */
    addSearchFunctionality() {
        const props = this.props;

        // Check if search_by_fields is enabled in arch
        if (!props.archInfo?.search_by_fields || props.archInfo.search_by_fields !== '1') {
            return;
        }

        const el = this.el;
        if (!el) return;

        // Add CSS class for section and note views
        const table = el.querySelector('.o_list_table');
        if (table) {
            table.classList.add('o_section_and_note_list_view');
            table.classList.add('oe_table_search');
        }

        // Check if search elements already exist
        if (el.querySelector('.oe_search_input')) {
            return;
        }

        // Get table headers for field selection
        const headers = el.querySelectorAll('table thead tr th:not(.o_list_record_remove_header)');
        if (headers.length === 0) return;

        // Build field select options
        let fieldOptions = '';
        headers.forEach(th => {
            const fieldName = th.dataset.name;
            const fieldLabel = th.getAttribute('title') || th.textContent.trim();
            if (fieldName) {
                fieldOptions += `<option value="${fieldName}">${fieldLabel}</option>`;
            }
        });

        // Create search elements
        const searchHTML = `
            <div class="oe_search_container oe_edit_only" style="margin-bottom: 8px; display: flex; align-items: center;">
                <span class="oe_row_count" style="margin-right: auto; color: #666;">
                    Total Row: ${this.props.list?.records?.length || 0}
                </span>
                <select class="search_select_one2many" style="
                    width: 150px;
                    height: 30px;
                    border-top-left-radius: 10px;
                    border-bottom-left-radius: 10px;
                    border: 1px solid #ccc;
                    padding-left: 8px;
                    margin-right: -1px;">
                    ${fieldOptions}
                </select>
                <input type="text" class="oe_search_input" placeholder="Search..." style="
                    width: 300px;
                    height: 30px;
                    border: 1px solid #ccc;
                    border-top-right-radius: 10px;
                    border-bottom-right-radius: 10px;
                    padding: 0 12px;">
            </div>
        `;

        // Insert search elements before the table
        if (table && !el.querySelector('.oe_search_container')) {
            table.insertAdjacentHTML('beforebegin', searchHTML);

            // Add event listeners
            const searchInput = el.querySelector('.oe_search_input');
            const searchSelect = el.querySelector('.search_select_one2many');

            if (searchInput) {
                searchInput.addEventListener('keyup', () => this.filterRows());
            }
            if (searchSelect) {
                searchSelect.addEventListener('change', () => this.filterRows());
            }
        }
    },

    /**
     * Filter table rows based on search input
     */
    filterRows() {
        const el = this.el;
        if (!el) return;

        const searchInput = el.querySelector('.oe_search_input');
        const searchSelect = el.querySelector('.search_select_one2many');
        const rowCount = el.querySelector('.oe_row_count');

        if (!searchInput || !searchSelect) return;

        const searchValue = searchInput.value.toLowerCase();
        const fieldToSearch = searchSelect.value;
        const rows = el.querySelectorAll('.oe_table_search tr.o_data_row:not(tfoot tr)');

        let visibleCount = 0;

        rows.forEach(row => {
            const cell = row.querySelector(`[name="${fieldToSearch}"]`);
            const cellText = cell ? cell.textContent.toLowerCase() : '';
            const matches = cellText.indexOf(searchValue) > -1;

            row.style.display = matches ? '' : 'none';
            if (matches) visibleCount++;
        });

        // Update row count
        if (rowCount) {
            rowCount.textContent = `Total Row: ${visibleCount}`;
        }
    }
});

/*
 * MIGRATION NOTES:
 * ================
 *
 * This module adds search functionality to One2Many list views when
 * the attribute search_by_fields="1" is set in the tree view definition.
 *
 * Changes from Odoo 15:
 * - Removed dependency on account.section_and_note_backend (may not exist in v18)
 * - Patches ListRenderer instead of SectionAndNoteListRenderer
 * - Uses OWL lifecycle hooks (onMounted, onPatched)
 * - Vanilla JavaScript instead of jQuery for DOM manipulation
 * - Search elements created with template literals and insertAdjacentHTML
 * - Event listeners use native addEventListener
 *
 * Testing:
 * - Add search_by_fields="1" to tree view XML
 * - Check that search input and field selector appear
 * - Verify filtering works correctly on selected field
 * - Check row count updates properly
 */
