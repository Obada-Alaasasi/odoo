from odoo import models, fields

class estate_property_tags(models.Model):
    _name="estate.property.tags"
    _description="property tags"

    name = fields.Char(required=True)