from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class SalePortalEnhanced(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        SaleOrder = request.env['sale.order']
        values['sale_count'] = SaleOrder.search_count([])
        return values

    @http.route(['/sale_orders'], type='http', auth="user", website=True)
    def portal_my_sale_orders(self, **kwargs):
        priority = kwargs.get('priority')  
        overdue = kwargs.get('overdue')    
        domain = [] 

        if priority:
            domain.append(('priority_level', '=', priority))

        if overdue == '1':
            domain.append(('is_deadline_overdue', '=', True))
            domain.append(('state', '!=', 'sale')) 

        orders = request.env['sale.order'].sudo().search(domain)

        values = {
            'orders': orders,
            'priority': priority,
            'overdue': overdue,
        }
        return request.render("sale_enhancement.portal_sale_orders_page", values)
