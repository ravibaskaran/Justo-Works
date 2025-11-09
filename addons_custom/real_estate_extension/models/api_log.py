from odoo import models, fields, api


class ApiLog(models.Model):
    _name = 'api.log'
    _description = 'API Log'
    _order = 'date desc'

    active = fields.Boolean(string="Active", default=True, help="Set to False to archive old logs")
    name = fields.Char(string="API Name")
    code = fields.Char(string="API Code")
    response = fields.Text(string="Response (Legacy)", help="Deprecated - use response_payload instead")
    date = fields.Datetime(string="Timestamp")
    type = fields.Selection([
        ('employee', 'Employee'),
        ('project', 'Project'),
        ('customer', 'Customer'),
        ('cp', 'CP'),
        ('cp_emp', 'CP Employee'),
        ('inventory', 'Inventory'),
        ('booking', 'Booking'),
        ('employee_assign', 'Project Employee Assign'),
        ('employee_details', 'Employee Details')
    ], string="API Type")
    status = fields.Selection([
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string="Status")
    record = fields.Char(string="Record Reference")
    direction = fields.Selection([
        ('in', 'In'),
        ('out', 'Out')
    ], string="Direction")

    # Legacy field - kept for backward compatibility
    args = fields.Text(string="Arguments (Legacy)", help="Deprecated - use request_payload instead")

    # New security and audit fields
    ip_address = fields.Char(string="IP Address", size=45, help="Client IP address (IPv4 or IPv6)")
    user_agent = fields.Text(string="User Agent", help="Client user agent string")
    execution_time = fields.Float(string="Execution Time (ms)", help="API execution time in milliseconds")

    # Structured payload fields
    request_payload = fields.Text(string="Request Payload (Sanitized)", help="Sanitized request data")
    response_payload = fields.Text(string="Response Payload (Sanitized)", help="Sanitized response data")

    # Security flags
    sanitized = fields.Boolean(string="Data Sanitized", default=False, help="Indicates if sensitive data was sanitized")
    is_sensitive = fields.Boolean(string="Contains Sensitive Data", default=False, help="Indicates if request contained sensitive fields")
