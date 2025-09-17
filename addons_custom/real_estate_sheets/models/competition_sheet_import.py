from datetime import datetime

from odoo import models, fields, _
import xlrd
import base64
import tempfile
from odoo.exceptions import ValidationError


class CompetitionSheetImport(models.TransientModel):
    _name = 'competition.sheet.import'

    file = fields.Binary()

    def action_import(self):
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
        # print(excel_data)
        competition_object = self.env['competition.sheet']
        for competition in excel_data:
            if competition.get('Name of Project'):
                developer = self.env['res.partner'].search(
                    [('name', '=', competition.get('Developer')), ('is_owner', '=', True)])
                if not developer:
                    developer = self.env['res.partner'].create({
                        'name': competition.get('Developer'),
                        'is_owner': True
                    })
                configuration = self.env['building.unit'].search([('name', '=', competition.get('Configuration'))])
                if not configuration:
                    configuration = self.env['building.unit'].create({
                        'name': competition.get('Configuration')
                    })
                year, month, day, hour, minute, second = xlrd.xldate_as_tuple(competition.get('Possession date'),
                                                                              workbook.datemode)
                py_date = datetime(year, month, day, hour, minute, second)
                competition_object.create({
                    'name': competition.get('Name of Project'),
                    'developer_id': developer.id,
                    'location': competition.get('Location'),
                    'configuration': configuration.id,
                    'carpet_area': competition.get('Carpet area'),
                    'saleable_area': competition.get('Saleable Area'),
                    'all_in_package': competition.get('All in Package'),
                    'quoted_agreement_value': competition.get('Quoted Agreement Value'),
                    'discount': competition.get('Discount'),
                    'transacted_av': competition.get('Transacted AV'),
                    'transacted_rate_sale_area': competition.get('Transacted Rate p sq ft incl. infra'),
                    'approx_after_discount': competition.get('Apprx. All. Inclusive Package after discount'),
                    'possession_date': py_date
                })
        return {
            'name': 'Competition Sheet',
            'res_model': 'competition.sheet',
            'type': 'ir.actions.act_window', 'target': 'main',
            'view_mode': 'tree,form',
            'views': [(False, 'list'), (False, 'form'), (False, 'kanban'), (False, 'graph')],
        }
