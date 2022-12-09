# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta

from odoo import api, exceptions, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class AccountMoveLine(models.TransientModel):
    _name = "account.move.line.wizard"

    # Retorna el asiento actual
    def _default_move_id(self):
        return self.env['account.move'].browse(self._context.get('active_id'))

    @api.model
    def _get_currency(self):
        currency = False
        context = self._context or {}
        if context.get('default_journal_id', False):
            currency = self.env['account.journal'].browse(
                context['default_journal_id']).currency_id
        return currency

        # Declaración de campos
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

    lifetime = fields.Boolean('Tiempo de realización mayor a 12 meses',
                              help='Marcar esto en caso de que el activo tenga un tiempo de realización mayor a 12 meses, para excluirlo del activo corriente',
                              )


    @api.depends('account_id')
    def _compute_capital_change_type_relate(self):
        for each in self:
            if each.account_id and each.account_id.code.startswith('5'):
                each.capital_change_type_relate = True
                break
            else:
                each.capital_change_type_relate = True

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

