from odoo import models, fields

class estate_property_tag(models.Model):
    _name="estate.property.tag"
    _description="property tag"
    _sql_constraints = [
        ('tag_unique', 'UNIQUE(name)','A property tag must be unique!')
    ]

    name = fields.Char(required=True)