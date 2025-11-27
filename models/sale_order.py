from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_deadline = fields.Date(string='Delivery Deadline')
    priority_level = fields.Selection(
        [('low','Low'),('medium','Medium'),('high','High')],
        string='Priority Level', default='medium')

    is_deadline_overdue = fields.Boolean(string='Deadline Overdue', compute='_compute_deadline_fields', store=True)
    deadline_delay_days = fields.Integer(string='Deadline Delay (days)', compute='_compute_deadline_fields', store=True)

    customer_rating = fields.Float(string='Customer Rating', default=0.0)

    @api.depends('delivery_deadline')
    def _compute_deadline_fields(self):
        today = datetime.today().date()  
        for order in self:
            if order.delivery_deadline:
                deadline_date = order.delivery_deadline
                if today > deadline_date:
                    order.is_deadline_overdue = True
                    delta = (today - deadline_date).days
                    order.deadline_delay_days = delta if delta > 0 else 0
                else:
                    order.is_deadline_overdue = False
                    order.deadline_delay_days = 0
            else:
                order.is_deadline_overdue = False
                order.deadline_delay_days = 0

    @api.onchange('partner_id')
    def _onchange_partner_id_copy_rating(self):
        for order in self:
            if order.partner_id:
                order.customer_rating = float(order.partner_id.customer_rating or 0.0)
    
    def action_confirm(self):
        for order in self:
            if not order.delivery_deadline:
                raise ValidationError(
                    "Please set a Delivery Deadline before confirming the order."
                )
        return super(SaleOrder, self).action_confirm()

    @api.constrains('priority_level', 'delivery_deadline', 'date_order')
    def _check_high_priority_deadline(self):
        for order in self:
            if order.priority_level == 'high' and order.delivery_deadline:
                order_date = order.date_order.date() if isinstance(order.date_order, datetime) else order.date_order
                deadline = order.delivery_deadline
                max_allowed_date = order_date + timedelta(days=3)
                if deadline > max_allowed_date:
                    raise ValidationError(
                        "For high priority orders, the delivery deadline must be within 3 days of the order date."
                    )


    @api.constrains('customer_rating')
    def _check_customer_rating(self):
        for order in self:
            if order.customer_rating is not None:
                if order.customer_rating < 0 or order.customer_rating > 5:
                    raise models.ValidationError('Customer rating must be between 0 and 5.')
    
    def action_extend_deadline_3(self):
        for order in self:
            if order.delivery_deadline:
                order.delivery_deadline = order.delivery_deadline + timedelta(days=3)
                order.message_post(body="Deadline extended by 3 days.")
            else:
                order.message_post(body="No delivery deadline was set earlier. Please set one.")
    
    def action_extend_deadline_by_3_days(self):
        for order in self:

            if order.delivery_deadline:
                new_deadline = order.delivery_deadline + timedelta(days=3)
                order.delivery_deadline = new_deadline
                order.message_post(body='Deadline extended by 3 days.')

            else:
                new_deadline = fields.Date.today() + timedelta(days=3)
                order.delivery_deadline = new_deadline
                order.message_post(body='Deadline set and extended by 3 days.')
