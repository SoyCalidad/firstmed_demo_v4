import calendar
import os
import tempfile
from datetime import datetime

from odoo import http
from odoo.http import request
from odoo.tools import (DEFAULT_SERVER_DATE_FORMAT, float_compare,
                        float_is_zero)


class PLE(http.Controller):

    # @http.route('/web/binary_text/saveas', type='http', auth="user")
    @http.route(['/web/binary_text/purchase/saveas/<fiscal_year>/<period>',
                 ], type='http', auth="user", methods=['GET'], website=True)
    def purchase(self, req, **kwargs):
        fp = tempfile.TemporaryFile()

        int_period = int(kwargs.get('period'))
        fiscal_year = int(kwargs.get('fiscal_year'))
        days = calendar.monthrange(fiscal_year, int_period)
        date_from = datetime(fiscal_year, int_period, 1)
        date_to = datetime(fiscal_year, int_period, days[1])
        # Write data into your file respectively with your logic
        invoices = request.env['account.move'].search([
            ('date', '>=', date_from),
            ('date', '<=', date_to),
            ('move_type', 'in', ('out_invoice', 'out_refund')),
            ('state', '=', 'posted'),
        ], order='date asc')

        for invoice in invoices:
            ple = PurchasePLE(invoice)
            a = '|'.join(ple.clean_fields())
            fp.write(a.encode())

        fp.seek(0)
        file_data = fp.read()
        fp.close()

        company = invoices.env.user.company_id

        purchase_name = "LE%s%s%s0008010000%s%s%s1" % (
            company.partner_id.vat, fiscal_year, kwargs.get('period'), 1, 1, 1)

        return req.make_response(
            file_data, headers=[
                ('Content-Disposition', 'attachment; filename="%s.txt"' %
                 purchase_name),
                ('Content-Type', 'text/plain')
            ]
        )

    @http.route(['/web/binary_text/journal/saveas/<fiscal_year>/<period>',
                 ], type='http', auth="user", methods=['GET'], website=True)
    def journal(self, req, **kwargs):
        fp = tempfile.TemporaryFile()

        int_period = int(kwargs.get('period'))
        fiscal_year = int(kwargs.get('fiscal_year'))
        days = calendar.monthrange(fiscal_year, int_period)
        date_from = datetime(fiscal_year, int_period, 1)
        date_to = datetime(fiscal_year, int_period, days[1])
        # Write data into your file respectively with your logic
        moves = request.env['account.move'].search([
            ('date', '>=', date_from),
            ('date', '<=', date_to),
            ('state', '=', 'posted')
        ], order='date asc')

        for move in moves:
            for line in move.line_ids:
                ple = JournalPLE(line)
                a = ple.get_ple_row()
                fp.write(a.encode())

        fp.seek(0)
        file_data = fp.read()
        fp.close()

        company = moves.env.user.company_id

        journal_name = "LE%s%s%s0005010000%s%s%s1" % (
            company.partner_id.vat, fiscal_year, kwargs.get('period'), 1, 1, 1)

        return req.make_response(
            file_data, headers=[
                ('Content-Disposition', 'attachment; filename="%s.txt"' % journal_name),
                ('Content-Type', 'text/plain')
            ]
        )

    @http.route(['/web/binary_text/general/saveas/<fiscal_year>/<period>',
                 ], type='http', auth="user", methods=['GET'], website=True)
    def general(self, req, **kwargs):
        fp = tempfile.TemporaryFile()

        fiscal_year = int(kwargs.get('fiscal_year'))
        date_from = datetime(fiscal_year, 1, 1)
        date_to = datetime(fiscal_year, 12, 31)
        # Write data into your file respectively with your logic
        moves = request.env['account.move'].search([
            ('date', '>=', date_from),
            ('date', '<=', date_to),
            ('state', '=', 'posted')
        ], order='date asc')

        for move in moves:
            for line in move.line_ids:
                ple = JournalPLE(line)
                a = ple.get_ple_row()
                fp.write(a.encode())

        fp.seek(0)
        file_data = fp.read()
        fp.close()

        company = moves.env.user.company_id

        journal_name = "LE%s%s%s0006010000%s%s%s1" % (
            company.partner_id.vat, fiscal_year, kwargs.get('period'), 1, 1, 1)

        return req.make_response(
            file_data, headers=[
                ('Content-Disposition', 'attachment; filename="%s.txt"' % journal_name),
                ('Content-Type', 'text/plain')
            ]
        )

    @http.route(['/web/binary_text/accounting_plan/saveas/<fiscal_year>/<period>',
                 ], type='http', auth="user", methods=['GET'], website=True)
    def account_plan(self, req, **kwargs):
        fp = tempfile.TemporaryFile()
        int_period = int(kwargs.get('period'))
        fiscal_year = int(kwargs.get('fiscal_year'))
        # Write data into your file respectively with your logic
        accounts = request.env['account.account'].search([], order='code')

        for account in accounts:
            ple = AccountPlan(account)
            a = ple.get_ple_row()
            fp.write(a.encode())

        fp.seek(0)
        file_data = fp.read()
        fp.close()

        company = accounts.env.user.company_id

        journal_name = "LE%s%s%s0005030000%s%s%s1" % (
            company.partner_id.vat, fiscal_year, kwargs.get('period'), 1, 1, 1)

        return req.make_response(
            file_data, headers=[
                ('Content-Disposition', 'attachment; filename="%s.txt"' % journal_name),
                ('Content-Type', 'text/plain')
            ]
        )


