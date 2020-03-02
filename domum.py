#This file is part of domum project for Tryton. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

class Group(tree(separator=' / '), ModelSQL, ModelView):
    'Domum Group'
    __name__ = 'domum.group'
    company = fields.Many2One('company.company', 'Company', required=True,
        states={
            'readonly': True,
            },
        domain=[
                ('id', If(Eval('context', {}).contains('company'), '=', '!='),
                    Eval('context', {}).get('company', -1)),
            ], select=True)
    name = fields.Char('Name', required=True)
    description = fields.Char('Description')
    parent = fields.Many2One('domum.group', 'Parent', select=True,
        domain=[
            ('company', '=', Eval('company'))
        ], depends=['company'])
    childs = fields.One2Many('domum.group', 'parent', string='Childs',
        domain=[
            ('company', '=', Eval('company'))
        ], depends=['company'])
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
    type = fields.Selection([
            ('apartment', 'Apartment'),
            ('house', 'House'),
        ], 'Type', required=True)
    party = fields.Many2One('party.party', 'Party', required=True)
    state = fields.Selection([
            ('unknown', 'Unknown'),
            ('rented', 'Rented'),
            ('for_rent', 'For rent'),
            ('for_sale', 'For sale'),
            ('unoccupied', 'Unoccupied'),
            ('occupied', 'occupied')
        ], 'State', required=True)
    order = fields.Integer('Order')
    surface = fields.Float('Surface',
        digits=(16, Eval('unit_digits', 2)),
        depends=['unit_digits'])
    unit_digits = fields.Function(fields.Integer('Unit Digits'),
        'on_change_with_unit_digits')
    uom = fields.Many2One('product.uom', 'Unit',
        domain=[
                ('category', '=', Eval('uom_category')),
            ],
        depends=['uom_category'])
    uom_category = fields.Function(
        fields.Many2One('product.uom.category', 'Uom Category'),
        'get_uom_category')
    extensions = fields.One2Many('domum.unit.extension',
        'unit', 'Extensions')
    owners = fields.Many2Many(
        'domun.unit-party.owner',
        'owner', 'unit', 'Owners')
    residents = fields.Many2Many(
        'domun.unit-party.resident',
        'resident', 'unit', 'Residents')
    agents = fields.Many2Many(
        'domun.unit-party.agent',
        'agent', 'unit', 'Agents')

    @classmethod
    def __setup__(cls):
        super(Unit, cls).__setup__()
        cls._order = [
                ('order', 'ASC'),
                ('name', 'ASC'),
            ]

    @fields.depends('uom')
    def on_change_with_unit_digits(self, name=None):
        if self.uom:
            return self.uom.digits
        return 2

    @fields.depends()
    def get_uom_category(self, name=None):
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id('product', 'uom_cat_surface')


class Extension(ModelSQL, ModelView):
    'Domum Unit Extension'
    __name__ = 'domum.unit.extension'
    unit = fields.Many2One('domum.unit', 'Unit', required=True)
    name = fields.Char('Name', states={'required': True})
    description = fields.Char('Description', size=None)
    type = fields.Selection([
            ('storehouse', 'Storehouse'),
            ('parking', 'Parking')
        ], 'Type', required=True)
    order = fields.Integer('Order')
    surface = fields.Float('Surface',
        digits=(16, Eval('unit_digits', 2)),
        depends=['unit_digits'])

    unit_digits = fields.Function(fields.Integer('Unit Digits'),
        'on_change_with_unit_digits')

    unit = fields.Many2One('product.uom', 'Surface',
        domain=[
            If(Bool(Eval('product_uom_category')),
                ('category', '=', Eval('product_uom_category')),
                ('category', '=', -1)),
            ],
        depends=['product_uom_category'])


class UnitOwner(ModelSQL):
    'Domum Unit - Owner'
    __name__ = 'domun.unit-party.owner'
    unit = fields.Many2One('domum.unit',
        'Unit', ondelete='CASCADE', select=True, required=True)
    owner = fields.Many2One('party.party',
        'Owner', ondelete='CASCADE', select=True, required=True)


class UnitResident(ModelSQL):
    'Domum Unit - Resident'
    __name__ = 'domun.unit-party.resident'
    unit = fields.Many2One('domum.unit',
        'Unit', ondelete='CASCADE', select=True, required=True)
    resident = fields.Many2One('party.party',
        'Resident', ondelete='CASCADE', select=True, required=True)


class UnitAgent(ModelSQL):
    'Domum Unit - Agent'
    __name__ = 'domun.unit-party.agent'
    unit = fields.Many2One('domum.unit',
        'Unit', ondelete='CASCADE', select=True, required=True)
    agent = fields.Many2One('party.party',
        'Agent', ondelete='CASCADE', select=True, required=True)

