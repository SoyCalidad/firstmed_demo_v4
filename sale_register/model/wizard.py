# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import base64
import calendar
from odoo.exceptions import UserError, ValidationError

class Year(models.Model):
    _name = 'date.year'

    name = fields.Char(string="Año", required=True)


class SaleRegisterWizard(models.TransientModel):
    _name = "wizard.sale.register"
    _description = "Registro de Ventas"

    def _default_month(self):
        return datetime.now().month

    def _default_year(self):
        return str(datetime.now().year)

    month = fields.Selection(string="Mes", selection=[
        ('1', 'ENERO'),
        ('2', 'FEBRERO'),
        ('3', 'MARZO'),
        ('4', 'ABRIL'),
        ('5', 'MAYO'),
        ('6', 'JUNIO'),
        ('7', 'JULIO'),
        ('8', 'AGOSTO'),
        ('9', 'SETIEMBRE'),
        ('10', 'OCTUBRE'),
        ('11', 'NOVIEMBRE'),
        ('12', 'DICIEMBRE')])
    year = fields.Char(
        string=u'Año',
        limit=4,
        default=_default_year,
        required=True,
    )
    company_id = fields.Many2one(
        string=u'Compañia',
        comodel_name='res.company', required=True,
        domain=lambda self: [('id', 'in', self.env.user.company_ids.ids)],
        default=lambda self: self.env.user.company_id.id,
    )

    # my_file = fields.Binary('File data', readonly=True, help='File(jpg, csv, xls, exe, any binary or text format)')
    ventas_reg = fields.Binary('File', readonly=True)
    ventas_reg_fname = fields.Char('Filename', readonly=True)

    journal_ids = fields.Many2many('account.journal', string='Diarios', domain="[('type','=','sale')]")

    def get_report(self):
        """Call when button 'Get Report' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'month': dict(self._fields['month'].selection).get(self.month),
                'year': self.year,
            },
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `get_report_values()` and pass `data` automatically.
        return self.env.ref('sale_register.sale_register').report_action(self, data=data)

    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['form'] = self.read()[0]

        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]

        if context.get('xls_export'):
            return self.env.ref('sale_register.sale_register_xls1').report_action(self, data=datas)

    def generate_txt_report(self):
        data = self.read()[0]
        month = data['month']
        year = data['year']
        company = data['company_id'][1]
        journal_ids = data['journal_ids']

        company = self.env['res.company'].search([('id', '=', data['company_id'][0])])


        # report_name = 'Registro de ventas PLE'
        # company = self[0].env.user.company_id
        mont_02 = str(int(month)).rjust(2, '0')
        filename = 'LE%s%s%s%s0100001111.txt' % (
            str(company.vat), str(year), mont_02, '0014')

        lines = []
        month = int(month)
        year = int(year)
        days = calendar.monthrange(year, month)
        init_date = datetime(year, month, 1)
        end_date = datetime(year, month, days[1])
        invoices = self.env['account.move'].search([
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('invoice_date', '>=', init_date),
            ('invoice_date', '<=', end_date),
            ('state', '=', 'posted'),
            ('company_id', '=', company.id),
            ('journal_id', 'in', journal_ids),
        ], order="invoice_date asc")
        # for invoice in invoices:
        #     date_m = datetime.strptime(
        #         invoice.date, '%Y-%m-%d').strftime('%m')
        #     date_y = datetime.strptime(
        #         invoice.date, '%Y-%m-%d').strftime('%Y')
        #     if int(date_m) == int(month) and date_y == year[1]:
        #         lines.append(invoice)
        lines = sorted(invoices, key=lambda x: str(x['name']))

        year = str(year)
        
        periodo_ple = year + mont_02 + '00'
        w_data = ""
        index = 1
        T10 = ['', 'FT', 'RH', 'BV', 'LQ', 'BA', 'CP', 'NA', 'ND', 'GS',
               'RA', 'PB', 'TK', 'LB', 'RC', '', '', '', '', '',
               '', '', '', '', '', '', '', '', '', '',
               '', '', '', '', '', '', '', '', '', '',
               '', '', '', '', '', '', '', '', '', '',
               'RL', '', '', '', '', '', '', '', '', '']
        for each in lines:
            w_data = w_data + periodo_ple + '|'
            cuo = each.name[-2:] + mont_02 + str(index).rjust(4, '0')
            w_data = w_data + cuo + '|'
            w_data = w_data + 'M001' + '|'
            # w_data = w_data + '04-' + str(int(month)).rjust(2, '0') + str(index).rjust(4, '0') + '|'
            # w_data = w_data + 'M0001' + '|'
            currency_rate = each.env['res.currency.rate'].search([
                ('name', '<=', each.date),
                ('currency_id', '=', each.currency_id.id),
            ], order='name desc', limit=1)
            res = ''
            refund_date = ''
            refund_document_type_code = ''
            refund_number = ''
            refund_serie = ''
            partner_name = each.partner_id.name if each.state == 'posted' else 'COMPROBANTE ANULADO'
            # partner_identification_type = each.partner_id.l10n_latam_identification_type_id.code if each.state == 'posted' else '0'
            partner_identification_type = each.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code or ''
            partner_vat = each.partner_id.vat if each.state == 'posted' else '00000000'
            if not partner_vat:
                partner_vat = '00000000'
            if currency_rate:
                res = "{0:.3f}".format(currency_rate.rate)
            else:
                res = "{0:.3f}".format(each.currency_id.rate)

            try:
                serie, numero = each.name.split('-')
            except:
                serie = numero = '-'

            refund = each.reversed_entry_id
            if refund:
                refund_date = refund.invoice_date.strftime(
                    '%d/%m/%Y') if refund.invoice_date else ''
                # 'refund.type_document_id.code'
                refund_document_type_code = refund.l10n_latam_document_type_id.code or ''
                try:
                    refund_serie, refund_number = refund.name.split('-')
                except:
                    refund_serie = refund_number = '-'
            
            if each.state == 'cancel':
                multiplier = 0
            elif each.move_type == 'out_refund':
                multiplier = -1
            else:
                multiplier = 1

            amount_untaxed = each.amount_untaxed * multiplier
            l10n_pe_edi_amount_isc = each.l10n_pe_edi_amount_isc * multiplier
            l10n_pe_edi_amount_igv = each.l10n_pe_edi_amount_igv * multiplier
            amount_total = each.amount_total * multiplier
            l10n_pe_edi_amount_discount = each.l10n_pe_edi_amount_discount * multiplier
            l10n_pe_edi_amount_exonerated = each.l10n_pe_edi_amount_exonerated * multiplier
            l10n_pe_edi_amount_unaffected = each.l10n_pe_edi_amount_unaffected * multiplier
            
            invoice_date = each.invoice_date.strftime(
                '%d/%m/%Y') if each.invoice_date else ''
            invoice_date_due = each.invoice_date_due.strftime(
                '%d/%m/%Y') if each.invoice_date_due else ''
                
            if each.invoice_date:
                w_data = w_data + invoice_date + '|'
            if each.invoice_date_due:
                w_data = w_data + '|'
            else:
                w_data = w_data + '01/01/0001' + '|'

            w_data = w_data + \
                str(int(each.l10n_latam_document_type_id.code)).rjust(2, '0') + '|'
            w_data = w_data + serie + '|'
            w_data = w_data + str(numero) + '|'
            w_data = w_data + '|'
            w_data = w_data + partner_identification_type + '|'
            w_data = w_data + str(partner_vat) + '|'
            w_data = w_data + partner_name + '|'
            w_data = w_data + '0.00' + '|'
            w_data = w_data + "{0:.2f}".format(amount_untaxed) + '|' # Base imponible de la operación gravada (4)
            w_data = w_data + "{0:.2f}".format(l10n_pe_edi_amount_discount) + '|' # Descuento de la Base Imponible
            w_data = w_data + "{0:.2f}".format(l10n_pe_edi_amount_igv) + '|' # Impuesto General a las Ventas y/o Impuesto de Promoción Municipal
            w_data = w_data + '0.00' + '|' # Descuento del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal
            w_data = w_data + "{0:.2f}".format(l10n_pe_edi_amount_exonerated) + '|' # Importe total de la operación exonerada
            w_data = w_data + "{0:.2f}".format(l10n_pe_edi_amount_unaffected) + '|' # Importe total de la operación inafecta 
            w_data = w_data + "{0:.2f}".format(l10n_pe_edi_amount_isc) + '|' # Impuesto Selectivo al Consumo, de ser el caso.
            w_data = w_data + '0.00' + '|' # Base imponible de la operación gravada con el Impuesto a las Ventas del Arroz Pilado
            w_data = w_data + '0.00' + '|' # Impuesto a las Ventas del Arroz Pilado 
            w_data = w_data + '0.00' + '|' # Otros conceptos, tributos y cargos que no forman parte de la base imponible
            w_data = w_data + '0.00' + '|' # ICEBPER
            w_data = w_data + "{0:.2f}".format(amount_total) + '|' # Importe total del comprobante de pago
            w_data = w_data + each.currency_id.name + '|' # Código  de la Moneda (Tabla 4)
            w_data = w_data + "{0:.3f}".format(each.currency_id.rate) + '|' # Tipo de cambio (5)
            w_data = w_data + refund_date + '|' # Fecha de emisión del comprobante de pago o documento original que se modifica (6) o documento referencial al documento que sustenta el crédito fiscal
            w_data = w_data + refund_document_type_code + '|' # Tipo del comprobante de pago que se modifica (6)
            w_data = w_data + refund_serie + '|' # Número de serie del comprobante de pago que se modifica (6) o Código de la Dependencia Aduanera
            w_data = w_data + refund_number + '|' # Número del comprobante de pago que se modifica (6) o Número de la DUA, de corresponder
            w_data = w_data + '|' # Identificación del Contrato o del proyecto en el caso de los Operadores de las sociedades irregulares, consorcios, joint ventures u otras formas de contratos de colaboración empresarial, que no lleven contabilidad independiente.
            w_data = w_data + '|' # Error tipo 1: inconsistencia en el tipo de cambio
            w_data = w_data + '|' # Indicador de Comprobantes de pago cancelados con medios de pago
            w_data = w_data + '1' + '|' # Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a alguna de las situaciones previstas en el inciso e) del artículo 8° de la Resolución de Superintendencia N.° 286-2009/SUNAT
            w_data = w_data + '\n'
            index += 1

        out = base64.encodestring(str.encode(w_data))
        self.write({'ventas_reg': out, 'ventas_reg_fname': filename})
        print("----->", filename, out)
        # path_file_not = os.path.join(my_path,path_file_not)
        return {
            # 'type': 'ir.actions.act_url',
            # 'target': 'new',
            # 'url': 'web/content/?model='+self._name+'&id='+str(self.id)+'&field=datas&download=true&filename='+filename,
            # 'url': '/web/binary/download_document?model=%s&field=datas&id=%s&filename=%s'%(self._name,self.id,filename),

            'name': filename,
            'res_id': self.id,
            'res_model': self._name,
            'target': 'new',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref('sale_register.save_file_wizard_view_done').id,
            'view_mode': 'form',
            'view_type': 'form',
        }


class SaleRegister(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """
    _name = 'report.sale.report_view'

    @api.model
    def get_report_values(self, docids, data=None):
        month = data['form']['month']
        year = data['form']['year']

        docs = []
        invoices = self.env['account.move'].search(
            [], order='date asc')
        # print("----> months", docs)
        # docs = sorted(docs, key=lambda x: x['date'])
        # invoices = invoices.search([('date.month','=',int(month))])
        for invoice in invoices:
            values = {
                'partner': invoice.partner_id.name,
                'date': invoice.date,
                'number': invoice.number,
                'user': invoice.user_id.name,
                'total1': invoice.amount_total_signed,
                'total': invoice.amount_total_signed,
                'residual': invoice.amount_residual_signed,
            }
            docs.append(values)
        docs = sorted(docs, key=lambda x: x['date'])

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'month': str(month),
            'year': str(year),
            'docs': docs,
        }
