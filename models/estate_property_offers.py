from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime, date
from dateutil.relativedelta import *

class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "price desc"

    price = fields.Float()
    partner_id = fields.Many2one('res.partner', required = True, string = "Partner")
    '''NOTE: 
    set foreign key constraint as ON DELETE CASCADE rather than RESTRICT to allow delete offer records 
    after deleting the corresponding property record
    '''
    property_id = fields.Many2one('estate.property', required = True ,ondelete = 'cascade')   
    validity = fields.Integer(default = 7, string = "validity (days)")
    date_deadline = fields.Date(string = "Deadline", compute = "_set_date", inverse = "_set_validity") #values are not stored in db unless attr "store=True"
    state = fields.Selection(selection = [("Accepted", "Accepted"), ("Refused", "Refused")], readonly = True, copy = False)

    #use validity to change the deadline before saving the record
    @api.depends("validity")
    def _set_date(self):
        for record in self:
            record.date_deadline = (datetime.now() + relativedelta(days =+ record.validity)).strftime("%Y-%m-%d")

    #change validity based on the set deadline date
    def _set_validity(self):
        for record in self:
            date_diff = record.date_deadline - date.today() #NOTE: both operands have the same data formats (both are dates, and of the same formats)
            record.validity = date_diff.days + 1

    #ACCEPT BUTTON: accept a given offer
    def accept_offer(self):            
        #accept offer, and set selling price and buyer
        for record in self:
            if 'Accepted' not in [entry.state for entry in self.env['estate.property.offer'].search([('property_id', '=', '{}'.format(record.id))])]: #if no offer is accepted
                record.state = "Accepted"
                record.property_id.selling_price = record.price
                record.property_id.partner_id = record.partner_id
                record.property_id.state = 'Offer Accepted'
            else:
                raise UserError("Another offer was already accepted!")
        return True

    #REFUSE BUTTON: refuse a given offer
    def refuse_offer(self):
        for record in self:
            record.state = "Refused"
        return True
            
    #change property state after first offer, a new offer can only be higher than existing offer
    @api.model
    def create(self, vars):
        #find the property the offer is referring to thru property_id (NOTE: browse returns a recordset)
        property = self.env['estate.property'].browse(vars['property_id'])[0]
        if vars['price'] <= property.best_offer:
            raise UserError('Sorry, placed offer has to be higher than {}'.format(property.best_offer))
        else:
            if len(property.offer_ids.mapped('price')) == 0:
                property.state = 'Offer Received'
            return super().create(vars)
        #NOTE: added business logic will take effect, but will return the parent's
        #NOTE: keep in mind that a record is only created after reload so, the excpetion will only appear upon reload
        

        
            
            