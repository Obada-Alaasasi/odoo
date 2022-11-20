from odoo import fields, models

class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"

    price = fields.Float()
    partner_id = fields.Many2one('res.partner', required = True, string = "Partner")
    property_id = fields.Many2one('estate.property', required = True)
    status = fields.Selection(selection = [("Accepted", "Accepted"), ("Refused", "Refused")],copy = False)
    