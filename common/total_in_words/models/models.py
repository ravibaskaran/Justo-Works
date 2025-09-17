# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCurrency(models.Model):
    _inherit = "res.currency"

    def convert_number_to_words(self, number):

        if number % 1 == 0:
            number = int(number)

        def get_word(n):
            words = {0: "", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight",
                     9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen",
                     15: "Fifteen", 16: "Sixteen", 17: "Seventeen", 18: "Eighteen", 19: "Nineteen", 20: "Twenty",
                     30: "Thirty", 40: "Forty", 50: "Fifty", 60: "Sixty", 70: "Seventy", 80: "Eighty", 90: "Ninty"}
            if n <= 20:
                return words[n]
            else:
                ones = n % 10
                tens = n - ones
                return words[tens] + " " + words[ones]

        def get_all_word(n):
            d = [100, 10, 100, 100]
            v = ["", "Hundred And", "Thousand", "Lakh"]
            w = []
            for i, x in zip(d, v):
                t = get_word(n % i)
                if t != "":
                    t += " " + x
                w.append(t.rstrip(" "))
                n = n // i
            w.reverse()
            w = ' '.join(w).strip()
            if w.endswith("And"):
                w = w[:-3]
            return w

        word = ""
        if number != 0:
            arr = str(number).split(".")
            number = int(arr[0])
            crore = number // 10000000
            number = number % 10000000

            if crore > 0:
                word += get_all_word(crore)
                word += " crore "
            word += get_all_word(number).strip() + " Rupees"
            if len(arr) > 1:
                if len(arr[1]) == 1:
                    arr[1] += "0"
                word += " and " + get_all_word(int(arr[1])) + " paisa"
        else:
            word += "Zero Rupees"
        return word


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('amount_total')
    def _compute_amount_total_words(self):
        for rec in self:
            rec.amount_total_words = self.env.company.currency_id.convert_number_to_words(rec.amount_total)

    amount_total_words = fields.Char("Total (In Words)", compute="_compute_amount_total_words")


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.depends('amount_total')
    def _compute_amount_total_words(self):
        for rec in self:
            rec.amount_total_words = self.env.company.currency_id.convert_number_to_words(rec.amount_total)

    amount_total_words = fields.Char("Total (In Words)", compute="_compute_amount_total_words")


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('amount_total')
    def _compute_amount_total_words(self):
        for invoice in self:
            if invoice.direct_journal_entry_inx and invoice.direct_journal_type_inx in ['payment', 'receipt',
                                                                                        'receipt_reverse',
                                                                                        'payment_reverse']:
                invoice.amount_total_words = invoice.currency_id.convert_number_to_words(
                    sum(invoice.direct_journal_item_ids.mapped('receipt_amount')) + sum(
                        invoice.direct_journal_item_ids.mapped('payment_amount')))
            else:
                invoice.amount_total_words = invoice.currency_id.convert_number_to_words(invoice.amount_total)
