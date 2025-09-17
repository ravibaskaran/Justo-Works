# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class BetaCategoryWiseAsset(models.TransientModel):  # change this
    _name = 'beta.category.wise.asset'  # change this
    _inherit = 'beta.reports'

    name = fields.Char(default='Category Wise Asset Report')  # change this
    category_ids = fields.Many2many('account.asset.category')
    date_from = fields.Date()
    date_to = fields.Date()

    @api.model
    def default_get(self, fields_list):
        res = super(BetaCategoryWiseAsset, self).default_get(fields_list)
        today = datetime.today()
        res['date_from'] = res['date_to'] = today
        return res

    def get_html(self):
        self.template_area = self.env.ref('category_wise_asset.report_category_wise_asset')._render({
            'date': self.date_from.strftime('%d/%m/%Y'),
            'date_to': self.date_to.strftime('%d/%m/%Y'),
            'lines': self.get_category_asset(),
        })

    def get_category_asset(self):
        doc = []
        asset_final = []
        asset = ''

        if self.date_from:
            domain = [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('state', '=', 'open')]
            if self.category_ids:
                domain.append(('category_id', 'in', self.category_ids.ids))

            asset = self.env['account.asset.asset'].search(domain).sorted(lambda line: line.category_id.name,
                                                                          reverse=False)

        if asset:
            for line in asset:
                doc.append({
                    'category_id': line.category_id.id,
                    'date': line.date.strftime('%d/%m/%Y'),
                    'category_name': line.category_id.name,
                    'asset_name': line.name,
                    'ser_number': line.ser_number,
                    'make': line.manufacture,
                    'holder': line.holder,
                    'purpose': line.purpose,
                })
        if len(doc) > 0:
            i = 0
            category_id = doc[0]['category_id']
            asset_final.append({
                'name': 5,
                'category_name': doc[0]['category_name'],
                'date': None,
                'make': None,
                'ser_number': None,
                'asset_name': None,
                'holder': None,
                'purpose': None,
            })

            while i < len(doc):
                if category_id == doc[i]['category_id']:
                    asset_final.append({
                        'name': 1,
                        'category_name': doc[i]['category_name'],
                        'date': doc[i]['date'],
                        'make': doc[i]['make'],
                        'ser_number': doc[i]['ser_number'],
                        'asset_name': doc[i]['asset_name'],
                        'holder': doc[i]['holder'],
                        'purpose': doc[i]['purpose'],
                    })
                else:
                    category_id = doc[i]['category_id']
                    asset_final.append({
                        'name': 5,
                        'category_name': doc[i]['category_name'],
                        'date': None,
                        'make': None,
                        'ser_number': None,
                        'asset_name': None,
                        'holder': None,
                        'purpose': None,
                    })
                    asset_final.append({
                        'name': 1,
                        'category_name': doc[i]['category_name'],
                        'date': doc[i]['date'],
                        'make': doc[i]['make'],
                        'ser_number': doc[i]['ser_number'],
                        'asset_name': doc[i]['asset_name'],
                        'holder': doc[i]['holder'],
                        'purpose': doc[i]['purpose'],
                    })
                i = i + 1
            return {
                'docsnn': asset_final,
            }
