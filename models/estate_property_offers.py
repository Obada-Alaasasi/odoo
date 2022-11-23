from odoo import fields, models, api
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
    
    @api.depends("validity")
    def _set_date(self):
        for record in self:
            record.date_deadline = (datetime.now() + relativedelta(days =+ record.validity)).strftime("%Y-%m-%d")

    def _set_validity(self):
        for record in self:
            date_diff = record.date_deadline - date.today() #NOTE: both operands have the same data formats (both are dates, and of the same formats)
            record.validity = date_diff.days + 1
            
            
            