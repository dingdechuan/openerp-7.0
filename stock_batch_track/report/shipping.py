# -*- encoding: utf-8 -*-
# © 2014 Elico corp(www.elico-corp.com)
# Licence AGPL-3.0 or later(http://www.gnu.org/licenses/agpl.html)


import time
from report import report_sxw
from lxml import etree
import pooler
from osv import osv,fields
from tools.translate import _

class shipping(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(shipping, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            '_add_header':self._add_header,
            'get_partner_ref':self.get_partner_ref,
            'tag':self.tag
        })
        
    def get_partner_ref(self, partner, product):
        result =''
        ref_obj=self.pool.get('product.partner.related.fields')
        ref_obj_ids=ref_obj.search(self.cr, self.uid, [('partner_id', '=', partner),('product_id', '=',product)])
        for ref_obj_id in ref_obj.browse(self.cr, self.uid, ref_obj_ids):
            result= ref_obj_id.name + " " + ref_obj_id.value
        return result
    
    def _add_header(self, rml_dom, header='external'):
        if header=='internal':
            rml_head =  self.rml_header2
        elif header=='internal landscape':
            rml_head =  self.rml_header3
        elif header=='external':
            rml_head =  self.rml_header
        else:
            header_obj= self.pool.get('res.header')
            rml_head_id = header_obj.search(self.cr,self.uid,[('name','=',header)])
            if rml_head_id:
                rml_head = header_obj.browse(self.cr, self.uid, rml_head_id[0]).rml_header
        try:
            head_dom = etree.XML(rml_head)
        except:
            raise osv.except_osv(_('Error in report header''s name !'), _('No proper report''s header defined for the selected report. Check that the report header defined in your report rml_parse line exist in Administration/reporting/Reporting headers.' ))
            
        for tag in head_dom:
            found = rml_dom.find('.//'+tag.tag)
            if found is not None and len(found):
                if tag.get('position'):
                    found.append(tag)
                else :
                    found.getparent().replace(found,tag)
        return True

report_sxw.report_sxw('report.shipping.to.subcontractor', 'stock.tracking', 'addons/stock_batch_track/report/shipping.rml', parser=shipping, header="external landscape")

