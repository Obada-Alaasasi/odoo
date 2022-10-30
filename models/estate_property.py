from odoo import fields, models
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
    date_availability = fields.Date(copy = False, default = (datetime.now() + relativedelta(months =+ 3)).strftime("%Y-%m-%d") )
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy =False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection = [('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')])
    state = fields.Selection(required = True, copy = False, selection=[('New', 'New'),\
        ('Offer Received', 'Offer Received'),\
            ('Offer Accepted', 'Offer Accepted'),\
                ('Sold', 'Sold'),\
                    ('Canceled', 'Canceled')], default = 'New')
    active = fields.Boolean(default = True)

