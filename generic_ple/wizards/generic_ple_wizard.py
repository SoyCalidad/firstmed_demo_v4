# -*- coding: utf-8 -*-

"""Método general que contiene las principales funciones para generar un reporte PLE
"""

import calendar
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError


class GenericPLE(models.TransientModel):
    _name = 'generic.ple'

    fiscal_year = fields.Integer(
        string='Año Fiscal', default=datetime.now().year, required=True)
    period = fields.Selection([
        ('01', 'Enero'),
        ('02', 'Febrero'),
        ('03', 'Marzo'),
        ('04', 'Abril'),
        ('05', 'Mayo'),
        ('06', 'Junio'),
        ('07', 'Julio'),
        ('08', 'Agosto'),
        ('09', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre')
    ], string='Periodo', required=True)


class PurchasePLE(models.TransientModel):
    _inherit = 'generic.ple'
    _name = 'purchase.ple'
    _description = 'Registro de compras PLE'

    
    def generate_ple_purchase(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary_text/purchase/saveas/%s/%s' % (str(self.fiscal_year), self.period),
            'target': 'self',
        }


class JournalPLE(models.TransientModel):
    _inherit = 'generic.ple'
    _name = 'journal.ple'
    _description = 'Libro Diario PLE'

    
    def generate_ple_journal(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary_text/journal/saveas/%s/%s' % (str(self.fiscal_year), self.period),
            'target': 'self',
        }


class GeneralPLE(models.TransientModel):
    _inherit = 'generic.ple'
    _name = 'general.ple'
    _description = 'Libro Mayor PLE'

    
    def generate_ple_general(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary_text/general/saveas/%s/%s'% (str(self.fiscal_year), self.period),
            'target': 'self',
        }

class AccountingPlanPLE(models.TransientModel):
    _inherit = 'generic.ple'
    _name = 'accounting.plan.ple'
    _description = 'Plan Contable Utilizado PLE'

    
    def generate_ple_accounting_plan(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary_text/accounting_plan/saveas/%s/%s'% (str(self.fiscal_year), self.period),
            'target': 'self',
        }
