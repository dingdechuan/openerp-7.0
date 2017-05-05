# -*- coding: utf-8 -*-
# © 2014 Elico corp(www.elico-corp.com)
# Licence AGPL-3.0 or later(http://www.gnu.org/licenses/agpl.html)


from openerp.osv import fields, osv


class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    _name = 'sale.order.line'

    def _get_pdt_code(self, cr, uid, ids, field, arg=None, context=None):
        res = {}
        for line in self.browse(cr, uid, ids):
            res[line.id] = line.product_id.default_code
        return res

    def _get_pdt_mmx_type(self, cr, uid, ids, field, arg=None, context=None):
        res = {}
        dic = dict(
            self.pool.get('product.product')._columns['mmx_type'].selection
        )
        for line in self.browse(cr, uid, ids):
            res[line.id] = dic[line.product_id.mmx_type]
        return res

    _columns = {
        'qty_store': fields.float('QTY store',help='Want you look this field,Pls first run xxxx wizard'),
        'product_default_code': fields.function(_get_pdt_code,
                                                arg=None,
                                                string='Product Code',
                                                type='char',
                                                size=32,
                                                readonly=True,
                                                store=True),
        'product_mmx_type': fields.function(_get_pdt_mmx_type,
                                            arg=None,
                                            string='Product Type',
                                            type='char',
                                            size=32,
                                            readonly=True,
                                            store=True),
        'qty_available': fields.related('product_id', 'qty_available', type='float', string='Quantity On Hand',),
        'virtual_available': fields.related('product_id', 'virtual_available', type='float', string='Forecasted Quantity',),
       
    }
    _sql_constraints = [
        ('product_uom_qty_check',
         'CHECK( product_uom_qty >= 0 )',
         'Sale Qty must be greater than zero.'),
    ]

    def link_to_order(self, cr, uid, ids, context=None):
        sol = self.browse(cr, uid, ids[0])
        so_id = sol.order_id.id
        return {
            'name': 'Order info',
            'target': "new",
            'view_type': 'form',
            "view_mode": 'form',
            'res_model': 'sale.order',
            'res_id': so_id,
            'type': 'ir.actions.act_window',
        }

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
                          uom=False, qty_uos=0, uos=False, name='',
                          partner_id=False, lang=False, update_tax=True,
                          date_order=False, packaging=False,
                          fiscal_position=False, flag=False, context=None):
        """
        if product sale_line_warn is set no-message,
        don't pop any warning
        """
        res = super(sale_order_line, self).product_id_change(
            cr, uid, ids, pricelist, product, qty=qty, uom=uom,
            qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order,
            packaging=packaging, fiscal_position=fiscal_position, flag=flag,
            context=context)
        if product:
            pdt = self.pool.get('product.product').browse(cr, uid, product)
            # if only to cancel the quantity  warning
            if pdt.sale_line_warn == 'no-message':
                res['warning'] = None
        return res

sale_order_line()


