from odoo import models, fields

class estate_property_tag(models.Model):
    _name="estate.property.tag"
    _description="property tag"

    name = fields.Char(required=True)