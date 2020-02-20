#This file is part of domum project for Tryton. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

class Group(tree(separator=' / '), ModelSQL, ModelView):
    'Domum Group'
    __name__ = 'domum.group'
    # Company
    name = fields.Char('Name', required=True)
    description = fields.Char('Description')
    parent = fields.Many2One('domum.group', 'Parent', select=True)
    childs = fields.One2Many('domum.group', 'parent',
            string='Childs')
    order = fields.Integer('Order')

    @classmethod
    def __setup__(cls):
        super(Category, cls).__setup__()
        cls._order = [
                ('order', 'ASC'),
                ('name', 'ASC'),
            ]


class Unit(ModelSQL, ModelView):
    'Domum Unit'
    __name__ = 'domum.unit'
    group = fields.Many2One('domum.group',
        'Group', required=True)
    name = fields.Char('Name', states={'required': True})
    description = fields.Char('Description', size=None)
    party = fields.Many2One('party.party',
        'Party', states={'required': True})
    type = fields.Selection([
            ('storehouse', 'Storehouse'),
            ('apartment', 'Apartment'),
            ('house', 'House'),
            ('parking', 'Parking')
        ], 'Type', required=True)
    state = fields.Selection([
            ('unknown', 'Unknown'),
            ('rented', 'Rented'),
            ('for_rent', 'For rent'),
            ('for_sale', 'For sale'),
            ('unoccupied', 'Unoccupied'),
            ('occupied', 'occupied')
        ], 'State', required=True)
    order = fields.Integer('Order')
    #surface
    unit = fields.Many2One('product.uom', 'Surface',
        domain=[
            If(Bool(Eval('product_uom_category')),
                ('category', '=', Eval('product_uom_category')),
                ('category', '=', -1)),
            ],
        depends=['product_uom_category'])

    owners = fields.Many2Many(
        'poliza.pagos-liquidacion.vendedor',
        'unit', 'party', 'Owners',
        domain=[
            ('company', '=', Eval('company')),
            ('currency', '=', Eval('currency')),
            ('vendedor', '=', Eval('vendedor')),
            If(
                In(Eval('state'), ['borrador', 'procesado']),
                ('state', '=', 'liq_cia'),
                ('state', '!=', '')
            )
        ],
        states={
            'readonly': Not(In(Eval('state'), ['borrador',])),
            'invisible': Not(Bool(Eval('vendedor'))),
        }, depends=['company', 'currency', 'vendedor', 'state'])


    owners = fields.One2Many('party.party',
        'domum_unit', 'Owners')
    tenants = fields.One2Many('party.party',
        'domum_unit', 'Tenants')

