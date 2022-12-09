from odoo import fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    def unlink(self):
        """When the record is deleted and is the last sequenced record the sequence is reduced by ONE"""
        for purchase in self:
            if purchase.sequence_id:
                if purchase.sequence_id.number_next_actual == purchase.sequence_id.number_next:
                    purchase.sequence_id.number_next_actual -= 1
        return super(PurchaseOrder, self).unlink()
        
        