class PurchasePLE(object):

    def __init__(self, invoice):
        self.C01 = sanitatize(self.get_C01(invoice))
        self.C02 = sanitatize(self.get_C02(invoice))
        self.C03 = sanitatize(self.get_C03(invoice))
        self.C04 = sanitatize(self.get_C04(invoice))
        self.C05 = sanitatize(self.get_C05(invoice))
        self.C06 = sanitatize(self.get_C06(invoice))
        self.C07 = sanitatize(self.get_C07(invoice))
        self.C08 = sanitatize(self.get_C08(invoice))
        self.C09 = sanitatize(self.get_C09(invoice))
        self.C10 = sanitatize(self.get_C10(invoice))
        self.C11 = sanitatize(self.get_C11(invoice))
        self.C12 = sanitatize(self.get_C12(invoice))
        self.C13 = sanitatize(self.get_C13(invoice))
        self.C14 = sanitatize(self.get_C14(invoice))
        self.C15 = sanitatize(self.get_C15(invoice))
        self.C16 = sanitatize(self.get_C16(invoice))
        self.C17 = sanitatize(self.get_C17(invoice))
        self.C18 = sanitatize(self.get_C18(invoice))
        self.C19 = sanitatize(self.get_C19(invoice))
        self.C20 = sanitatize(self.get_C20(invoice))
        self.C21 = sanitatize(self.get_C21(invoice))
        self.C22 = sanitatize(self.get_C22(invoice))
        self.C23 = sanitatize(self.get_C23(invoice))
        self.C24 = sanitatize(self.get_C24(invoice))
        self.C25 = sanitatize(self.get_C25(invoice))
        self.C26 = sanitatize(self.get_C26(invoice))
        self.C27 = sanitatize(self.get_C27(invoice))
        self.C28 = sanitatize(self.get_C28(invoice))
        self.C29 = sanitatize(self.get_C29(invoice))
        self.C30 = sanitatize(self.get_C30(invoice))
        self.C31 = sanitatize(self.get_C31(invoice))
        self.C32 = sanitatize(self.get_C32(invoice))
        self.C33 = sanitatize(self.get_C33(invoice))
        self.C34 = sanitatize(self.get_C34(invoice))
        self.C35 = sanitatize(self.get_C35(invoice))
        self.C36 = sanitatize(self.get_C36(invoice))
        self.C37 = sanitatize(self.get_C37(invoice))
        self.C38 = sanitatize(self.get_C38(invoice))
        self.C39 = sanitatize(self.get_C39(invoice))
        self.C40 = sanitatize(self.get_C40(invoice))
        self.C41 = sanitatize(self.get_C41(invoice))
        self.LS0 = os.linesep

    def get_C01(self, invoice):
        ''' Periodo
        1. Obligatorio
        2. Validar formato AAAAMM00
        3. 01 <= MM <= 12
        4. Menor o igual al periodo informado
        5. Si periodo es menor a periodo informado, entonces campo 41 es igual a '9' o '6' o '7'
        6. Si el periodo es igual a periodo informado, campo 41 es igual a '0' o '1' 
        '''
        res = ''
        res = invoice.invoice_date.strftime('%Y%m00') if invoice.invoice_date else ''
        return res

    def get_C02(self, invoice):
        ''' Número correlativo del mes o Código Único de la Operación (CUO)
        1. Obligatorio
        2. Si el campo 41 es igual a '0'', 1' o '6' o '7', consignar el Código Único de 
        la Operación (CUO) o número correlativo de la operación que se está informando
        3. Si el campo 41 es igual a '9', consignar el Código Único de la Operación 
        (CUO) o número correlativo de la operación original que se modifica
        4. No acepta el caracter "&"
        5. Si el CUO proviene de un asiento contable consolidado se debe adicionar 
        un número secuencial separado de un guión "-". 
        '''

        res = ''
        res = invoice.name[-2:] + invoice.invoice_date.strftime('%m') + str(1).rjust(4, '0')
        return res.zfill(4) or ''

    def get_C03(self, invoice):
        ''' CUO 
        1. Obligatorio
        2. El primer dígito debe ser: A, M o C
        3. En los casos de Contribuyentes del RER:Consignar M-RER.
        4. No acepta el caracter "&"
        '''
        move_type = 'M'
        if 'apertura' in invoice.name:
            move_type = 'A'
        res = ''
        res = move_type + str(invoice.id).zfill(4)
        return res or ''

    def get_C04(self, invoice):
        ''' Fecha de emisión del comprobante de pago o documento
        1. Obligatorio
        2. Menor o igual al periodo informado
        5. Si fecha de emisión está dentro de los doce meses anteriores al periodo señalado en el campo 1, entonces campo 41 = '6'
        6. Si fecha de emisión está fuera de los doce meses anteriores al periodo señalado en el campo 1, entonces campo 41 = '7'
        '''
        res = ''
        res = invoice.invoice_date.strftime('%d/%m/%Y') if invoice.invoice_date else ''
        return res

    def get_C05(self, invoice):
        ''' Fecha de Vencimiento o Fecha de Pago (1)
        1. Opcional, excepto cuando el campo 6 = '14' en cuyo caso es obligatorio
        2. Menor o igual al mes siguiente del periodo informado
        3. Menor o igual al mes siguiente del periodo señalado en el campo 1.
        '''
        res = ''
        res = invoice.invoice_date_due.strftime('%d/%m/%Y') if invoice.invoice_date_due else ''
        return res

    def get_C06(self, invoice):
        '''Tipo de Comprobante de Pago o Documento
        1. Obligatorio
        2. Validar con parámetro tabla 10
        3. No permite los tipos de comprobantes o documentos "91", "97" y "98"de la tabla 10
        '''
        res = ''
        res = invoice.l10n_latam_document_type_id.code if invoice.l10n_latam_document_type_id else '00'
        return res or ''

    def get_C07(self, invoice):
        ''' Serie del comprobante de pago o documento
        1. Optativo
        2. Aplicar Regla General (tipo y nro. doc.)
        '''
        serie, _ = invoice.name.split('-')
        res = serie
        return res or '00'

    def get_C08(self, invoice):
        ''' Año de emisión de la DUA o DSI
        1. Si campo 6 = '50' , '52' registrar número mayor a  1981 y menor o igual al año del 
        periodo informado o al año del periodo señalado en el campo 1.
        '''
        res = ''
        return res or ''

    def get_C09(self, invoice):
        ''' Número del comprobante de pago
        1. Obligatorio
        2. Aplicar Regla General (por tipo de doc.)
        '''
        _, numero = invoice.name.split('-')
        res = numero
        return res or '0000'

    def get_C10(self, invoice):
        ''' Importe total de las operaciones diarias que no otorguen derecho a crédito fiscal en forma consolidada
        1. Si campo 6 = '00','03','05','06','07','08','11','12','13','14','15','16','18','19','23','26','28','30',
        '34','35','36','37','55','56','87' y '88' y  campo 9 sea mayor o igual a cero 
        '''
        res = ''
        return res or ''

    def get_C11(self, invoice):
        '''Tipo de Documento de Identidad del proveedor
        1. Obligatorio, excepto cuando 
            a. campo 6 = '00','03','05','06','07','08','11','12','13','14','15','16','18','19','22','23','26','28',
            '30','34','35','36','37','55','56','87','88', '91', '97' y '98' o
            b. campo 6 = '07', '08', '87', '88', '97', '98' y campo 27 = '03', '12', '13', '14' y '36' 
            en cuyos casos será opcional
        2. Validar con parámetro tabla 2, no acepta el tipo de documento 0
        '''
        res = ''
        res = invoice.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code if invoice.partner_id and invoice.partner_id.l10n_latam_identification_type_id else ''
        return res or ''

    def get_C12(self, invoice):
        ''' Número de RUC del proveedor o número de documento de Identidad, según corresponda.
        1. Obligatorio, excepto cuando 
            a. campo 6 = '00','03','05','06','07','08','11','12','13','14','15','16','18','19','22','23','26','28',
            '30','34','35','36','37','55','56','87','88', '91', '97' y '98' o 
            b. campo 6 = '07', '08', '87', '88', '97', '98' y campo 27 = '03', '12', '13', '14' y '36' 
            en cuyos casos será opcional
        2. Aplicar Regla General (por tipo de doc.)
        '''
        res = ''
        res = invoice.partner_id.vat
        return res or ''

    def get_C13(self, invoice):
        ''' Apellidos y nombres, denominación o razón social  del proveedor
        1. Obligatorio, excepto cuando 
            a. campo 6 = '00','03','05','06','07','08','11','12','13','14','15','16','18','19',
            '22','23','26','28','30','34','35','36','37','55','56','87','88', '91', '97' y '98' o 
            b. campo 6 = '07', '08', '87', '88', '97', '98' y 
            campo 27 = '03', '12', '13', '14' y '36'
        '''
        res = ''
        res = invoice.partner_id.name[:100]
        return res or ''

    def get_C14(self, invoice):
        ''' Base imponible de las adquisiciones gravadas
        1. Acepta negativos
        '''
        res = ''
        multiplier = self._get_multiplier(invoice)
        res = "{0:.2f}".format(invoice.amount_untaxed*multiplier)
        return res or ''

    def get_C15(self, invoice):
        ''' 
        Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal
        1. Negativo si campo 14 es negativo
        2. Positivo si campo 14 es positivo
        3. Impuesto que corresponde a la adquisición registrada conforme lo dispuesto en el campo 14.
        '''
        res = ''
        multiplier = self._get_multiplier(invoice)
        res = "{0:.2f}".format(invoice.l10n_pe_edi_amount_igv*multiplier)
        return res or ''

    def get_C16(self, invoice):
        ''' Base imponible de las adquisiciones gravadas que dan derecho a crédito fiscal 
        y/o saldo a favor por exportación, destinadas a operaciones gravadas y/o de exportación y 
        a operaciones no gravadas
        1. Acepta negativos
        '''
        res = ''
        return res or ''

    def get_C17(self, invoice):
        ''' Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal
        1. Negativo si campo 16 es negtivo
        2. Positivo si campo 16 es positivo
        3. Impuesto que corresponde a la adquisición registrada conforme lo dispuesto en el campo 16.
        '''
        res = ''
        return res or ''

    def get_C18(self, invoice):
        ''' Base imponible de las adquisiciones gravadas que no dan derecho a crédito fiscal 
        y/o saldo a favor por exportación, por no estar destinadas a operaciones gravadas y/o 
        de exportación.
        1. Acepta negativos 
        '''
        res = ''
        return res or ''

    def get_C19(self, invoice):
        ''' Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal
        1. Acepta negativos 
        '''
        res = ''
        return res or ''

    def get_C20(self, invoice):
        ''' Valor de las adquisiciones no gravadas
        1. Acepta negativos
        '''
        res = ''
        return res or ''

    def get_C21(self, invoice):
        ''' Monto del Impuesto Selectivo al Consumo en los casos en que el sujeto pueda utilizarlo como deducción.
        1. Acepta negativos
        '''
        res = ''
        return res or ''

    def get_C22(self, invoice):
        ''' Otros conceptos, tributos y cargos que no formen parte de la base imponible.
        1. Acepta negativos
        '''
        res = ''
        return res or ''

    def get_C23(self, invoice):
        ''' Importe total de las adquisiciones registradas según comprobante de pago.
        1. Obligatorio
        2. Acepta negativos
        3. Suma de los campos 14 al 22
        '''
        res = ''
        multiplier = self._get_multiplier(invoice)
        res = "{0:.2f}".format(invoice.amount_total*multiplier)
        return res or ''

    def get_C24(self, invoice):
        ''' Código  de la Moneda (Tabla 4)
        1. Validar con parámetro tabla 4
        '''
        res = ''
        res = invoice.currency_id.name
        return res or ''

    def get_C25(self, invoice):
        ''' Tipo de cambio (3).
        '''
        res = ''
        currency_rate = invoice.env['res.currency.rate'].search([
            ('name', '<=', invoice.date),
            ('currency_id', '=', invoice.currency_id.id),
        ], order='name desc', limit=1)
        if currency_rate:
            res = "{0:.3f}".format(currency_rate.rate)
        else:
            res = "{0:.3f}".format(invoice.currency_id.rate)
        return res or ''

    def get_C26(self, invoice):
        ''' Fecha de emisión del comprobante de pago que se modifica (4).

        '''
        res = ''
        refund = invoice.reversed_entry_id
        if refund:
            res = refund.invoice_date.strftime('%d/%m/%Y')
        return res or ''

    def get_C27(self, invoice):
        ''' Tipo de comprobante de pago que se modifica (4).
        1. Obligatorio si campo 6 = '07' o '08' o '87' o '88' o '97' o '98'
        2. Validar con parámetro tabla 10
        '''
        res = ''
        refund = invoice.reversed_entry_id
        if refund:
            res = refund.l10n_latam_document_type_id.code or ''
        return res or ''

    def get_C28(self, invoice):
        ''' Número de serie del comprobante de pago que se modifica (4).
        1. Obligatorio si campo 6 = '07' o '08' o '87' o '88' o '97' o '98'
        2. Aplicar Regla General (por tipo de doc.)
        '''
        res = ''
        refund = invoice.reversed_entry_id
        if refund:
            refund_serie, _ = refund.name.split('-')
            res = refund_serie
        return res or '00'

    def get_C29(self, invoice):
        ''' Código de la dependencia Aduanera de la Declaración Única de Aduanas (DUA) o de la Declaración Simplificada de Importación (DSI) .
        1. Obligatorio si campo 27 = '50' , '52'. Validar con parámetro tabla 11
        '''
        res = ''
        return res or ''

    def get_C30(self, invoice):
        ''' Número del comprobante de pago que se modifica (4).
        1. Obligatorio si campo 6 = '07' o '08' o '87' o '88' o '97' o '98'
        '''
        res = ''
        refund = invoice.reversed_entry_id
        if refund:
            _, refund_number = refund.name.split('-')
            res = refund_number
        return res or ''

    def get_C31(self, invoice):
        ''' Fecha de emisión de la Constancia de Depósito de Detracción (6)
        1. Menor o igual al mes siguiente del periodo informado
        2. Menor o igual al mes siguiente del periodo señalado en el campo 1.
        '''
        res = ''
        return res or ''

    def get_C32(self, invoice):
        ''' Número de la Constancia de Depósito de Detracción (6)
        1. Positivo, de ser numérico
        '''
        res = ''
        return res or ''

    def get_C33(self, invoice):
        ''' Marca del comprobante de pago sujeto a retención
        1. Si identifica el comprobante sujeto a retención consignar '1' caso contrario no consignar nada
        '''
        res = ''
        return res or ''

    def get_C34(self, invoice):
        ''' Clasificación de los bienes y servicios adquiridos (Tabla 30) 
        Aplicable solo a los contribuyentes que hayan obtenido ingresos mayores a 1,500 UIT en el ejercicio anterior
        1. Validar con parámetro tabla 30
        '''
        res = ''
        return res or ''

    def get_C35(self, invoice):
        ''' Identificación del Contrato o del proyecto en el caso de los Operadores de las sociedades irregulares, 
        consorcios, joint ventures u otras formas de contratos de colaboración empresarial, 
        que no lleven contabilidad independiente.
        1. Uso exclusivo para los Operadores de las sociedades irregulares, consorcios, 
        joint ventures u otras formas de contratos de colaboración empresarial, que no 
        lleven contabilidad independiente. En este caso, deberán identificar cada contrato o proyecto.
        '''
        res = ''
        return res or ''

    def get_C36(self, invoice):
        ''' Error tipo 1: inconsistencia en el tipo de cambio
        1. El tipo de cambio (campo 25) correspondiente a la fecha de emisión (campo 4) debe ser 
        igual al tipo de cambio (campo 3) correspondiente a la fecha (campo 1) de la Estructura 1 
        Tipo de Cambio, del mismo periodo, caso contrario se debe consignar "1". Esto se aplica a 
        todos los tipos de comprobantes de pago, excepto el tipo 14 (tabla 10).
        2. El tipo de cambio (campo 25) correspondiente a la fecha de vencimiento (campo 5) debe ser igual 
        al tipo de cambio (campo 3) correspondiente a la fecha (campo 1) de la Estructura 1 Tipo de Cambio, 
        del mismo periodo, caso contrario se debe consignar "1". Esto se aplica sólo al tipo de comprobantes 
        de pago 14 (tabla 10).
        '''
        res = ''
        return res or ''

    def get_C37(self, invoice):
        ''' Error tipo 2: inconsistencia por proveedores no habidos
        '''
        res = ''
        return res or ''

    def get_C38(self, invoice):
        ''' Error tipo 3: inconsistencia por proveedores que renunciaron a la exoneración del Apéndice I del IGV
        '''
        res = ''
        return res or ''

    def get_C39(self, invoice):
        ''' Error tipo 4: inconsistencia por DNIs que fueron utilizados en las Liquidaciones de Compra y que ya cuentan con RUC
        '''
        res = ''
        return res or ''

    def get_C40(self, invoice):
        ''' Indicador de Comprobantes de pago cancelados con medios de pago
        '''
        res = ''
        return res or ''

    def get_C41(self, invoice):
        ''' Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a un ajuste.
        '''
        res = '1'
        return res or ''

    def is_rect(self, invoice):
        if invoice.origin:
            return True
        return False

    def get_orig(self, invoice):
        res = ''
        if self.is_rect(invoice):
            origin_invoice = invoice.env['account.move'].search(
                [('name', '=', invoice.origin)])
            return origin_invoice
        return res or ''

    def get_fields(self):
        res = list()
        for val in dir(self):
            if val.startswith('C'):
                res.append(str(getattr(self, val)))
        res.append(self.LS0)
        return res or ''

    def clean_fields(self):
        res = list()
        fields = self.get_fields()
        for field in fields:
            if not field:
                field = ''
            res.append(field)
        return res or ''
    
    def _get_multiplier(self, invoice):
        if invoice.state == 'cancel':
            multiplier = 0
        elif invoice.move_type == 'in_refund':
            multiplier = -1
        else:
            multiplier = 1
        return multiplier


