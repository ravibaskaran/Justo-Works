from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import Warning

class MultipleAccountOpening(models.Model):
    _name = "multiple.account.opening"
    _order = "id desc"

    @api.model
    def default_get(self, fieldsname):
        res = super(MultipleAccountOpening, self).default_get(fieldsname)
        res['date'] = datetime.now().date()
        return res

    name = fields.Char(required=True)
    date = fields.Date(required=True, readonly=True,
                                  states={'draft': [('readonly', False)]})
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 default=lambda self: self.env.company, required=True, readonly=False)
    account_opening_move_id = fields.Many2one(string='Opening Journal Entry', comodel_name='account.move',
                                              related="company_id.account_opening_move_id")
    opening_ids = fields.One2many('multiple.account.opening.line', 'multiple_id', string='Journal Items', readonly=True,
                                  states={'draft': [('readonly', False)]})
    summary_ids = fields.One2many('multiple.account.opening.summary', 'multiple_id', string='Journal Items', readonly=True,
                                  compute="_get_account_opening_summary", store=True)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft')

    def validate_opening(self):
        if not self.opening_ids:
            raise Warning("No opening entries")
        self.state = 'posted'
        self.update_move_journal_items()

    def set_to_draft_opening(self):
        self.state = 'draft'
        self.update_move_journal_items()

    def cancel_opening(self):
        self.state = 'cancel'
        self.update_move_journal_items()

    def update_move_journal_items(self):
        if not self.account_opening_move_id:
            self.company_id.create_op_move_if_non_existant()
        self.account_opening_move_id.date = self.date
        if self.account_opening_move_id.state == 'posted':
            self.account_opening_move_id.button_draft()
        posted_openings = self.search([('state', '=', 'posted')])
        data = []
        total_credit = total_debit = balance_credit = balance_debit = 0
        for opening in posted_openings:
            for line in opening.opening_ids:
                data.append((0, 0, {'account_id': line.account_id.id,
                                    'partner_id': line.partner_id.id if line.partner_id else False, 'name': line.name,
                                    'debit': line.debit, 'credit': line.credit}))
                total_credit += line.credit
                total_debit += line.debit
        balance_account = self.env['account.account'].search([('code', '=', str(999999))]).id
        balance = total_credit - total_debit
        if balance > 0:
            balance_debit = balance
        else:
            balance_credit = abs(balance)
        data.append((0, 0, {'account_id': balance_account, 'debit': balance_debit, 'credit': balance_credit}))
        if self.account_opening_move_id.line_ids:
            self.account_opening_move_id.line_ids.unlink()
        self.account_opening_move_id.write({'line_ids': data})
        self.account_opening_move_id.action_post()
        return True

    @api.depends('opening_ids.credit','opening_ids.debit')
    def _get_account_opening_summary(self):
        for opening in self:
            data = {}
            for line in opening.opening_ids:
                if line.account_id.id in data:
                    data[line.account_id.id]['debit'] += line.debit
                    data[line.account_id.id]['credit'] += line.credit
                else:
                    data[line.account_id.id] = {
                        'debit': line.debit,
                        'credit' : line.credit,
                    }
            rows = []
            for item in data:
                rows.append((0,0,{'account_id': item, 'debit': data[item]['debit'], 'credit': data[item]['credit']}))
            opening.summary_ids = False
            opening.summary_ids = rows

class MultipleAccountOpeningLine(models.Model):
    _name = "multiple.account.opening.line"

    multiple_id = fields.Many2one('multiple.account.opening')
    account_id = fields.Many2one('account.account', string='Account',
                                 index=True, ondelete="restrict", check_company=True,
                                 domain=[('deprecated', '=', False)], required=True)
    name = fields.Char(string='Remark')
    partner_id = fields.Many2one('res.partner', string='Partner', ondelete='restrict')
    debit = fields.Monetary(string='Debit', default=0.0, currency_field='company_currency_id')
    credit = fields.Monetary(string='Credit', default=0.0, currency_field='company_currency_id')
    company_id = fields.Many2one(related='multiple_id.company_id', store=True, readonly=True)
    company_currency_id = fields.Many2one(related='multiple_id.company_id.currency_id', string='Company Currency',
                                          readonly=True, store=True,
                                          help='Utility field to express amount currency')

class MultipleAccountOpeningSummary(models.Model):
    _name = "multiple.account.opening.summary"

    account_id = fields.Many2one('account.account', string='Account')
    multiple_id = fields.Many2one('multiple.account.opening')
    debit = fields.Monetary(string='Debit', default=0.0, currency_field='company_currency_id')
    credit = fields.Monetary(string='Credit', default=0.0, currency_field='company_currency_id')
    company_id = fields.Many2one(related='multiple_id.company_id', store=True, readonly=True)
    company_currency_id = fields.Many2one(related='multiple_id.company_id.currency_id', string='Company Currency',
                                          readonly=True, store=True,
                                          help='Utility field to express amount currency')

