from odoo import models, fields, api, Command
from odoo.exceptions import UserError, AccessError

class inh_estate_property(models.Model):
    _inherit = 'estate.property'

    def property_sold(self):
        
        # print('reached'.center(100, '='))

        # check acess priveleges
        self.env['estate.property'].check_access_rights('write', True)
        self.env['estate.property'].check_access_rule('write')

        # print('reached'.center(100, '=')) #accessed

        #create the invoice lines
        #NOTE: two sudo() methods here are requried to access two different models (account.move, account.journal)
        self.env['account.move'].sudo().create({
            'partner_id':self.partner_id.id,
            'move_type': 'out_invoice',
            'journal_id': self.env['account.journal'].sudo().search([('name','=','Customer Invoices')]).id,
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

