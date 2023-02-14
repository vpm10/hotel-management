from odoo import fields, models


class ReportWizard(models.TransientModel):
    _name = 'report.wizard'

    date_from = fields.Datetime(string='From Date')
    date_to = fields.Datetime(string='To Date')
    guest_id = fields.Many2one('guest.details', String='Guest')

    # partner_id = fields.Many2one('res.partner', string='Guest', domain="[('id', '=', guest_id)]")

    def action_report(self):
        # print(self.guest_id.guest_id.name)
        query = """
        SELECT guest_details.check_in,guest_details.check_out,guest_details.state,res_partner.name
        FROM guest_details
        INNER JOIN res_partner
        ON res_partner.id = guest_details.guest_id where 1=1 """
        if self.date_from:
            query += """and guest_details.check_in >= '%s'""" % self.date_from
        if self.date_to:
            query += """and guest_details.check_out <= '%s'""" % self.date_to
        if self.guest_id.guest_id.name:
            query += """and res_partner.name = '%s'""" % self.guest_id.guest_id.name
        self._cr.execute(query)
        sql_dict = self._cr.dictfetchall()
        # print(sql_dict)

        data = {
            'model_id': self.id,
            'name': self.guest_id.guest_id.name,
            'to_date': self.date_to,
            'from_date': self.date_from,
            'sql_data': sql_dict
        }
        return self.env.ref(
            'hotel_room_management.hotel_report').report_action(None, data=data)

    def action_report_xlsx(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/hotel/excel_report/%s' % (self.id),
            'target': 'new',
        }
        # print('aa')

    def get_report(self):
        query = """
                SELECT guest_details.check_in,guest_details.check_out,guest_details.state,res_partner.name
                FROM guest_details
                INNER JOIN res_partner
                ON res_partner.id = guest_details.guest_id where 1=1 """
        if self.date_from:
            query += """and guest_details.check_in >= '%s'""" % self.date_from
        if self.date_to:
            query += """and guest_details.check_out <= '%s'""" % self.date_to
        if self.guest_id.guest_id.name:
            query += """and res_partner.name = '%s'""" % self.guest_id.guest_id.name
        self._cr.execute(query)
        sql_dict = self._cr.dictfetchall()
        # print(sql_dict)

        data = {
            'model_id': self.id,
            'name': self.guest_id.guest_id.name,
            'to_date': self.date_to,
            'from_date': self.date_from,
            'sql_data': sql_dict
        }
        return data
