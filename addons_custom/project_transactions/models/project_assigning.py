from odoo import models, fields, api
from odoo.exceptions import UserError


class ProjectAssigning(models.Model):
    _name = 'project.assigning'
    _inherit = ['mail.thread']
    _description = 'Project Assigning'
    _rec_name = 'project_id'

    project_id = fields.Many2one('building')
    business_head = fields.Many2one('hr.employee')
    site_head = fields.Many2one('hr.employee')
    source_head = fields.Many2one('hr.employee')
    closing_head = fields.Many2one('hr.employee')
    channel_partner = fields.Many2one('res.partner', domain=[('is_channel', '=', True)])
    closing_manager = fields.Many2one('hr.employee')
    assigning_flat_ids = fields.One2many('project.assigning.flats', 'project_assigning_id')
    select_all = fields.Boolean()

    @api.onchange('select_all')
    def flat_select_all(self):
        for line in self.assigning_flat_ids:
            if self.select_all:
                line.activate = True
            else:
                line.activate = False

    @api.model
    def create(self, values):
        res = super(ProjectAssigning, self).create(values)
        deactivated_lines = res.assigning_flat_ids.filtered(lambda l: not l.activate)
        deactivated_lines.unlink()
        for line in res.assigning_flat_ids.filtered(lambda l: l.activate):
            assigned_flat = self.env['project.assigning.flats'].search([('flat_id', '=', line.flat_id.id)]).filtered(
                lambda l: l.project_assigning_id.id != res.id)
            if assigned_flat:
                raise UserError(str(line.flat_id.name) + ' is already assigned!')
        return res

    def write(self, vals):
        res = super(ProjectAssigning, self).write(vals)
        deactivated_lines = self.assigning_flat_ids.filtered(lambda l: not l.activate)
        deactivated_lines.unlink()
        for line in self.assigning_flat_ids.filtered(lambda l: l.activate):
            assigned_flat = self.env['project.assigning.flats'].search([('flat_id', '=', line.flat_id.id)]).filtered(
                lambda l: l.project_assigning_id.id != self.id)
            if assigned_flat:
                raise UserError(str(line.flat_id.name) + ' is already assigned!')
        return res

    @api.onchange('project_id')
    def render_available_flats(self):
        flat_list = []
        if self.project_id:
            flats = self.env['product.template'].search([('building_id', '=', self.project_id.id), ('state', '!=', 'inactive')])
            for flat in flats:
                assigned_flat = self.env['project.assigning.flats'].search([('flat_id', '=', flat.id)]).filtered(
                    lambda l: l.project_assigning_id.id != self._origin.id)
                if not assigned_flat:
                    flat_list.append((0, 0, {
                        'flat_id': flat.id
                    }))
        self.assigning_flat_ids = False
        self.assigning_flat_ids = flat_list


class ProjectAssigningFlats(models.Model):
    _name = 'project.assigning.flats'
    _description = 'Project Assigning Flats'

    project_assigning_id = fields.Many2one('project.assigning', ondelete='cascade')
    flat_id = fields.Many2one('product.template')
    activate = fields.Boolean('Assign')
