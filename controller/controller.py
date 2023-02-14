from odoo import http
from odoo.http import request, content_disposition
import io
import xlsxwriter


class HotelReportExcel(http.Controller):
    @http.route([
        '/hotel/excel_report/<model("report.wizard"):report_id>',
    ], type='http', auth="user", csrf=False)
    def get_sale_excel_report(self, report_id=None,):
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition('Hotel_report' + '.xlsx'))
            ]
        )
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        # get data for the report.
        report_lines = report_id.get_report()
        sql_data = report_lines.get('sql_data')
        # print(sql_data)

        # prepare excel sheet styles and formats
        sheet = workbook.add_worksheet("invoices")
        sheet.write(1, 0, 'No.',)
        sheet.write(1, 1, 'Customer',)
        sheet.write(1, 2, 'Checkin date',)
        sheet.write(1, 3, 'Checkout date',)
        sheet.write(1, 4, 'State',)

        row = 2
        number = 1
        # write the report lines to the excel document
        for data in sql_data:
            sheet.set_row(row, 20)
            sheet.write(row, 0, number)
            sheet.write(row, 1, data['name'])
            sheet.write(row, 2, str(data['check_in']))
            sheet.write(row, 3, str(data['check_out']))
            sheet.write(row, 4, (data['state']))
            row += 1
            number += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return response
