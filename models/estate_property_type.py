from odoo import models, fields

class estate_property_type(models.Model):
    _name= "estate.property.type"
    _description= "property type"

    #define model fields (columns in the SQL table)
    type= fields.Char(required = True)
    description = fields.Text()