from odoo import models, api


class InvoicePrint(models.AbstractModel):
    _name = 'report.real_estate_extension.invoice_print'
    _description = 'Invoice Print'

    @api.model
    def _get_report_values(self, docids, data=None):
        invoice = self.env['account.move'].browse(docids)
        line_limit = 19
        line_number = 0
        book = {}
        page_number = 1
        book[page_number] = []
        for line in invoice.invoice_line_ids:
            if line_number == line_limit:
                line_number = 0
                page_number += 1
                book[page_number] = []
            line_number += 1
            book[page_number].append({
                'line': line
            })
        bank = self.env['res.bank'].search([('is_invoice_bank', '=', True)], limit=1)
        return {
            'line_limit': line_limit,
            'book': book,
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'docs': self.env['account.move'].browse(docids),
            'report_type': data.get('report_type') if data else '',
            'bank': bank
        }
