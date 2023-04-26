from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be strictly positive"),
    ]
    price = fields.Float("Price", required=True)
    # validity = fields.Integer(string="Validity (days)", default=7)
    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
        default=False,
    )
    create_date = fields.Date(default=lambda self:fields.Date.today())
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline_from_validity", inverse="_compute_validity_from_deadline")
    max_offer = fields.Boolean(compute="_is_max_offer")
    price_per_area = fields.Float("Price per sqm", compute="_compute_price_per_area")

    # Relational
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type")

    # ---------------------------------------- Compute Methods -------------------------------------
    @api.depends("create_date", "validity")
    def _compute_deadline_from_validity(self):
        for record in self:
            date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = date + relativedelta(days=record.validity)
    
    def _compute_validity_from_deadline(self):
        for record in self:
            date = record.create_date if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - date).days

    @api.depends("price")
    def _is_max_offer(self):
        records = self.property_id
        if records.offer_ids:
            max_offer = max(records.mapped("offer_ids.price"))
            for record in self:
                record.max_offer = float_compare(record.price, max_offer, precision_rounding=0.01) >= 0

    @api.depends("price")
    def _compute_price_per_area(self):
        for record in self:
            if record.property_id.living_area:
                record.price_per_area = record.price / record.property_id.living_area
            else:
                record.price_per_area = 0


    # ---------------------------------------- Action Methods -------------------------------------
    def action_accept(self):
        if 'accepted' == self.mapped('property_id.offer_ids.state'):
            raise UserError('An offer as already been accepted.')
        self.write({"state": "accepted",})
        return self.mapped("property_id").write({"state": "offer_accepted", "selling_price": self.price, "buyer_id": self.partner_id.id,})

    def action_refuse(self):
        return self.write({"state": "refused",})
    
    # ------------------------------------------ Model overloads  -------------------------------------
    @api.model
    def create(self, vals):
        if not vals.get("property_id") or not vals.get("price"):
            raise UserError("A price higher than zero must be defined")
        prop = self.env["estate.property"].browse(vals["property_id"])
        # We check if the offer is higher than the existing offers
        if prop.offer_ids:
            max_offer = max(prop.mapped("offer_ids.price"))
            if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                raise UserError("The offer must be higher than %.2f" % max_offer)
        prop.state = "offer_received"
        return super().create(vals)