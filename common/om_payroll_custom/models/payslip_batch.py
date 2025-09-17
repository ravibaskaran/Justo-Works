from odoo import models, api,_,fields
from odoo.exceptions import UserError


# ♦ ▼ Inherited 'HR Payslip Run'. ▼ ♦
class NewModule(models.Model):
    _inherit = 'hr.payslip.run'

    journal_id = fields.Many2one('account.journal', 'Salary Journal', states={'draft': [('readonly', False)]},
                                 readonly=True, required=True,
                                 default=lambda self: self.env['account.journal'].search([('type', '=', 'bank')],
                                                                                         limit=1))
    @api.onchange('journal_id','date_start','date_end')
    def onchange_journal_batch(self):
        if self.journal_id:
            if self.slip_ids:
                for i in self.slip_ids:
                    if i.state != 'done':
                        i.account_journal_id = self.journal_id
                        i.date_from = self.date_start if self.date_start else i.date_from
                        i.date_to = self.date_end if self.date_end else i.date_to
                        i.onchange_employee()
                        i.onchange_leave_deduction_amount()
                        i.check_employee_payslip

    # ♦ Mass Compute ♦
    def mass_compute(self):
        if self.slip_ids:
            for i in self.slip_ids:
                i.account_journal_id = self.journal_id
                i.onchange_employee_id(i.date_from, i.date_to, employee_id=False, contract_id=False)
                i.onchange_employee()
                i.onchange_leave_deduction_amount()
                i.check_employee_payslip
                i.compute_sheet()

    # ♦ Mass Confirm ♦
    def mass_confirm(self):
        for i in self.slip_ids:
            if not i.payable_amount:
                raise UserError(_("Please compute first"))
            i.action_payslip_done()
        self.close_payslip_run()

    # ♦ Reset to Draft ♦
    def draft_payslip_run(self):
        if self.slip_ids:
            for i in self.slip_ids:
                if i.state == 'done':
                    i.cancel_sheet()
                    i.action_payslip_draft()
        return self.write({'state': 'draft'})

