from odoo import fields, models, api
from datetime import datetime, timedelta
from dateutil.relativedelta import *

class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"

    price = fields.Float()
    partner_id = fields.Many2one('res.partner', required = True, string = "Partner")
    property_id = fields.Many2one('estate.property', required = True)
    validity = fields.Integer(default = 7, string = "validity (days)")
    date_deadline = fields.Date(string = "Deadline", compute = "_set_date", inverse = "_set_validity")
    status = fields.Selection(selection = [("Accepted", "Accepted"), ("Refused", "Refused")],copy = False)
    
    @api.depends("validity")
    def _set_date(self):
        for record in self:
            record.date_deadline = (datetime.now() + relativedelta(days =+ record.validity)).strftime("%Y-%m-%d")

    def _set_validity(self):
        for record in self:
            record.validity = (record.date_deadline - datetime.now()).days + 1
            
            #reset validity to 7 days if manually-input date is before current date
            if record.validity < 0: record.validity = 7 
            