from odoo import models, fields, api


class ApiLog(models.Model):
    _name = 'api.log'
    _description = 'API Log'

    name = fields.Char()
    code = fields.Char()
    response = fields.Text()
    date = fields.Datetime()
    type = fields.Selection([('employee', 'Employee'), ('project', 'Project'), ('customer', 'Customer'), ('cp', 'CP'),
                             ('cp_emp', 'CP Employee'), ('inventory', 'Inventory'), ('booking', 'Booking'),
                             ('employee_assign', 'Project Employee Assign'), ('employee_details', 'Employee Details')])
    status = fields.Selection([('success', 'Success'), ('failed', 'Failed')])
    record = fields.Char()
    direction = fields.Selection([('in', 'In'), ('out', 'Out')])
    args = fields.Text()
