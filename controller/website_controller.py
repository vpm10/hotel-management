import base64
from odoo import http
from odoo.http import request, Controller


class WebsiteForm(Controller):
    @http.route(['/rooms'], type='http', auth="user", website=True)
    def room(self):
        rooms = request.env['hotel.room'].sudo().search([
            ('state', '=', 'available')])
        partner_id = request.env['res.partner'].sudo().search([])
        values = {}
        values.update({
            'rooms': rooms,
            'guests': partner_id,
        })
        return request.render("hotel_room_management.room_booking_form",
                              values)

    @http.route(['/rooms/submit'], type='http', auth="user", website=True)
    def submit(self, **kwargs):
        guest_detail = {
            'bed': kwargs.get('rooms'),
            'guest_id': kwargs.get('guest_id'),
            'expected_days': kwargs.get('days'),
            'number_of_guests': kwargs.get('persons'),
        }
        request.env['guest.details'].sudo().create(guest_detail)
        details = request.env['guest.details'].sudo().search([])[-1]
        file_name = kwargs.get('attachments').filename
        file = kwargs.get('attachments')
        request.env['ir.attachment'].sudo().create({
            'name': file_name,
            'type': 'binary',
            'datas': base64.b64encode(file.read()),
            'res_model': 'guest.details',
            'res_id': details.id
        })
        return request.render("hotel_room_management.booking_thanks")
        