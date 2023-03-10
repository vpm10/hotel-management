{
    'name': 'Hotel Room Management',
    'version': '16.0.5.0.0',
    'sequence': '-2',
    'category': 'Hotel Management',
    'summary': 'Manage hotel room',
    'description': '''Hotel room management''',

    'installation': True,
    'application': True,

    'depends': ['base', 'mail', 'sale', 'account', 'website'],
    'data': ['security/user_group.xml',
             'security/ir.model.access.csv',
             'report/report.xml',
             'data/food.category.csv',
             'data/item_food.xml',
             'data/website_menu.xml',
             'wizard/food_order.xml',
             'wizard/report_wizard.xml',
             'wizard/report_wizard_js.xml',
             'views/reception.xml',
             'views/guest_info.xml',
             'views/hotel_room.xml',
             'views/facility.xml',
             'views/order_food.xml',
             'views/food_category.xml',
             'views/food_item.xml',
             'views/order_list.xml',
             'views/payment_calculation.xml',
             'views/portal_templates.xml',
             'views/website_room_booking.xml',
             'views/hotel_menu.xml',
             ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'hotel_room_management/static/src/js/action_manager.js'
    #     ]
    # }
}
