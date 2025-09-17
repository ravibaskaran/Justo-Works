# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models


class GstHsnData(models.TransientModel):
    _name = "gst.hsn.data"
    _description = "GST HSN data"

    def getHSNData(self, invoiceObj, count, hsnDict={}, hsnDataDict={}):
        mainData = []
        jsonData = []
        currency = invoiceObj.currency_id or None
        ctx = dict(self._context or {})
        sign = -1 if invoiceObj.move_type in ('out_refund', 'in_refund') else 1
        for invoiceLineObj in invoiceObj.invoice_line_ids.filtered(lambda l: l.product_id):
            quantity = invoiceLineObj.quantity or 1.0
            price = invoiceLineObj.price_subtotal / quantity
            taxedAmount, cgst, sgst, igst, cess, rt = 0.0, 0.0, 0.0, 0.0, 0.0, 0
            rateObjs = invoiceLineObj.tax_ids
            for rateObj in rateObjs:
                if rateObjs:
                    taxData = self.env['gst.tax.data'].getTaxedAmount(
                        rateObj, price, currency, invoiceLineObj, invoiceObj)
                    rateAmount = taxData[1]
                    taxAmount = taxData[0]
                    if currency.name != 'INR':
                        taxAmount = taxAmount * currency.rate
                    taxedAmount += round(taxAmount, 2)
                    # if invoiceObj.partner_id.country_id.code == 'IN':
                    rateObj = rateObj[0]
                    print(rateObj.name)
                    if rateObj.amount_type == "group":
                        rt += rateObj.children_tax_ids and rateObj.children_tax_ids[0].amount * 2 or 0
                        cgst += round(taxAmount / 2, 2)
                        sgst += round(taxAmount / 2, 2)
                    else:
                        if 'cess' in rateObj.name.lower():
                            cess += round(taxAmount, 2)
                        else:
                            rt += rateObj.amount
                            igst += round(taxAmount, 2)
            invUntaxedAmount = round(invoiceLineObj.price_subtotal, 2)
            if currency.name != 'INR':
                invUntaxedAmount = round(invoiceLineObj.price_subtotal * currency.rate, 2)
            productObj = invoiceLineObj.product_id
            hsnvalue = productObj.l10n_in_hsn_code or ''
            hsnVal = hsnvalue.replace('.', '') or 'False'
            hsnName = '' # productObj.name or 'name'
            uqc = 'OTH-OTHERS'
            if productObj.uom_id:
                uom = productObj.uom_id.id
                uqcObj = self.env['uom.mapping'].search([('uom', '=', uom)])
                if uqcObj:
                    uqc = uqcObj[0].name.code+'-'+uqcObj[0].name.name
            hsnTuple = (uqc, rt)
            invQty = sign * invoiceLineObj.quantity
            invAmountTotal = sign * (invUntaxedAmount + taxedAmount)
            invUntaxedAmount *= sign
            igst *= sign
            cgst *= sign
            sgst *= sign
            cess *= sign
            if hsnDataDict.get(hsnVal):
                hsnTupleDict = hsnDataDict.get(hsnVal).get(hsnTuple) or {}
                if hsnTupleDict:
                    if hsnTupleDict.get('qty'):
                        invQty += hsnTupleDict.get('qty')
                        hsnTupleDict['qty'] = invQty
                    else:
                        hsnTupleDict['qty'] = invQty
                    if hsnTupleDict.get('val'):
                        invAmountTotal = round(hsnTupleDict.get('val') + invAmountTotal, 2)
                        hsnTupleDict['val'] = invAmountTotal
                    else:
                        invAmountTotal = round(invAmountTotal, 2)
                        hsnTupleDict['val'] = invAmountTotal
                    if hsnTupleDict.get('txval'):
                        invUntaxedAmount = round(hsnTupleDict.get('txval') + invUntaxedAmount, 2)
                        hsnTupleDict['txval'] = invUntaxedAmount
                    else:
                        invUntaxedAmount = round(invUntaxedAmount, 2)
                        hsnTupleDict['txval'] = invUntaxedAmount
                    if hsnTupleDict.get('iamt'):
                        igst = round(hsnTupleDict.get('iamt') + igst, 2)
                        hsnTupleDict['iamt'] = igst
                    else:
                        igst = round(igst, 2)
                        hsnTupleDict['iamt'] = igst
                    if hsnTupleDict.get('camt'):
                        cgst = round(hsnTupleDict.get('camt') + cgst, 2)
                        hsnTupleDict['camt'] = cgst
                    else:
                        cgst = round(cgst, 2)
                        hsnTupleDict['camt'] = cgst
                    if hsnTupleDict.get('samt'):
                        sgst = round(hsnTupleDict.get('samt') + sgst, 2)
                        hsnTupleDict['samt'] = sgst
                    else:
                        sgst = round(sgst, 2)
                        hsnTupleDict['samt'] = sgst
                    if hsnTupleDict.get('csamt'):
                        cess = round(hsnTupleDict.get('csamt') + cess, 2)
                        hsnTupleDict['csamt'] = cess
                    else:
                        cess = round(cess, 2)
                        hsnTupleDict['csamt'] = cess
                else:
                    count += 1
                    hsnDataDict.get(hsnVal)[hsnTuple] = {
                        'num': count,
                        'hsn_sc': hsnVal,
                        'uqc': uqc,
                        'qty': invQty,
                        'rt': rt,
                        'txval': invUntaxedAmount,
                        'iamt': igst,
                        'camt': cgst,
                        'samt': sgst,
                        'csamt': cess,
                        # 'desc': hsnName,
                        'val': round(invAmountTotal,2),


                    }
            else:
                count += 1
                hsnDataDict[hsnVal] = {
                    hsnTuple: {
                        'num': count,
                        'hsn_sc': hsnVal,
                        # 'desc': hsnName,
                        'uqc': uqc,
                        'qty': invQty,
                        'rt': rt,
                        'txval': invUntaxedAmount,
                        'iamt': igst,
                        'camt': cgst,
                        'samt': sgst,
                        'csamt': cess,
                        'val': round(invAmountTotal,2),
                    }
                }
            hsnvalue = productObj.l10n_in_hsn_code or ''
            hsnData = [
                hsnvalue.replace('.', ''), hsnName, uqc, invQty,
                invAmountTotal, rt, invUntaxedAmount, igst, cgst, sgst, cess
            ]
            if hsnDict.get(hsnVal):
                hsnDict.get(hsnVal)[hsnTuple] = hsnData
            else:
                hsnDict[hsnVal] = {hsnTuple: hsnData}
            mainData.append(hsnData)
        # print(hsnDataDict)
        return [mainData, jsonData, hsnDict, hsnDataDict]
