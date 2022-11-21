from odoo import fields, models, api
from datetime import datetime, timedelta
from dateutil.relativedelta import *

#the model will be mapped to a PostgreSQL table in the odoo database through ORM
class estate_property(models.Model):
    #define table info
    _name = "estate.property"
    _description = "features of listed estate properties"

    #define table columns
    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, string = "Available from",  default = (datetime.now() + relativedelta(months =+ 3)).strftime("%Y-%m-%d") )
    expected_price = fields.Float(required = True)
    best_offer = fields.Float(compute = "_best_offer")
    selling_price = fields.Float(readonly = True, copy =False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Float(compute = "_total_area")
    garden_orientation = fields.Selection(selection = [('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')])
    state = fields.Selection(required = True, copy = False, selection=[('New', 'New'),\
        ('Offer Received', 'Offer Received'),\
            ('Offer Accepted', 'Offer Accepted'),\
                ('Sold', 'Sold'),\
                    ('Canceled', 'Canceled')], default = 'New')
    active = fields.Boolean(default = True)
    type = fields.Many2one('estate.property.type')
    user_id = fields.Many2one('res.users', index = True, string = 'Salesperson', default = lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string = 'Partner', required = True, copy = False)
    tag_ids = fields.Many2many('estate.property.tag', string = 'tags')
    offer_ids = fields.One2many('estate.property.offer', inverse_name = 'property_id')
    
    @api.depends("living_area", "garden_area")
    def _total_area(self):
        for record in self:
                record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'))

            


    
