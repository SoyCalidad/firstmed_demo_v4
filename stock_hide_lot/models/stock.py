# Copyright 2022 Luis Vargas - Soy Calidad
# License Other proprietary (https://www.soycalidad.com/soy-calidad-terms-of-service/).

from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    product_qty = fields.Float('Quantity', compute='_product_qty', store=True)