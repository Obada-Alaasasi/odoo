from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import *

#the model will be mapped to a PostgreSQL table in the odoo database through ORM
class estate_property(models.Model):
    #define table info
    _name = "estate.property"
    _description = "features of listed estate properties"
    _sql_constraints = [
        ('selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling price must be strictly positive!'),
        ('expected_price_positive', 'CHECK(expected_price >= 0)', 'Expected price must be strictly positive!')
    ]

    #define table columns
    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, string = "Available from",  default = (datetime.now() + relativedelta(months =+ 3)).strftime("%Y-%m-%d") )
    expected_price = fields.Float(required = True)
    best_offer = fields.Float(compute = "_best_offer")
    selling_price = fields.Float(readonly = True, copy =False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer(string = "Living area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string = "Garden area (sqm)")
    total_area = fields.Float(compute = "_total_area")
    garden_orientation = fields.Selection(selection = [('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')])
    state = fields.Selection(required = True, copy = False, selection=[('New', 'New'),\
        ('Offer Received', 'Offer Received'),\
            ('Offer Accepted', 'Offer Accepted'),\
                ('Sold', 'Sold'),\
                    ('Cancelled', 'Cancelled')], default = 'New')
    active = fields.Boolean(default = True)
    type = fields.Many2one('estate.property.type')
    user_id = fields.Many2one('res.users', index = True, string = 'Salesperson', default = lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string = 'Partner', required = True, copy = False)
    tag_ids = fields.Many2many('estate.property.tag', string = 'tags')
    offer_ids = fields.One2many('estate.property.offer', inverse_name = 'property_id')
    
    #computed field: total_area; add living and garden areas
    @api.depends("living_area", "garden_area") 
    def _total_area(self):
        for record in self:
                record.total_area = record.living_area + record.garden_area

    #computed field: best_offer; compare offers and choose max price
    @api.depends("offer_ids.price")
    def _best_offer(self):
        for record in self:
            if len(record.offer_ids.mapped('price')) > 0:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else: record.best_offer = 0

    #onchange function; change garden area and orientation values when garden changes
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    
    #SOLD BUTTON: set the property state as SOLD
    def property_sold(self):
        for record in self:
            if record.state != 'Cancelled':
                record.state = 'Sold'
            else: #return an error message 
                raise UserError("This property is cancelled!")
        return True

    #CANCEL BUTTON: set the property state as CANCELlED
    def property_cancelled(self):
        for record in self:
            if record.state != "Sold":
                record.state = "Cancelled"
            else: #return an error message 
                raise UserError("This property is already sold!")
        return True
    
    #SELLING_PRICE CONSTRAINT
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if 'Accepted' not in [entry.status for entry in self.env['estate.property.offer'].search([('property_id', '=', '{}'.format(record.id))])]:
                if record.selling_price < (0.9 * record.expected_price):
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price.")
            
    #TEST BUTTON
    def test(self):
        raise UserError("{}".format([record.status for record in self.env['estate.property.offer'].search([])]))

    
    

    

    


            


    
