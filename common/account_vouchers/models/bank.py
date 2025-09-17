# ♦ Import ♦
from odoo import models,Command, fields, api
from odoo.exceptions import ValidationError


# ♦ Inherited Res Bank ♦
class ResBank(models.Model):
    _inherit = 'res.bank'

    @api.model
    def get_partner_domain(self):
        return [('id', '=', self.env.company.partner_id.id)]

    def _default_inbound_payment_methods(self):
        return self.env.ref('account.account_payment_method_manual_in')

    def _default_outbound_payment_methods(self):
        return self.env.ref('account.account_payment_method_manual_out')

    account_number = fields.Char()
    partner_id = fields.Many2one('res.partner', 'Account Holder', domain=get_partner_domain)
    inbound_payment_method_ids = fields.Many2many('account.payment.method', 'account_journal_inbound_payment_method_rel', 'journal_id', 'inbound_payment_method',
        domain=[('payment_type', '=', 'inbound')], string='For Incoming Payments', default=lambda self: self._default_inbound_payment_methods())
    outbound_payment_method_ids = fields.Many2many('account.payment.method', 'account_journal_outbound_payment_method_rel', 'journal_id', 'outbound_payment_method',
        domain=[('payment_type', '=', 'outbound')], string='For Outgoing Payments', default=lambda self: self._default_outbound_payment_methods())
    bank_account_type = fields.Char()

    @api.model
    def default_get(self, fields):
        res = super(ResBank, self).default_get(fields)
        res['country'] = self.env.company.country_id.id
        res['state'] = self.env.company.state_id.id
        res['partner_id'] = self.env.company.partner_id.id
        return res

    @api.model
    def create(self, values):
        res = super(ResBank, self).create(values)
        res_partner_bank_id = self.env['res.partner.bank'].create({
            'acc_number': res.account_number,
            'bank_id': res.id,
            'partner_id': self.env.company.partner_id.id,
            'acc_holder_name': res.partner_id.name
        })
        print(res.inbound_payment_method_ids.ids,"res.inbound_payment_method_ids.ids")
        print(res.outbound_payment_method_ids.ids,"res.outbound_payment_method_ids.ids")
        journal = self.env['account.journal'].create({
            'name': res.name,
            'code': res.bic,
            'type': 'bank',
            'company_id': self.env.company.id,
            'bank_account_id': res_partner_bank_id.id,
            'inbound_payment_method_line_ids': None,
            'outbound_payment_method_line_ids': None
        })
        journal.profit_account_id = journal.default_account_id
        journal.loss_account_id = journal.default_account_id
        inbound_data = []
        journal.inbound_payment_method_line_ids = False
        journal.outbound_payment_method_line_ids = False
        for line in res.inbound_payment_method_ids:
            inbound_data.append((0, 0, {
                'payment_method_id': line.id,
                'name': line.name,
                'payment_account_id': journal.default_account_id.id
            }))
        journal.inbound_payment_method_line_ids = inbound_data
        outbound_data = []
        for line in res.outbound_payment_method_ids:
            outbound_data.append((0, 0, {
                'payment_method_id': line.id,
                'name': line.name,
                'payment_account_id': journal.default_account_id.id
            }))
        journal.outbound_payment_method_line_ids = outbound_data
        return res

    def write(self, values):
        res = super(ResBank, self).write(values)
        if values.get('name'):
            account_journal = self.env['account.journal']
            related_journals = account_journal.search([("bank_id", "=", self.id)])
            default_debit_account_id = related_journals.mapped('loss_account_id')
            default_credit_account_id = related_journals.mapped('profit_account_id')
            len_rel_debit_acc_id = len(default_debit_account_id)
            len_rel_credit_acc_id = len(default_credit_account_id)
            if len_rel_debit_acc_id == 1:
                default_debit_account_id.name = values.get('name')
                pass
            elif len_rel_debit_acc_id == 0:
                pass
            else:
                raise ValidationError('Related Multiple Bank Journal has Different Default Debit Account:- ' + str(
                    default_debit_account_id.mapped('name')))
            if len_rel_credit_acc_id == 1:
                default_credit_account_id.name = values.get('name')
                pass
            elif len_rel_credit_acc_id == 0:
                pass
            else:
                raise ValidationError('Related Multiple Bank Journal has Different Default Credit Account:- ' + str(
                    default_credit_account_id.mapped('name')))
        return res


#   ♦ ▼ Inherited 'Account Journal'. ▼ ♦
class AccountJournalInherit(models.Model):
    _inherit = 'account.journal'

    # Removed the domain filter from these fields.
    profit_account_id = fields.Many2one(
            comodel_name='account.account', check_company=True,
            help="Used to register a profit when the ending balance of a cash register differs from what the system computes",
            string='Profit Account',domain=[])

    loss_account_id = fields.Many2one(
            comodel_name='account.account', check_company=True,
            help="Used to register a loss when the ending balance of a cash register differs from what the system computes",
            string='Loss Account',domain=[])

    @api.depends('type', 'currency_id')
    def _compute_inbound_payment_method_line_ids(self):
        for journal in self:
            pay_method_line_ids_commands = [Command.clear()]
            if journal.type in ('bank', 'cash'):
                default_methods = journal._default_inbound_payment_methods()
                pay_method_line_ids_commands += [Command.create({
                    'name': pay_method.name,
                    'payment_method_id': pay_method.id,
                    'payment_account_id': journal.default_account_id
                }) for pay_method in default_methods]
            journal.inbound_payment_method_line_ids = pay_method_line_ids_commands

    @api.depends('type', 'currency_id')
    def _compute_outbound_payment_method_line_ids(self):
        for journal in self:
            pay_method_line_ids_commands = [Command.clear()]
            if journal.type in ('bank', 'cash'):
                default_methods = journal._default_outbound_payment_methods()
                pay_method_line_ids_commands += [Command.create({
                    'name': pay_method.name,
                    'payment_method_id': pay_method.id,
                    'payment_account_id': journal.default_account_id
                }) for pay_method in default_methods]
            journal.outbound_payment_method_line_ids = pay_method_line_ids_commands