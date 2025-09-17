# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, models


class GstTaxData(models.TransientModel):
    _name = "gst.tax.data"
    _description = "GST tax data"

    def getTaxedAmount(self, rateObjs, price, currency, invoiceLineObj, invoiceObj):
        taxedAmount = 0.0
        total_excluded = 0.0
        taxes = rateObjs.compute_all(price, currency, invoiceLineObj.quantity,
                                     product=invoiceLineObj.product_id, partner=invoiceObj.partner_id,handle_price_include=invoiceLineObj.tax_ids[0].included_in_price)
        if taxes:
            total_included = taxes.get('total_included') or 0.0
            total_excluded = taxes.get('total_excluded') or 0.0
            taxedAmount = total_included - total_excluded
        if currency.name != 'INR':
            taxedAmount = taxedAmount * currency.rate
            total_excluded = total_excluded * currency.rate
        return [taxedAmount, total_excluded]

    def getGstTaxData(self, invoiceObj, invoiceLineObj, rateObjs, taxedAmount, invoiceType):
        taxedAmount = round(taxedAmount, 2)
        gstDict = {
            "txval": 0.0,
            "rt": 0.0,
            "iamt": 0.0,
            "camt": 0.0,
            "samt": 0.0,
            "csamt": 0.0
        }
        if invoiceType == "export":
            gstDict = {"txval": 0.0, "rt": 0, "iamt": 0.0}
        if invoiceType in ['imps', 'impg']:
            gstDict = {
                "elg": "no",
                "txval": 0.0,
                "rt": 0,
                "iamt": 0.0,
                'tx_i': 0.0,
                'tx_cs': 0.0
            }
        if invoiceType == "b2cs":
            gstDict = {
                "rt": 0.0,
                "sply_ty": '',
                "pos": '',
                "typ" : '',
                "txval": 0.0,
                "iamt": 0.0,
                "camt": 0.0,
                "samt": 0.0,
                "csamt": 0.0
            }
            gstDict['sply_ty'] = 'INTRA'
            gstDict['typ'] = 'OE'
        if rateObjs:
            # rateObj = rateObjs[0]
            for rateObj in rateObjs:
                if invoiceObj.partner_id.country_id.code == 'IN':
                    if rateObj.amount_type == "group":
                        gstDict['rt'] += rateObj.children_tax_ids and rateObj.children_tax_ids[0].amount * 2 or 0
                        gstDict['samt'] += round(taxedAmount / 2, 2)
                        gstDict['camt'] += round(taxedAmount / 2, 2)
                        # print(gstDict,'dict')
                    else:
                        # gstDict['rt'] += rateObj.amount
                        if 'cess' in rateObj.name.lower():
                            gstDict['csamt'] += round(taxedAmount, 2)
                        else:
                            gstDict['rt'] += rateObj.amount
                            gstDict['iamt'] += round(taxedAmount, 2)
                        # print(gstDict,'elsse')

                elif invoiceType in ['imps', 'impg']:

                    if 'cess' in rateObj.name.lower():
                        gstDict['csamt'] += round(taxedAmount, 2)
                    else:
                        gstDict['rt'] += rateObj.amount
                        gstDict['iamt'] += round(taxedAmount, 2)
                    # gstDict['iamt'] += round(taxedAmount, 2)
                    # print(gstDict, 'elih')

        return gstDict
