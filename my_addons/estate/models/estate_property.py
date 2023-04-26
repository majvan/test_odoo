from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The offer price must be positive"),
        ("check_offer_accepted", "CHECK((NOT state = 'offer_accepted') OR (selling_price >= 0.9 * expected_price))", "Too low selling price to accept, it has to be at least 90% of expected price")
    ]
    _inherit = ['mail.thread']  # For a chatter
    _order = "id desc"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=2))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Garden orientation',
        selection=[('N', 'North'), ('S', 'South'), ('E', 'East'), ('W', 'West')],
        )
    state = fields.Selection(string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        default='new',
        group_expand="_read_group_state_ids",
        )

    # Relational
    user_ids = fields.Many2many('res.users', string='Salesman', default=lambda self:self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', readonly=True)
    tags_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')

    # Computed
    total_area = fields.Integer(
        "Total Area (sqm)",
        compute="_compute_total_area",
        # search="_search",  # this is used in search, but also for sorting because it creates a query
        help="Total area computed by summing the living area and the garden area",
    )
    best_price = fields.Float("Best Offer", compute="_compute_best_price", help="Best offer received")

    # ---------------------------------------- Compute methods ------------------------------------
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        # Self can be a list of entries or one entry itself.
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'N'
            else:
                record.garden_area = 0
                record.garden_orientation = ''

    # @api.onchange("user_ids")  # Temporarily disabled
    def _onchange_users(self):
        for record in self:
            followers = set(record.message_follower_ids.partner_id.ids)
            users = set(record.user_ids.partner_id.ids)
            new_followers = users - followers
            old_followers = followers - users
            record.message_subscribe(list(new_followers))
            record.message_unsubscribe(list(old_followers))

    # ------------------------------------------ Model overloads -------------------------------------
    @api.ondelete(at_uninstall=False)
    def check_delete(self):
        if set(self.mapped("state")) - {"new", "canceled"}:
            raise UserError("Only new and canceled properties can be deleted.")
        
    @api.model
    def _read_group_state_ids(self, stages, domain, order):
        #return [t[0] for t in self.__class__.state.selection]
        return ['new', 'offer_received', 'offer_accepted','sold']

    # ---------------------------------------- Constrains -------------------------------------
    # another solution for constrains, now with changing expected / selling price
    # @api.constrains("expected_price", "selling_price")
    # def _check_price_difference(self):
    #     for prop in self:
    #         if (
    #             not float_is_zero(prop.selling_price, precision_rounding=0.01)
    #             and float_compare(prop.selling_price, prop.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
    #         ):
    #             raise ValidationError(
    #                 "The selling price must be at least 90% of the expected price! "
    #                 + "You must reduce the expected price if you want to accept this offer."
    #             )

    # ---------------------------------------- Action Methods -------------------------------------
    def action_sold(self):
        if 'canceled' in self.mapped('state'):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if 'sold' in self.mapped('state'):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})