class JournalPLE(object):
    '''Row implementation for Journal Book.'''

    def __init__(self, line):
        self.period = sanitatize(self.get_period(line)),
        self.unique_code_operation = sanitatize(
            self.get_unique_code_operation(line)),
        self.correlative_number = sanitatize(
            self.get_correlative_number(line)),
        self.move_account = sanitatize(self.get_move_account(line)),
        self.unit_code = sanitatize(self.get_unit_code(line)),
        self.center = sanitatize(sanitatize(self.get_center(line)),)
        self.type_currency = sanitatize(self.get_type_currency(line)),
        self.type_document = sanitatize(self.get_type_document(line)),
        self.number_document = sanitatize(self.get_number_document(line)),
        self.payment_document = sanitatize(self.get_payment_document(line)),
        self.voucher_serial_number = sanitatize(
            self.get_voucher_serial_number(line)),
        self.voucher_payment_number = sanitatize(
            self.get_voucher_payment_number(line)),
        self.accounting_date = sanitatize(self.get_accounting_date(line)),
        self.expiration_date = sanitatize(self.get_expiration_date(line)),
        self.operation_number = sanitatize(self.get_operation_number(line)),
        self.description = sanitatize(self.get_description(line)),
        self.referential_description = sanitatize(
            self.get_referential_description(line)),
        self.move_debit = sanitatize(self.get_move_debit(line)),
        self.move_credit = sanitatize(self.get_move_credit(line)),
        self.data = sanitatize(self.get_data(line)),
        self.operation_status = sanitatize(self.get_operation_status(line)),
        self.LS0 = os.linesep,

    def get_period(self, line):
        '''Periodo
        Formato: Numérico
        1. Obligatorio
        2. Validar formato AAAAMM00
        3. 01 <= MM <= 12
        4. Menor o igual al periodo informado
        5. Si el periodo es igual a periodo informado, 
        campo 21 es igual a '1' 
        6. Si periodo es menor a periodo informado,
        entonces campo 21 es diferente a '1'
        '''
        res = ''
        res = datetime.strptime(line.date,
                                DEFAULT_SERVER_DATE_FORMAT).strftime('%Y%m00')
        return res or ''

    def get_unique_code_operation(self, line):
        '''Código único de la operación
        Formato: Texto
        1. Obligatorio
        2. Si el campo 21 es igual a '1', consignar el Código Único de la Operación (CUO) 
        de la operación que se está informando
        3. Si el campo 21 es igual a '8', consignar el Código Único de la Operación (CUO)
        que corresponda al periodo en que se omitió la anotación. 
        Para modificaciones posteriores se hará referencia a este 
        Código Único de la Operación (CUO)
        4. Si el campo 21 es igual a '9', consignar el Código Único de la Operación (CUO) 
        de la operación original que se modifica
        '''
        # Whatever the field 21 is, this always return the correlative.
        correlative = str(line.move_id.id).zfill(4)
        return correlative

    def get_correlative_number(self, line):
        '''Número correlativo del asiento contable identificado en el campo 2. 
        Formato: Alfanumérico
        1. Obligatorio
        2. El primer dígito debe ser: A, M o C 
        '''
        move_type = "M"
        if 'apertura' in line.move_id.name:
            move_type = 'A'

        # if line.move_id.move_type == 'open':
        #     move_type = "A"
        # if line.move.move_type == 'close':
        #     move_type = "C"
        entry_corr = move_type + str(line.id).zfill(4)
        return entry_corr or 'M000'

    def get_move_account(self, line):
        '''Código de la cuenta contable desagregado en subcuentas
        al nivel máximo de dígitos utilizado,
        según la estructura 5.3 - Detalle del Plan Contable utilizado
        Formato: Numérico
        1. Obligatorio
        '''
        # The accounting plan is obtained in the accounts, then this
        # field has the internal values, and validation
        line_account_code = line.account_id.code.replace('.', '')
        return line_account_code

    def get_unit_code(self, line):
        '''Código de la Unidad de Operación, de la Unidad Económica
        Administrativa, de la Unidad de Negocio, de la Unidad de
        Producción, de la Línea, de la Concesión, del Local o del Lote, 
        de corresponder. 
        Formato: Alfanumérico
        '''
        return ''

    def get_center(self, line):
        '''Código del Centro de Costos, Centro de Utilidades
        o Centro de Inversión, de corresponder 
        Formato: Alfanumérico
        '''
        return ''

    def get_type_currency(self, line):
        '''Tipo de Moneda de origen
        Formato: Alfanumérico
        1. Obligatorio
        2. Validar con parámetro tabla 4
        '''
        # If are not origin invoice or document the currency
        # is the company currency by default
        res = line.currency_id.name
        return res or 'PEN'

    def get_type_document(self, line):
        '''Tipo de documento de identidad del emisor
        Formato: Alfanumérico
        1. Aplicar Regla general
        '''
        # If doesn't exist a origin document then this field hasn't a
        # value
        res = line.invoice_id.partner_id.catalog_06_id.code
        return res or '0'

    def get_number_document(self, line):
        '''numero de documento de identidad del emisor
        Formato: Alfanumérico
        1. Aplicar Regla general
        '''
        # If doesn't exist a origin document then this field hasn't a
        # value
        res = line.invoice_id.partner_id.vat
        return res or '00000000'

    def get_payment_document(self, line):
        '''Tipo de Comprobante de Pago o Documento asociada a la operación,
        de corresponder
        Formato: Numérico 
        1. Obligatorio
        2. Validar con parámetro tabla 10
        '''
        # If doesn't exist a origin document then this field are 00
        res = line.invoice_id.type_document_id.code
        return res or '00'

    def get_voucher_serial_number(self, line):
        '''Número de serie del comprobante de pago o documento 
        asociada a la operación, de corresponder
        Formato: Alfanumérico  
        1. Aplicar Regla General (tipo y nro. doc.)
        '''
        res = line.invoice_id.serie_id.name
        return res or '00'

    def get_voucher_payment_number(self, line):
        '''Número del comprobante de pago o documento asociada a la operación  
        Formato: Alfanumérico
        1. Obligatorio
        2. Aplicar Regla General (por tipo de doc.)
        '''
        # If doesn't exist a origin document then the value of this field is
        # 0000000
        res = line.invoice_id.numero
        return res or '00'

    def get_accounting_date(self, line):
        '''Fecha contable
        Formato: DD/MM/AAAA
        1. Menor o igual al periodo informado
        2. Menor o igual al periodo señalado en el campo 1.
        '''
        # All the moves have a date
        res = datetime.strptime(line.date,
                                DEFAULT_SERVER_DATE_FORMAT).strftime('%d/%m/%Y')
        return res

    def get_expiration_date(self, line):
        '''Fecha de vencimiento 
        Formato: DD/MM/AAAA
        '''
        return ''

    def get_operation_number(self, line):
        '''Fecha de la operación o emisión
        Formato: DD/MM/AAAA
        1. Obligatorio
        2. Menor o igual al periodo informado
        3. Menor o igual al periodo señalado en el campo 1.
        '''
        # If the move hasn't a origin document then the date
        # of the move are seted by default
        res = ''
        if line.invoice_id:
            res = datetime.strptime(line.invoice_id.date,
                                    DEFAULT_SERVER_DATE_FORMAT).strftime('%d/%m/%Y')
        else:
            res = datetime.strptime(line.date,
                                    DEFAULT_SERVER_DATE_FORMAT).strftime('%d/%m/%Y')
        return res

    def get_description(self, line):
        '''Glosa o descripción de la naturaleza de la operación registrada,
        de ser el caso.
        Formato: Texto
        1. Obligatorio
        '''
        # If the line hasn't a description the account name are seted by default
        res = line.name
        return res

    def get_referential_description(self, line):
        '''Glosa referencial, de ser el caso
        Formato: Texto
        '''
        return ''

    def get_move_debit(self, line):
        '''Movimientos del Debe
        Formato: Numérico
        1. Obligatorio
        2. Positivo o '0.00'
        3. Excluyente con campo 19
        4. Campo 18 y 19 pueden ser ambos 0.00
        5. La suma del campo 18 (correspondiente al Estado 1) 
        debe ser igual a la suma del campo 19
        '''
        res = '{0:.2f}'.format(abs(line.debit))
        return res

    def get_move_credit(self, line):
        '''Movimientos del Haber
        Formato: Numérico
        1. Obligatorio
        2. Positivo o '0.00'
        3. Excluyente con campo 18
        4. Campo 18 y 19 pueden ser ambos 0.00
        5. La suma del campo 18 (correspondiente al estado 1) 
        debe ser igual a la suma del campo 19.
        '''
        res = '{0:.2f}'.format(abs(line.credit))
        return res

    def get_data(self, line):
        '''
        Dato Estructurado: Código del libro, campo 1, campo 2 y 
        campo 3 del Registro de Ventas e Ingresos o del Registro de Compras, 
        separados con el carácter "&", de corresponder.
        Formato: Texto
        1. Obligatorio solo si el asiento contable en el Libro Diaro 
        no es consolidado, caso contrario no se consigna nada en este campo. 
        2. Código del Registro de Ventas e Ingresos: 140100
        3. Código del Registro de Compras: 080100 y 080200
        4. Validar estructuras de los campos 1, 2 y 3 del Registro de Ventas e
        Ingresos o del registro de Compras
        '''
        # Only for moves in purchase and sales books
        res = ''
        return res

    def get_operation_status(self, line):
        '''Indica el estado de la operación
        Formato: Numérico
        1. Obligatorio
        2. Registrar '1' cuando la operación corresponde al periodo.
        3. Registrar '8' cuando la operación corresponde a un periodo anterior
        y NO ha sido anotada en dicho periodo.
        4. Registrar '9' cuando la operación corresponde a un periodo anterior
        y SI ha sido anotada en dicho periodo.
        '''
        return '1'

    def get_ple_row(self):

        row_data = [
            'period',
            'unique_code_operation',
            'correlative_number',
            'move_account',
            'unit_code',
            'center',
            'type_currency',
            'type_document',
            'number_document',
            'payment_document',
            'voucher_serial_number',
            'voucher_payment_number',
            'accounting_date',
            'expiration_date',
            'operation_number',
            'description',
            'referential_description',
            'move_debit',
            'move_credit',
            'data',
            'operation_status',
            'LS0'
        ]
        data = list()
        for attr in row_data:
            info = getattr(self, attr)
            if info:
                data.append(info[0])
            else:
                data.append('')
        return '|'.join(data)


