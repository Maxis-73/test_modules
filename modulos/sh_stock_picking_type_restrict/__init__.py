# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

'''
importing all folders having models 
'''
from . import models

def uninstall_hook(env):
    '''
    activate the rule if not 
    '''
    rule = env.ref("stock.stock_picking_type_rule", raise_if_not_found=False)
    if rule:
        rule.write({'active': True})
        