from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    # invoice_date = fields.Date(default=fields.Date.context_today)
    # bill_date = fields.Date()

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if self._context.get('default_direct_journal_entry_inx'):
            if res.get('toolbar', False) and res.get('toolbar').get('print', False):
                prints_to_remove = [self.env.ref('real_estate_extension.account_invoice_print_action')]
                for print_id in prints_to_remove:
                    reports = res.get('toolbar').get('print')
                    for report in reports:
                        if report.get('id', False) and report.get('id') == print_id.id:
                            res['toolbar']['print'].remove(report)
        return res

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
