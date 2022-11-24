from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime, date
from dateutil.relativedelta import *

class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"

    price = fields.Float()
    partner_id = fields.Many2one('res.partner', required = True, string = "Partner")
    property_id = fields.Many2one('estate.property', required = True)
    validity = fields.Integer(default = 7, string = "validity (days)")
    date_deadline = fields.Date(string = "Deadline", compute = "_set_date", inverse = "_set_validity") #values are not stored in db unless attr "store=True"
    status = fields.Selection(selection = [("Accepted", "Accepted"), ("Refused", "Refused")],copy = False)
    
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
        if 'Accepted' not in [record.status for record in self.env['estate.property.offer'].search([])]: #if no offer is accepted
            
            #accept offer, and set selling price and buyer
            for record in self:
                record.status = "Accepted"
                record.property_id.selling_price = record.price
                record.property_id.partner_id = record.partner_id
        else:
            raise UserError("Another offer was already accepted!")
        return True

    #REFUSE BUTTON: refuse a given offer
    def refuse_offer(self):
        for record in self:
            record.status = "Refused"
        return True
            
            
            