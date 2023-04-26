from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence", default=10)

    # Relational (for inline view)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Property Offer")

    # Computed
    offer_count = fields.Integer("Number of offers", compute="_compute_offer")

    # ---------------------------------------- Compute Methods -------------------------------------
    @api.depends("offer_ids")  # not sure if this would work
    def _compute_offer(self):
        count = 0
        for record in self:
            count += len(self.offer_ids)
        self.offer_count = count

    # ---------------------------------------- Actions -------------------------------------
    def action_view_offers(self):
        # This works only once :) After History back and forward on web browser,
        # the filter is not applied. Maybe the issue is that it wraps estate_property_offer_action
        # which does not filter.
        # The other solution - create a separate tab in viee, is better IMHO.
        res = self.env.ref("estate.estate_property_offer_action").read()[0]
        res["domain"] = [("id", "in", self.offer_ids.ids)]
        return res