class AccountPlan(object):
    """Returns a clean list of the accounting plan."""

    def __init__(self, account):
        self.period = self.get_period(account)
        self.account_code = sanitatize(
            self.get_account_code(account)),
        self.account_description = sanitatize(
            self.get_account_description(account)),
        self.account_plan_code = sanitatize(
            self.get_account_plan_code(account)),
        self.account_plan_desc = sanitatize(
            self.get_account_plan_desc(account)),
        self.account_child_code = sanitatize(
            self.get_account_child_code(account)),
        self.account_child_desc = sanitatize(
            self.get_account_child_desc(account)),
        self.operation_status = sanitatize(
            self.get_operation_status(account)),
        self.LS0 = os.linesep,

    def get_period(self, account):
        '''Periodo
        Formato: Numérico
        1. Obligatorio
        2. Validar formato AAAAMMDD
        3. 01 <= MM <= 12
        4. Menor o igual al periodo informado
        5. Si el periodo es igual a periodo informado, campo 8 es igual a '1'.
        6. Si periodo es menor a periodo informado, entonces campo 8 es
        diferente a '1'
        '''
        dt = datetime.today()
        year = str(dt.year)
        month = '0' + str(dt.month) if dt.month < 10 else str(dt.month)
        # day = str(dt.day)
        period = year + month + '00'
        return period

    def get_account_code(self, account):
        '''Código de la Cuenta Contable desagregada hasta el nivel máximo de
        dígitos utilizado
        Formato: Numérico
        1. Obligatorio
        2. Desde tres dígitos hasta el nivel el nivel máximo de dígitos
        utilizado por cuenta contable.
        '''
        return account.code

    def get_account_description(self, account):
        '''Descripción de la Cuenta Contable desagregada al nivel máximo
        de dígitos utilizado
        Formato: Texto
        1. Obligatorio
        '''
        return account.name

    def get_account_plan_code(self, account):
        '''Código del Plan de Cuentas utilizado por el deudor tributario
        Formato: Numérico
        1. Obligatorio
        2. Validar con parámetro tabla 17
        '''
        return '01'

    def get_account_plan_desc(self, account):
        '''Descripción del Plan de Cuentas utilizado por el deudor tributario
        Formato: Texto
        1. Obligatorio si campo 4 = 99
        '''
        return 'PLAN CONTABLE GENERAL EMPRESARIAL'

    def get_account_child_code(self, account):
        '''Código de la Cuenta Contable Corporativa desagregada hasta el nivel
        máximo de dígitos utilizado, cuando deban consolidar sus estados
        financieros según la Superintendencia del Mercado de Valores o sean
        Sucursales de una empresa no domiciliada o pertenezca a un Grupo
        Económico que consolida los estados financieros.
        Formato: Numérico
        '''
        return ''

    def get_account_child_desc(self, account):
        '''Descripción de la Cuenta Contable Corporativa desagregada al nivel
        máximo de dígitos utilizado
        Formato: Texto
        1. Obligatorio si existe dato en el campo 6
        '''
        return ''

    def get_operation_status(self, account):
        '''Indica el estado de la operación
        Formato: Numérico
        1. Obligatorio
        2. Registrar '1' cuando la Cuenta Contable se informa en el periodo.
        3. Registrar '8' cuando la Cuenta Contable se debió informar en un
        periodo anterior y NO se informó en dicho periodo.
        4. Registrar '9' cuando la Cuenta Contable se informó en un periodo
        anterior y se desea corregir.
        '''
        return '1'

    def get_ple_row(self):

        row_data = [
            'period',
            'account_code',
            'account_description',
            'account_plan_code',
            'account_plan_desc',
            'account_child_code',
            'account_child_desc',
            'operation_status',
            'LS0',
        ]
        data = list()
        for attr in row_data:
            data.append(getattr(self, attr)[0])
        return '|'.join(data)


def sanitatize(value):
    if type(value) != str and value is not None:
        value = str(value)
        sanitatize(value)
    if value is None:
        value = ''
    value = value.strip()
    value = value.replace("\n", "")
    return value
