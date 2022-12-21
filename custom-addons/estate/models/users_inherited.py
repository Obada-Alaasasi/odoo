from odoo import models,fields, api

#extend res.users model to have a field for properties
class users_inherited(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', inverse_name="user_id", domain ="['|', ('state','=','New'), ('state','=','Offer Received')]")
