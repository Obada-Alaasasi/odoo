from odoo import models, fields

class estate_property_type(models.Model):
    _name= "estate.property.type"
    _description= "property type"
    _sql_constraints = [
        ('type_unique', 'UNIQUE(name)', 'A property type must be unique')
    ]
    _order = "sequence"

    #define model fields (columns in the SQL table)
    name= fields.Char(string = "Title", required = True)
    property_ids = fields.One2many('estate.property', inverse_name='properties_per_type')
    sequence = fields.Integer(string="Sequence") #used to order elements by dragging