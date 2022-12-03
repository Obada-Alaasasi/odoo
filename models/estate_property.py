from odoo import models, fields, api, Command
from odoo.exceptions import UserError

class inh_estate_property(models.Model):
    _inherit = 'estate.property'

    def property_sold(self):
        #create the invoice lines
        self.env['account.move'].create({
            'partner_id':self.partner_id.id,
            'move_type': 'out_invoice',
            'journal_id': self.env['account.journal'].search([('name','=','Customer Invoices')]).id,
            'line_ids':[
                # invoice line #1: 6% selling price 
                Command.create({
                    'name':'Property: {} | upfront payment'.format(self.name),
                    'quantity': 1,
                    'price_unit':self.selling_price*0.06
                }),
                # invoice line #2: 100$ administritive fees
                Command.create({
                    'name':'Property: {} | administritive fees'.format(self.name),
                    'quantity': 1,
                    'price_unit': 100
                })
            ]
        })
        return super().property_sold()

