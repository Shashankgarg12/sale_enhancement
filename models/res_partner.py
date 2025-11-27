from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'


    customer_rating = fields.Integer(string='Customer Rating', default=0)