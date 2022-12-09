from odoo import fields, models


class SunatCatalog(models.Model):
    _name = 'sunat.chart'
    _description = 'SUNAT Catalog'

    code = fields.Char(string='Código')
    description = fields.Char(string='Descripción')


class SunatCatalog1(models.Model):
    _inherit = 'sunat.chart'
    _name = 'sunat.chart.1'
    _description = 'SUNAT Chart 1'
    _rec_name = 'description'


# class SunatCatalog5(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.5'
#     _description = 'SUNAT Chart 5'
#     _rec_name = 'description'


# class SunatCatalog6(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.6'
#     _description = 'SUNAT Chart 6'
#     _rec_name = 'description'


# class SunatCatalog7(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.7'
#     _description = 'SUNAT Chart 7'
#     _rec_name = 'description'


class SunatCatalog11(models.Model):
    _inherit = 'sunat.chart'
    _name = 'sunat.chart.11'
    _description = 'SUNAT Chart 11'
    _rec_name = 'description'


# class SunatCatalog14(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.14'
#     _description = 'SUNAT Chart 14'
#     _rec_name = 'description'


# class SunatCatalog16(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.16'
#     _description = 'SUNAT Chart 16'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'

# class SunatCatalog12(models.Model):
#     _inherit = 'sunat.chart'
#     _name = 'sunat.chart.12'
#     _description = 'SUNAT Chart 12'
#     _rec_name = 'description'
