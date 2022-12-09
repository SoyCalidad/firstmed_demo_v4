from odoo import fields, models, _
from odoo.http import request
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    share_link = fields.Char('Share Link', compute='_compute_share_link')

    def _compute_share_link(self):
        base_url = request.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        for move in self:
            move.share_link = base_url + move._get_share_url()


class AccountPayment(models.TransientModel):
    _inherit = 'account.payment.register'

    def action_create_payments(self):
        account_with_same_memos = False
        if self.communication:
            account_with_same_memos = self.env['account.payment'].search(
                [('ref', '=', self.communication), ('move_id', '!=', self._context['active_id'])])
        if account_with_same_memos:
            raise UserError(_('Ya hay un pago con el mismo memo.'))
        super().action_create_payments()


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        '''Verify if RUC has 11 digits or DNI 8 digits befores post the invoice'''
        for invoice in self:
            if invoice.partner_id.vat:
                if invoice.partner_id.country_id.code == 'PE':
                    if invoice.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code == '6':
                        if len(invoice.partner_id.vat) != 11:
                            raise UserError(
                                _('El RUC debe tener 11 dígitos.'))
                    elif invoice.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code == '1':
                        if len(invoice.partner_id.vat) != 8:
                            raise UserError(
                                _('El DNI debe tener 8 dígitos.'))
        return super().action_post()
