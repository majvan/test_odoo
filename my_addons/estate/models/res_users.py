from odoo import fields, models

class NewUserModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.Many2many('estate.property', string="Properties", domain=[("state", "in", ["new", "offer_received"])])