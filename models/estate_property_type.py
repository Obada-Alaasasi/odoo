from odoo import models, fields

class estate_property_type(models.Model):
    _name= "estate.property.type"
    _description= "property type"
    _sql_constraints = [
        ('type_unique', 'UNIQUE(name)', 'A property type must be unique')
    ]

    #define model fields (columns in the SQL table)
    name= fields.Char(required = True)
    # description = fields.Text()