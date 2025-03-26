# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
from odoo.osv import expression


class ShPickingTypeRestrict(models.Model):
    '''
    inherit stock.picking.type to access standard flow
    '''
    _inherit = "stock.picking.type"

    user_ids = fields.Many2many("res.users", string="Users", copy=False)



    @api.model
    def _search_display_name(self, operator, value):
    # Try to reverse the `display_name` structure
        
        domain = super()._search_display_name(operator, value)
        
        restricted_picking_type_code = self.env.context.get('restricted_picking_type_code')
        
        if self.env.user.has_group("sh_stock_picking_type_restrict.group_stock_picking_type_restrict_feature") and not self.env.user.has_group("base.group_erp_manager"):
            if restricted_picking_type_code:
                domain = expression.AND([[('code', '=', restricted_picking_type_code)], domain])

        else:
            if restricted_picking_type_code:
                domain = expression.AND([[('code', '=', restricted_picking_type_code)], domain])

        return domain



    @api.model
    def search(self, domain=None, offset=0, limit=None, order=None):
        '''
        To apply domain to load menu_________ 1
        '''
        if self.env.user.has_group(
            "sh_stock_picking_type_restrict.group_stock_picking_type_restrict_feature")  and not self.env.user.has_group("base.group_erp_manager"):
            if domain is None:
                domain = []

            domain += [
                ("user_ids", "in", self.env.user.id),
            ]
        
        return super().search(
            domain=domain,
            offset=offset,
            limit=limit,
            order=order,
        )
    

    @api.model
    def web_search_read(self, domain, specification, offset=0, limit=None, order=None, count_limit=None):
        if self.env.su:
            return super().web_search_read(domain, specification, offset=offset, limit=limit, order=order, count_limit=count_limit)

        if (
            self.env.user.has_group('sh_stock_picking_type_restrict.group_stock_picking_type_restrict_feature')
            and not self.env.user.has_group('base.group_erp_manager')
        ):
            restricted_picking_type_code = self.env.context.get('restricted_picking_type_code')
            
        
    
            if restricted_picking_type_code=="incoming":
              domain = expression.AND([[('code', '=',restricted_picking_type_code )], domain])
            elif restricted_picking_type_code=="outgoing":
              domain = expression.AND([[('code', '=',restricted_picking_type_code )], domain])
            elif restricted_picking_type_code=="internal":
              domain = expression.AND([[('code', '=',restricted_picking_type_code )], domain])
        else:
            restricted_picking_type_code = self.env.context.get('restricted_picking_type_code')
            
        
    
            if restricted_picking_type_code=="incoming":
              domain = expression.AND([[('code', '=',restricted_picking_type_code )], domain])
            elif restricted_picking_type_code=="outgoing":
              domain = expression.AND([[('code', '=',restricted_picking_type_code )], domain])
            elif restricted_picking_type_code=="internal":
              domain = expression.AND([[('code', '=',restricted_picking_type_code )], domain])

        return super().web_search_read(domain, specification, offset=offset, limit=limit, order=order, count_limit=count_limit)


    