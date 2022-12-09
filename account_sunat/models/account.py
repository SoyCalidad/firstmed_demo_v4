from odoo import models, fields, api, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class Account(models.Model):
    _inherit = 'account.account'

    reference1 = fields.Boolean(string='Documento de Referencia')
    reference2 = fields.Boolean(string='Documento de Referencia 2')
    area = fields.Boolean(string='Área')
    adjust_account = fields.Boolean(string='Cuenta de Ajuste')
    bank_concilation = fields.Boolean(string='Conciliar Bancos')
    payment_document_type = fields.Boolean(string='Tipo de Documento de Pago')
    category_id = fields.Many2one('account.account.category', 'Clasificación')
    account_related_credit_id = fields.Many2one('account.account', string='Cuenta de amarre (Debit)')
    account_related_debit_id = fields.Many2one('account.account', string='Cuenta de amarre (Haber)')


class AccountCategory(models.Model):
    _name = 'account.account.category'

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')
    active = fields.Boolean(string='Activo')
    account_ids = fields.One2many(
        'account.account', 'category_id', string='Cuenta Contable')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    lifetime = fields.Boolean('Tiempo de realización mayor a 12 meses',
                              help='Marcar esto en caso de que el activo tenga un tiempo de realización mayor a 12 meses, para excluirlo del activo corriente')

    reference1 = fields.Char(string='Documento de Referencia')
    has_reference1 = fields.Boolean(
        compute='_compute_has_reference1', string='Tiene Documento de Referencia?')
    reference2 = fields.Char(string='Documento de Referencia 2')
    has_reference2 = fields.Boolean(
        compute='_compute_has_reference2', string='Tiene Documento de Referencia?')
    area = fields.Char(string='Área')
    has_area = fields.Boolean(
        compute='_compute_has_area', string='Tiene Área?')
    adjust_account = fields.Many2one(
        'account.account', string='Cuenta de Ajuste')
    has_adjust_account = fields.Boolean(
        compute='_compute_has_adjust_account', string='Tiene Cuenta de Ajuste?')

    payment_document_type = fields.Many2one(
        'einvoice.catalog.01', string='Tipo de Documento de Pago')
    has_payment_document_type = fields.Boolean(
        compute='_compute_has_payment_document_type', string='Tiene Documento de Pago?')

    # cost_center = fields.Many2one('account.cost.center', 'Centro de Costos')
    capital_change_type = fields.Selection([
        ('1', 'Efecto acumulado de los cambios en las políticas contables y la corrección de errores sustanciales'),
        ('2', 'Distribuciones o asignaciones de utilidades efectuadas en el período'),
        ('3', 'Dividendos y participaciones acordados durante el período'),
        ('4', 'Nuevos aportes de accionistas'),
        ('5', 'Movimiento de prima en la colocación de aportes y donaciones'),
        ('6', 'Incrementos o disminuciones por fusiones o escisiones'),
        ('7', 'Revaluación de activos'),
        ('8', 'Capitalización de partidas patrimoniales'),
        ('9', 'Redención de Acciones de Inversión o reducción de capital'),
        ('10', 'Utilidad (pérdida) Neta del ejercicio'),
        ('11', 'Otros incrementos o disminuciones de las partidas patrimoniales')], string='Razón de Cambio de Patrimonio')

    capital_change_type_relate = fields.Boolean(
        compute='_compute_capital_change_type_relate', string='Es cuenta 50?')

    @api.depends('account_id')
    def _compute_capital_change_type_relate(self):
        for each in self:
            if each.account_id and each.account_id.code.startswith('5'):
                each.capital_change_type_relate = True
                break
            else:
                each.capital_change_type_relate = False

    @api.depends('account_id')
    def _compute_has_reference1(self):
        for each in self:
            if each.account_id.reference1:
                each.has_reference1 = True
            else:
                each.has_reference1 = False

    @api.depends('account_id')
    def _compute_has_reference2(self):
        for each in self:
            if each.account_id.reference2:
                each.has_reference2 = True
            else:
                each.has_reference2 = False

    @api.depends('account_id')
    def _compute_has_area(self):
        for each in self:
            if each.account_id.area:
                each.has_area = True
            else:
                each.has_area = False

    @api.depends('account_id')
    def _compute_has_adjust_account(self):
        for each in self:
            if each.account_id.adjust_account:
                each.has_adjust_account = True
            else:
                each.has_adjust_account = False

    @api.depends('account_id')
    def _compute_has_payment_document_type(self):
        for each in self:
            if each.account_id.payment_document_type:
                each.has_payment_document_type = True
            else:
                each.has_payment_document_type = False

    def open_extra_data_form_view(self):
        return {
            'res_model': 'account.move.line',
            'type': 'ir.actions.act_window',
            'context': {},
            'view_mode': 'form',
            'view_id': self.env.ref("account_sunat.account_move_line_extra_data_view_form"),
            'target': 'new'
        }
    
    def open_to_form_view(self):

        view_id = self.env.ref('account_sunat.view_move_line_form').id

        context = self._context.copy()

        return {
            'name': 'Linea de Asiento',
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(view_id, 'form')],
            'res_model': 'account.move.line',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
            'context': context,
        }


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"
    _description = "Bank Statement"

    payment_method = fields.Many2one('sunat.chart.1', string='Medio de Pago')


class AccountInvoice(models.Model):
    _inherit = "account.move"

    dua_year = fields.Char(string='Año de emisión de la DUA o DSI')
    customs_dependency = fields.Many2one(
        'sunat.chart.11', string='Dependencia ADUANERA')

    # def post(self):
    #     self.post_assert_balanced()
    #     invoice = self._context.get('invoice', False)
    #     self._post_validate()
    #     # Create the analytic lines in batch is faster as it leads to less cache invalidation.
    #     self.mapped('line_ids').create_analytic_lines()
    #     for move in self:
    #         if move.name == '/':
    #             new_name = False
    #             journal = move.journal_id

    #             if invoice and invoice.move_name and invoice.move_name != '/':
    #                 new_name = invoice.move_name
    #             else:
    #                 if journal.sequence_id:
    #                     # If invoice is actually refund and journal has a refund_sequence then use that one or use the regular one
    #                     sequence = journal.sequence_id
    #                     if invoice and invoice.type in ['out_refund', 'in_refund'] and journal.refund_sequence:
    #                         if not journal.refund_sequence_id:
    #                             raise UserError(
    #                                 _('Please define a sequence for the credit notes'))
    #                         sequence = journal.refund_sequence_id

    #                     new_name = sequence.with_context(
    #                         ir_sequence_date=move.date).next_by_id()
    #                 else:
    #                     raise UserError(
    #                         _('Please define a sequence on the journal.'))

    #             if new_name:
    #                 move.name = new_name
    #     return self.write({'state': 'posted'})

    
    # def assert_balanced(self):
    #     return True

    
    # def post_assert_balanced(self):
    #     if not self.ids:
    #         return True
    #     prec = self.env['decimal.precision'].precision_get('Account')

    #     self._cr.execute("""\
    #         SELECT      move_id
    #         FROM        account_move_line
    #         WHERE       move_id in %s
    #         GROUP BY    move_id
    #         HAVING      abs(sum(debit) - sum(credit)) > %s
    #         """, (tuple(self.ids), 10 ** (-max(5, prec))))
    #     if len(self._cr.fetchall()) != 0:
    #         raise UserError(_("Cannot create unbalanced journal entry."))
    #     return True
