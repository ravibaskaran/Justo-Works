from odoo import models, fields, _
import xlrd
import base64
import tempfile
from odoo.exceptions import ValidationError


class BuildingCreateInventory(models.TransientModel):
    _name = 'building.create.inventory'

    file = fields.Binary()
    project_id = fields.Many2one('building')

    def action_download_sample(self):
        # Return an action to open the URL that triggers the download
        return {
            'type': 'ir.actions.act_url',
            'url': '/project_transactions/download_sample_file',
            'target': 'self',
        }

    def action_generate(self):
        if not self.file:
            raise ValidationError('Please upload a file!')
        try:
            file = base64.b64decode(self.file)
            file_path = tempfile.gettempdir() + '/temp1.xlsx'
            f = open(file_path, 'wb')
            f.write(file)
            workbook = xlrd.open_workbook(file_path, on_demand=False)
            worksheet = workbook.sheet_by_index(0)
        except Exception as e:
            raise ValidationError(_("Not a valid file! " + str(e)))
        title_list = []
        for col in range(worksheet.ncols):
            title = worksheet.cell_value(0, col)
            title_list.append(title)
        excel_data = []
        for row in range(1, worksheet.nrows):
            row_dict = {}
            for col in range(worksheet.ncols):
                col_value = worksheet.cell_value(row, col)
                row_dict[title_list[col]] = col_value
            excel_data.append(row_dict)
        print(excel_data)
        property_pool = self.env['product.template']
        props = []
        try:
            for flat in excel_data:
                sequence = flat['Sr. No.']
                flat_number = str(flat['Flat No.'])
                flat_number = flat_number.rstrip('0').rstrip('.') if '.' in flat_number else flat_number
                floor = flat['Floor']
                wing = self.env['building.wing'].search([('name', '=', flat['Wing '])], limit=1)
                if not wing:
                    wing = self.env['building.wing'].create({'name': flat['Wing '], 'code': flat['Wing ']})
                flat_type = self.env['building.unit'].search([('name', '=', flat['Type'])], limit=1)
                if not flat_type:
                    flat_type = self.env['building.unit'].create({'name': flat['Type']})
                carpet = flat['Carpet']
                balcony = flat['Balcony / Garden']
                total_carpet = flat['Total Carpet']
                saleable_area = flat['Saleable Area']
                flat_name = self.project_id.code + '-' + str(wing.name) + '-' + str(flat_number)
                state = flat['Status']
                hold = flat['Hold']
                if hold and hold.lower() == 'yes':
                    on_hold = True
                else:
                    on_hold = False
                existing_flat = self.env['product.template'].search([('name', '=', flat_name), ('building_id', '=', self.project_id.id)], limit=1)
                if existing_flat:
                    existing_flat.flat_state = state.lower() if state else 'rts'
                    existing_flat.on_hold = on_hold
                    continue
                vals = {
                    'name': flat_name,
                    'code': flat_name,
                    'building_id': self.project_id.id,
                    'floor': int(floor),
                    'sequence': sequence,
                    'wing_id': wing.id,
                    'flat_number': flat_number,
                    'flat_type': flat_type.id,
                    'carpet': carpet,
                    'balcony': balcony,
                    'total_carpet': total_carpet,
                    'saleable_area': saleable_area,
                    'state': 'free',
                    'region_id': self.project_id.region_id.id,
                    'rel_anyletec_prop': self.project_id.account_analytic_id.id,
                    'flat_cost': self.project_id.pricing,
                    'is_property': True,
                    'flat_state': state.lower() if state else 'rts',
                    'on_hold': on_hold
                }
                print(vals)
                prop_id = property_pool.create(vals)
                props.append(prop_id.id)
            self.project_id.unit_ids = [(6, 0, props)]
        except:
            raise ValidationError('Not a valid file')
