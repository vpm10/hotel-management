from odoo import http
from odoo.http import request, content_disposition
import io
import xlsxwriter


class HotelReportExcel(http.Controller):
    @http.route([
        '/hotel/excel_report/<model("report.wizard"):report_id>',
    ], type='http', auth="user", csrf=False)
    def get_excel_report(self, report_id=None, ):
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition',
                 content_disposition('Hotel report' + '.xlsx'))
            ]
        )
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        # get data for the report.
        report_lines = report_id.get_report()
        sql_data = report_lines.get('sql_data')
        from_date = report_lines.get('from_date')
        to_date = report_lines.get('to_date')
        name = report_lines.get('name')
        # print(from_date)
        # print(to_date)
        # print(name)
        # prepare excel sheet styles and formats
        sheet = workbook.add_worksheet("hotel_report")
        sheet.write(0, 1, 'Hotel Management Report')
        if from_date:
            sheet.write(2, 1, 'Date from:-')
            sheet.write(2, 2, str(from_date))
        if to_date:
            sheet.write(3, 1, 'Date To:-')
            sheet.write(3, 2, str(to_date))
        if name:
            sheet.write(4, 1, 'Customer:-')
            sheet.write(4, 2, name)
        sheet.write(6, 0, 'No.', )
        sheet.write(6, 1, 'Customer', )
        sheet.write(6, 2, 'Checkin date', )
        sheet.write(6, 3, 'Checkout date', )
        sheet.write(6, 4, 'State', )

        row = 7
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
