/** @odoo-module **/

import { Component, useState, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

/**
 * Accounting Dashboard Component for Odoo 18
 * Migrated from Odoo 15 JavaScript to OWL framework
 * Compatible with Chart.js v4.x
 */
class AccountDashboard extends Component {
    static template = "base_accounting_kit.Invoicedashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            currency: null,
            posted: false,
            selectedAgedReceivable: 'this_month',
            selectedAgedPayable: 'this_month',
            selectedTop10Customer: 'this_month',
        });

        // Chart references
        this.incomeExpenseChartRef = useRef("canvas");
        this.agedPayableChartRef = useRef("canvas1");
        this.agedReceivableChartRef = useRef("horizontalbarChart");

        // Store chart instances
        this.charts = {
            incomeExpense: null,
            agedPayable: null,
            agedReceivable: null,
        };

        onMounted(async () => {
            await this.loadInitialData();
        });

        onWillUnmount(() => {
            this.destroyAllCharts();
        });
    }

    /**
     * Destroy all chart instances
     */
    destroyAllCharts() {
        Object.keys(this.charts).forEach(key => {
            if (this.charts[key]) {
                this.charts[key].destroy();
                this.charts[key] = null;
            }
        });
    }

    /**
     * Load initial dashboard data
     */
    async loadInitialData() {
        try {
            // Get currency
            this.state.currency = await this.orm.call(
                "account.move",
                "get_currency",
                []
            );

            // Load initial income/expense chart
            await this.loadIncomeThisMonth();

            // Load aged payable/receivable
            await this.loadAgedPayable('this_month');
            await this.loadAgedReceivable('this_month');

            // Load invoice data
            await this.loadInvoiceDataCurrentMonth();

            // Load other dashboard widgets
            await this.loadOverdues();
            await this.loadTop10Customers('this_month');
            await this.loadBankBalance();
            await this.loadLateBills();
            await this.loadUnreconciledItems();
            await this.loadIncomeExpenseData();
            await this.loadProfitData();

        } catch (error) {
            console.error("Error loading dashboard data:", error);
        }
    }

    /**
     * Format currency value
     */
    formatCurrency(amount) {
        if (typeof amount !== 'number') {
            amount = parseFloat(amount);
        }

        const currency = this.state.currency;
        if (!currency) return amount;

        const formatted = parseInt(amount).toLocaleString(currency.language, {
            minimumFractionDigits: 2
        });

        if (currency.position === "after") {
            return formatted + ' ' + currency.symbol;
        } else {
            return currency.symbol + ' ' + formatted;
        }
    }

    /**
     * Create/Update Income/Expense Chart (Chart.js v4)
     */
    createIncomeExpenseChart(data) {
        const ctx = this.incomeExpenseChartRef.el?.getContext('2d');
        if (!ctx) return;

        // Destroy existing chart
        if (this.charts.incomeExpense) {
            this.charts.incomeExpense.destroy();
        }

        // Chart.js v4 configuration
        this.charts.incomeExpense = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Income',
                        data: data.income,
                        backgroundColor: '#66aecf',
                        borderColor: '#66aecf',
                        borderWidth: 1,
                        type: 'bar'
                    },
                    {
                        label: 'Expense',
                        data: data.expense,
                        backgroundColor: '#6993d6',
                        borderColor: '#6993d6',
                        borderWidth: 1,
                        type: 'bar'
                    },
                    {
                        label: 'Profit/Loss',
                        data: data.profit,
                        backgroundColor: '#0bd465',
                        borderColor: '#0bd465',
                        borderWidth: 2,
                        type: 'line',
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                    },
                    tooltip: {
                        enabled: true,
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    /**
     * Create/Update Doughnut Chart for Aged Payable (Chart.js v4)
     */
    createAgedPayableChart(data) {
        const ctx = this.agedPayableChartRef.el?.getContext('2d');
        if (!ctx) return;

        if (this.charts.agedPayable) {
            this.charts.agedPayable.destroy();
        }

        const colors = [
            '#66aecf', '#6993d6', '#666fcf', '#7c66cf', '#9c66cf',
            '#bc66cf', '#b75fcc', '#cb5fbf', '#cc5f7f', '#cc6260',
            '#cc815f', '#cca15f', '#ccc25f', '#b9cf66', '#99cf66',
            '#75cb5f', '#60cc6c', '#804D8000', '#80B33300', '#80CC80CC',
            '#f2552c', '#00cccc', '#1f2e2e', '#993333', '#00cca3',
            '#1a1a00', '#3399ff', '#8066664D', '#80991AFF', '#808E666FF',
            '#804DB3FF', '#801AB399', '#80E666B3', '#8033991A', '#80CC9999',
            '#80B3B31A', '#8000E680', '#804D8066', '#80809980', '#80E6FF80',
            '#801AFF33', '#80999933', '#80FF3380', '#80CCCC00', '#8066E64D',
            '#804D80CC', '#809900B3', '#80E64D66', '#804DB380', '#80FF4D4D',
            '#8099E6E6', '#806666FF'
        ];

        this.charts.agedPayable = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.due_partner,
                datasets: [{
                    data: data.due_amount,
                    backgroundColor: colors,
                    hoverBackgroundColor: colors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    },
                    tooltip: {
                        enabled: true,
                    }
                }
            }
        });
    }

    /**
     * Create/Update Doughnut Chart for Aged Receivable (Chart.js v4)
     */
    createAgedReceivableChart(data) {
        const ctx = this.agedReceivableChartRef.el?.getContext('2d');
        if (!ctx) return;

        if (this.charts.agedReceivable) {
            this.charts.agedReceivable.destroy();
        }

        const colors = [
            '#66aecf', '#6993d6', '#666fcf', '#7c66cf', '#9c66cf',
            '#bc66cf', '#b75fcc', '#cb5fbf', '#cc5f7f', '#cc6260',
            '#cc815f', '#cca15f', '#ccc25f', '#b9cf66', '#99cf66',
            '#75cb5f', '#60cc6c', '#804D8000', '#80B33300', '#80CC80CC',
            '#f2552c', '#00cccc', '#1f2e2e', '#993333', '#00cca3',
            '#1a1a00', '#3399ff', '#8066664D', '#80991AFF', '#808E666FF',
            '#804DB3FF', '#801AB399', '#80E666B3', '#8033991A', '#80CC9999',
            '#80B3B31A', '#8000E680', '#804D8066', '#80809980', '#80E6FF80',
            '#801AFF33', '#80999933', '#80FF3380', '#80CCCC00', '#8066E64D',
            '#804D80CC', '#809900B3', '#80E64D66', '#804DB380', '#80FF4D4D',
            '#8099E6E6', '#806666FF'
        ];

        this.charts.agedReceivable = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.bill_partner,
                datasets: [{
                    data: data.bill_amount,
                    backgroundColor: colors,
                    hoverBackgroundColor: colors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    },
                    tooltip: {
                        enabled: true,
                    }
                }
            }
        });
    }

    /**
     * Event Handlers
     */

    async onClickIncomeThisMonth(ev) {
        ev.preventDefault();
        await this.loadIncomeThisMonth();
    }

    async onClickIncomeThisYear(ev) {
        ev.preventDefault();
        await this.loadIncomeThisYear();
    }

    async onClickIncomeLastMonth(ev) {
        ev.preventDefault();
        await this.loadIncomeLastMonth();
    }

    async onClickIncomeLastYear(ev) {
        ev.preventDefault();
        await this.loadIncomeLastYear();
    }

    async onClickInvoiceThisMonth(ev) {
        ev.preventDefault();
        await this.loadInvoiceDataCurrentMonth();
    }

    async onClickInvoiceThisYear(ev) {
        ev.preventDefault();
        await this.loadInvoiceDataCurrentYear();
    }

    async onTogglePosted(ev) {
        this.state.posted = ev.target.checked ? "posted" : false;
        await this.refreshAllData();
    }

    async onChangeAgedReceivable(ev) {
        const value = ev.target.value;
        this.state.selectedAgedReceivable = value;
        await this.loadAgedPayable(value);
    }

    async onChangeAgedPayable(ev) {
        const value = ev.target.value;
        this.state.selectedAgedPayable = value;
        await this.loadAgedReceivable(value);
    }

    async onChangeTop10Customer(ev) {
        const value = ev.target.value;
        this.state.selectedTop10Customer = value;
        await this.loadTop10Customers(value);
    }

    /**
     * Data Loading Methods
     */

    async loadIncomeThisMonth() {
        const result = await this.orm.call(
            'account.move',
            'get_income_this_month',
            [this.state.posted]
        );

        this.createIncomeExpenseChart({
            labels: result.date,
            income: result.income,
            expense: result.expense,
            profit: result.profit
        });
    }

    async loadIncomeThisYear() {
        const result = await this.orm.call(
            'account.move',
            'get_income_this_year',
            [this.state.posted]
        );

        this.createIncomeExpenseChart({
            labels: result.month,
            income: result.income,
            expense: result.expense,
            profit: result.profit
        });
    }

    async loadIncomeLastMonth() {
        const result = await this.orm.call(
            'account.move',
            'get_income_last_month',
            [this.state.posted]
        );

        this.createIncomeExpenseChart({
            labels: result.date,
            income: result.income,
            expense: result.expense,
            profit: result.profit
        });
    }

    async loadIncomeLastYear() {
        const result = await this.orm.call(
            'account.move',
            'get_income_last_year',
            [this.state.posted]
        );

        this.createIncomeExpenseChart({
            labels: result.month,
            income: result.income,
            expense: result.expense,
            profit: result.profit
        });
    }

    async loadAgedPayable(period) {
        const result = await this.orm.call(
            'account.move',
            'get_overdues_this_month_and_year',
            [this.state.posted, period]
        );

        this.createAgedPayableChart(result);
    }

    async loadAgedReceivable(period) {
        const result = await this.orm.call(
            'account.move',
            'get_latebillss',
            [this.state.posted, period]
        );

        this.createAgedReceivableChart(result);
    }

    async loadInvoiceDataCurrentMonth() {
        const result = await this.orm.call(
            "account.move",
            "get_total_invoice_current_month",
            [this.state.posted]
        );

        // Update DOM with invoice data
        // This would need to be converted to OWL reactive state
        this.updateInvoiceDisplay(result, 'month');
    }

    async loadInvoiceDataCurrentYear() {
        const result = await this.orm.call(
            "account.move",
            "get_total_invoice_current_year",
            [this.state.posted]
        );

        this.updateInvoiceDisplay(result, 'year');
    }

    async loadTop10Customers(period) {
        const result = await this.orm.call(
            "account.move",
            "get_top_10_customers_month",
            [this.state.posted, period]
        );

        // Update top customers list (convert to reactive state)
        // TODO: Implement reactive top 10 customers display
    }

    async loadBankBalance() {
        const result = await this.orm.call(
            "account.move",
            "bank_balance",
            [this.state.posted]
        );

        // Update bank balance display
        // TODO: Implement reactive bank balance display
    }

    async loadOverdues() {
        const result = await this.orm.call(
            "account.move",
            "get_overdues",
            []
        );

        // Update overdues list
        // TODO: Implement reactive overdues display
    }

    async loadLateBills() {
        const result = await this.orm.call(
            "account.move",
            "get_latebills",
            []
        );

        // Update late bills list
        // TODO: Implement reactive late bills display
    }

    async loadUnreconciledItems() {
        const result = await this.orm.call(
            "account.move",
            "unreconcile_items",
            []
        );

        // Update unreconciled items count
        // TODO: Implement reactive unreconciled items display
    }

    async loadIncomeExpenseData() {
        // Load income data
        const incomeMonth = await this.orm.call(
            "account.move",
            "month_income_this_month",
            [this.state.posted]
        );

        const incomeYear = await this.orm.call(
            "account.move",
            "month_income_this_year",
            [this.state.posted]
        );

        // Load expense data
        const expenseMonth = await this.orm.call(
            "account.move",
            "month_expense_this_month",
            [this.state.posted]
        );

        const expenseYear = await this.orm.call(
            "account.move",
            "month_expense_this_year",
            [this.state.posted]
        );

        // TODO: Update reactive state with income/expense data
    }

    async loadProfitData() {
        const profitMonth = await this.orm.call(
            "account.move",
            "profit_income_this_month",
            [this.state.posted]
        );

        const profitYear = await this.orm.call(
            "account.move",
            "profit_income_this_year",
            [this.state.posted]
        );

        // TODO: Update reactive state with profit data
    }

    updateInvoiceDisplay(result, period) {
        // TODO: Convert jQuery DOM manipulation to OWL reactive state
        // This is a placeholder for the actual implementation
    }

    async refreshAllData() {
        await this.loadInitialData();
    }

    /**
     * Action methods for clickable items
     */

    async onClickPartner(partnerId) {
        this.action.doAction({
            res_model: 'res.partner',
            name: 'Partner',
            views: [[false, 'form']],
            type: 'ir.actions.act_window',
            res_id: partnerId,
        });
    }

    async onClickBankAccount(accountId) {
        this.action.doAction({
            res_model: 'account.account',
            name: 'Account',
            views: [[false, 'form']],
            type: 'ir.actions.act_window',
            res_id: accountId,
        });
    }

    async onClickInvoice(invoiceIds, title) {
        this.action.doAction({
            res_model: 'account.move',
            name: title,
            views: [[false, 'list'], [false, 'form']],
            type: 'ir.actions.act_window',
            domain: [['id', 'in', invoiceIds]],
        });
    }

    async onClickAccountMoveLine(lineIds, title) {
        this.action.doAction({
            res_model: 'account.move.line',
            name: title,
            views: [[false, 'list'], [false, 'form']],
            type: 'ir.actions.act_window',
            domain: [['id', 'in', lineIds]],
        });
    }
}

// Register the dashboard action
registry.category("actions").add("invoice_dashboard", AccountDashboard);

export default AccountDashboard;
