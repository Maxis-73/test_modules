# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShResUsers(models.Model):
    '''
    inherite the res.users 
    '''
    _inherit = "res.users"

    picking_ids = fields.Many2many(
        "stock.picking.type", string="Picking Types", copy=False
    )


    