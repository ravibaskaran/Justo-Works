from odoo import models, fields,_
from odoo.exceptions import UserError


class BranchHsnReport(models.TransientModel):
    _name = 'branch.hsn.report'

    branch = fields.Many2many('res.branch',required=True)
    hsn_attachment = fields.Many2one('ir.attachment', help="HSN Data Attachment")

    def get_hsn_branch_report(self):
        self.hsn_attachment = None
        active_id = self.env['gstr1.tool'].search([('id','in',self.env.context.get('active_ids'))])
        invoiceObjs = active_id.invoice_lines
        name = active_id.name
        gstType = active_id.gst_type
        ctx = dict(active_id._context or {})
        invoiceIds = []
        if invoiceObjs:
            for line in invoiceObjs:
                if line.branch_id.id in self.branch.ids:
                    invoiceIds.append(line.id)
            respHsnData = self.env['export.csv.wizard'].with_context(
                ctx).exportCsv(invoiceIds, 'hsn', name, gstType)
            if respHsnData:
                hsnAttachment = respHsnData[0]
                if hsnAttachment:
                    self.hsn_attachment = hsnAttachment.id
        if not self.hsn_attachment:
            raise UserError(_("HSN of gst invoice is not present"))
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (self.hsn_attachment.id),
            'target': 'new',
        }