from odoo import models, fields, api, models
from odoo.exceptions import UserError

class inh_estate_property(models.Model):
    _inherit = 'estate.property'

    def property_sold(self):
        #create an invoice in account.move for the sale
        vals = {
            'partner_id':self.partner_id.id,
            'move_type': 'out_invoice',
            'journal_id': self.env['account.journal'].search([('name','=','Customer Invoices')]).id
        }
        self.env['account.move'].create(vals)

        return super().property_sold()

