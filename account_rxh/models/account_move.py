from odoo import api, fields, models

class L10nLatamDocumentType(models.Model):

    _inherit = 'l10n_latam.document.type'

    internal_type = fields.Selection(
        selection_add=[
            ('rxh', 'Recibo por honorarios'),])
