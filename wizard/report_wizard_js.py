import xlsxwriter
from odoo import fields, models
from odoo.tools import date_utils
import io
import json
from odoo.exceptions import ValidationError


class ExcelWizard(models.TransientModel):
    _name = "report.js"
    date_from = fields.Datetime(string='From Date')
    date_to = fields.Datetime(string='To Date')
    guest_id = fields.Many2one('guest.details', String='Guest')

    def print_xlsx(self):
        query = """SELECT guest_details.check_in,guest_details.check_out,
        guest_details.state,res_partner.name
        FROM guest_details
        INNER JOIN res_partner
        ON res_partner.id = guest_details.guest_id where 1=1 """
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise ValidationError('From date must be less than to date')
        if self.date_from:
            query += """and guest_details.check_in >= '%s'""" % self.date_from
        if self.date_to:
            query += """and guest_details.check_out <= '%s'""" % self.date_to
        if self.guest_id.guest_id.name:
            query += """and res_partner.name = '%s'""" % \
                     self.guest_id.guest_id.name
        self._cr.execute(query)
        sql_dict = self._cr.dictfetchall()
        # print(self.date_from)
        data = {
            'model_id': self.id,
            'name': self.guest_id.guest_id.name,
            'to_date': self.date_to,
            'from_date': self.date_from,
            'sql_data': sql_dict
        }
        # print(sql_dict)
        return {
                'type': 'ir.actions.report',
                'data': {'model': 'report.js',
                         'options': json.dumps(data,
                                               default=date_utils.
                                               json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Excel Report',
                         },
                'report_type': 'xlsx',
            }

    def get_xlsx_report(self, data, response):
        # print(data)
        from_date = data['from_date']
        to_date = data['to_date']
        customer = data['name']
        query = """
                    SELECT guest_details.check_in,guest_details.check_out,
                    guest_details.state,res_partner.name
                    FROM guest_details
                    INNER JOIN res_partner
                    ON res_partner.id = guest_details.guest_id where 1=1 """
        if from_date:
            query += """and guest_details.check_in >= '%s'""" % from_date
        if to_date:
            query += """and guest_details.check_out <= '%s'""" % to_date
        if customer:
            query += """and res_partner.name = '%s'""" % customer
        self._cr.execute(query)
        sql_dict = self._cr.dictfetchall()
        # print(sql_dict)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        sheet.write(8, 1, 'No.', )
        sheet.write(8, 2, 'Customer')
        sheet.write(8, 3, 'Checkin date')
        sheet.write(8, 4, 'Checkout date')
        sheet.write(8, 5, 'State')

        row = 9
        number = 1
        '''write the report lines to the excel document'''
        for sq in sql_dict:
            sheet.set_row(row, 20)
            sheet.write(row, 1, number)
            sheet.write(row, 2, sq['name'])
            sheet.write(row, 3, str(sq['check_in']))
            sheet.write(row, 4, str(sq['check_out']))
            sheet.write(row, 5, (sq['state']))
            row += 1
            number += 1
        cell_format = workbook.add_format(
           {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
           {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '13px', 'align': 'center'})
        sheet.merge_range('B2:I3', 'Hotel Room Management Report', head),
        if from_date:
            sheet.merge_range('A6:B6', 'From Date:', cell_format)
            sheet.merge_range('C6:E6', from_date, txt)
        if to_date:
            sheet.write('F6', 'To Date:', cell_format)
            sheet.merge_range('G6:I6', to_date, txt)
        if customer:
            sheet.merge_range('A7:B7', 'Guest', cell_format)
            sheet.merge_range('C7:E7', customer, txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
