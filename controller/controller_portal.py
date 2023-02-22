from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request, Controller


class CountBooking(CustomerPortal):
    # @http.route(['/my/home'], type='http', auth="user", website=True)
    def _prepare_home_portal_values(self, counters):
        # print("csss",counters)
        vals = super()._prepare_home_portal_values(counters)
        if 'count_booking' in counters:
            vals['count_booking'] = request.env['guest.details'].sudo().\
                search_count([
                    ('guest_id', '=', request.env.user.name)])
        # print(vals)

        return vals


class PortalControl(Controller):
    @http.route(['/my/room'], type='http', auth="user", website=True)
    def _portal_room_book(self):
        bookings = request.env['guest.details'].sudo().search([
            ('guest_id', '=', request.env.user.name)])
        values = {}
        values.update({
            'rooms': bookings,
        })
        return request.render("hotel_room_management.portal_room_booking",
                              values)
