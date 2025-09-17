# -*- coding: utf-8 -*-

# from numpy import product
from odoo import models, fields, api, tools
import json
# import time


class AdvanceSearch(models.AbstractModel):
    _name = "advance.search"

    def get_tally_result(self,tables,model_obj,model,sel1st,sel2nd,add,whr,limit):
        try:
            wquery = model_obj._where_calc([])
            model_obj._apply_ir_rules(wquery, 'read')
            from_c, where_c, where_params = wquery.get_sql()
            where_condition = where_c % tuple(where_params)
            where_condition = where_condition.replace(',)',')')
            query1 = """ 
                SELECT """+str(sel1st)+"""pid
                FROM (SELECT """+str(sel2nd)+model.replace('.','_')+""".id as pid
                FROM """+from_c+"""
                WHERE """+where_condition + """) innertable
                WHERE """+str(whr)+""" limit """+str(limit)
            self.env.cr.execute(query1)
            result = self.env.cr.dictfetchall()
        except Exception as e:
            self.env.cr.rollback()
            query2 = """SELECT """ + str(sel1st) + """pid
                FROM (SELECT """ + str(sel2nd) + model.replace('.', '_') + """.id as pid
                FROM """ + model.replace('.', '_') + add + """) innertable
                WHERE """+ str(whr) + """ limit """ + str(limit)
            self.env.cr.execute(query2)
            result = self.env.cr.dictfetchall()
        return result

    def _adv_search_rec_get(self, model, domain, search_on, search_keyword, search_result_fields, limit):
        # inherit and customize search results based on model. Append model's field name in 'search_on' list -
        # to check 'search_keyword' matches any field in the model
        search_results = []
        exact_match_dom = []
        any_word_domain = []
        model_obj = self.env[model]

        if 'tally' in search_on and search_keyword:
            search_key = search_keyword.replace(' ','').replace("'","''").replace('\\','\\\\')
            tables = self.env['ir.model'].search([('model', '=', model)])
            add = ''
            search_fields = search_on

            search_fields.remove('tally')
            if not search_fields:
                search_fields = ['name']
            sel1st = ''
            sel2nd = ''
            whr = ''
            count = 1
            for item in search_fields:
                sel1st += ' %s, ' %item
                sel2nd += " Replace(%s,' ','') as %s, " %(item,item)
                if count>1:
                    whr += ' or '
                whr += item+""" ilike '%"""+str(search_key)+"""' or """+item+""" ilike '%"""+str(search_key)+"""%' """
                count += 1
            for t in tables:
                for j in t.inherited_model_ids:
                    rel_field = self.env['ir.model.fields'].search(
                        [('model', '=', model), ('relation', '=', j.model)], limit=1)
                    add += ' left join %s on %s.id=%s.%s' %(j.model.replace('.','_'),j.model.replace('.','_'),model.replace('.','_'),rel_field.name,)
            get_tally_result = self.get_tally_result(tables, model_obj, model, sel1st, sel2nd, add, whr, limit)

            table_ids = []

            for x in get_tally_result:
                table_ids.append(x['pid'])
            data_ids = model_obj.search([('id','in',table_ids)])
            search_results = data_ids.read(search_result_fields)

        else:
            for search_on_val in search_on:
                if '%' in search_on_val:
                    search_on_val = search_on_val.replace('%', '')
                    exact_match_dom.append(
                        (search_on_val, '=ilike', search_keyword + '%'))
                else:
                    exact_match_dom.append(
                        (search_on_val, '=ilike', search_keyword))
                any_word_domain.append(
                    (search_on_val, 'ilike', search_keyword))

            len_search_on = len(search_on)-1
            if len_search_on > 0:
                exact_match_dom = ['|']*len_search_on + exact_match_dom
                any_word_domain = ['|']*len_search_on + any_word_domain

            if search_keyword:
                search_results += model_obj.search_read(
                    domain+exact_match_dom, search_result_fields, limit=limit, order='name')
                next_limit = limit - len(search_results)

                if next_limit > 0:
                    product_products_ids = [pro['id'] for pro in search_results]
                    search_results += model_obj.search_read(
                        domain+any_word_domain + [('id', 'not in', product_products_ids)], search_result_fields, limit=next_limit)

            else:
                search_results += model_obj.search_read(
                    domain, search_result_fields, limit=limit)
        return search_results

    @api.model
    def name_search_custom(self, name='', field_name='', args=None, operator='ilike', model=None, limit=10, adv_fields='{}', search_fields='name'):
        table_head_main = [0, 'Name', 'adv_search_autocomplete_dropdown '+field_name,True]
        result = []
        search_result_fields = ['id', 'name']
        table_head = ""
        ar_open = '<a class="text-right">'
        ac_open = '<a class="text-center">'
        a_open = '<a>'
        a_close = "</a>"
        adv_fields = json.loads(adv_fields)
        # adv_fields = {"virtual_available":["Stock","r"],"uom_id":["Unit","l"],
        # "list_price":["Price","r"]}
        # adv_fields = '{"virtual_available":["Stock","r"],"uom_id":["Unit","l"]}'
        for field in adv_fields:
            len_advf_lst = len(adv_fields[field])
            if len_advf_lst == 2 and adv_fields[field][1] == "r":
                table_head += ar_open+adv_fields[field][0]+a_close
            elif len_advf_lst == 2 and adv_fields[field][1] == "c":
                table_head += ac_open+adv_fields[field][0]+a_close
            elif len_advf_lst == 0:
                table_head += ac_open+"head"+a_close
            else:
                table_head += a_open+adv_fields[field][0]+a_close

            search_result_fields.append(field)
        # result[0].append(table_head)
        table_head_main.append(table_head)
        domain = []
        if args:
            domain = [tuple(dom) if type(dom) is list else dom for dom in args]

        # search_keyword = name
        if search_fields == '':
            search_fields = 'name'
        search_on = search_fields.split(",")

        # print(search_on)

        search_results = self._adv_search_rec_get(
            model, domain, search_on, name, search_result_fields, limit+2)
        limit_count = 1
        for search_result in search_results:
            pro_details = []
            other_fields = ""

            # print('products',product)
            for fileld in search_result_fields:
                if fileld == 'id' or fileld == 'name':
                    pro_details.append(search_result[fileld])
                else:
                    # print(type(search_result[fileld]))
                    if type(search_result[fileld]) is str:
                        other_fields += a_open + \
                            str(search_result[fileld]) + a_close
                    elif type(search_result[fileld]) is tuple:
                        other_fields += a_open + \
                            str(search_result[fileld][1]) + a_close
                    elif type(search_result[fileld]) is list:
                        other_fields += a_open + \
                            ','.join(str(x)
                                     for x in search_result[fileld]) + a_close
                    elif type(search_result[fileld]) is float:
                        other_fields += ar_open + \
                            '{:.2f}'.format(search_result[fileld]) + a_close
                    else:
                        other_fields += a_open + \
                            str(search_result[fileld]) + a_close
            if limit_count > 1 and limit_count == limit:
                result.append(table_head_main)
            pro_details.append(
                'adv_search_autocomplete_dropdown '+field_name)
            pro_details.append(False)
            if other_fields:
                pro_details.append(other_fields)
            result.append(pro_details)
            limit_count += 1
        if limit_count > 1 and limit_count <= limit:
            result.append(table_head_main)
        #
        # print('result', result)
        # end = time.time()
        # print("time:",end - start)
        return result
