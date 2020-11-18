# This file is part of domum module.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.model import ModelView, ModelSQL, fields, tree
from trytond.pyson import Bool, Eval, If

__all__ = [
    'Group', 'Unit', 'Extension',
    'UnitOwner', 'UnitResident', 'UnitAgent',
    ]


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
    units = fields.One2Many('domum.unit',
            'group', 'Units')
    order = fields.Integer('Order')

    @classmethod
    def __setup__(cls):
        super(Group, cls).__setup__()
        cls._order = [
            ('order', 'ASC'),
            ('name', 'ASC'),
            ]

    @staticmethod
    def default_company():
        return Transaction().context.get('company')


class _UnitMixin(ModelSQL, ModelView):
    description = fields.Char('Description', size=None)
    order = fields.Integer('Order')
    surface = fields.Float('Surface',
        digits=(16, Eval('unit_digits', 2)),
        depends=['unit_digits'])
    uom = fields.Many2One('product.uom', 'Unit',
        states={
            'required': Bool(Eval('surface')),
        },
        domain=[
            ('category', '=', Eval('uom_category')),
        ],
        depends=['surface', 'uom_category'])
    unit_digits = fields.Function(fields.Integer('Unit Digits'),
        'on_change_with_unit_digits')
    uom_category = fields.Function(
        fields.Many2One('product.uom.category', 'Uom Category'),
        'get_uom_category')

    @staticmethod
    def default_uom_category():
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id('product', 'uom_cat_surface')

    @fields.depends('uom')
    def on_change_with_unit_digits(self, name=None):
        if self.uom:
            return self.uom.digits
        return 2

    @fields.depends()
    def get_uom_category(self, name=None):
        return self.default_uom_category()

    @classmethod
    def __setup__(cls):
        super(_UnitMixin, cls).__setup__()
        cls._order = [
            ('order', 'ASC'),
            ]


class Unit(_UnitMixin):
    'Domum Unit'
    __name__ = 'domum.unit'
    group = fields.Many2One('domum.group', 'Group', required=True,
        domain=[
            ('company', If(Eval(
                        'context', {}).contains('company'), '=', '!='),
                Eval('context', {}).get('company', -1)),
            ])
    type = fields.Selection([
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ], 'Type', required=True)
    party = fields.Many2One('party.party', 'Party', required=True,
        domain=[
            ('party_type', '=', 'domum')
        ])
    state = fields.Selection([
        ('unknown', 'Unknown'),
        ('rented', 'Rented'),
        ('for_rent', 'For rent'),
        ('for_sale', 'For sale'),
        ('unoccupied', 'Unoccupied'),
        ('occupied', 'Occupied')
        ], 'State', required=True)
    extensions = fields.One2Many('domum.unit.extension',
        'unit', 'Extensions')
    owners = fields.Many2Many(
        'domun.unit-party.owner',
        'unit', 'owner', 'Owners')
    residents = fields.Many2Many(
        'domun.unit-party.resident',
        'unit', 'resident', 'Residents')
    agents = fields.Many2Many(
        'domun.unit-party.agent',
        'unit', 'agent', 'Agents')
    currency = fields.Many2One('currency.currency', 'Currency', required=True,
        states={
            'readonly': True,
        })
    currency_digits = fields.Function(fields.Integer('Currency Digits'),
        'on_change_with_currency_digits')
    amount = fields.Numeric('Amount',
        digits=(16, Eval('currency_digits', 2)),
        depends=['currency_digits'])

    @staticmethod
    def default_currency():
        Company = Pool().get('company.company')
        company = Transaction().context.get('company')
        if company:
            company = Company(company)
            return company.currency.id

    @staticmethod
    def default_currency_digits():
        Company = Pool().get('company.company')
        company = Transaction().context.get('company')
        if company:
            company = Company(company)
            return company.currency.digits
        return 2

    @fields.depends('currency')
    def on_change_with_currency_digits(self, name=None):
        if self.currency:
            return self.currency.digits
        return 2

    def get_rec_name(self, name):
        return self.party.rec_name

    @classmethod
    def search_rec_name(cls, name, clause):
        return [('party.rec_name',) + tuple(clause[1:])]


class Extension(_UnitMixin):
    'Domum Unit Extension'
    __name__ = 'domum.unit.extension'
    name = fields.Char('Name', required=True)
    unit = fields.Many2One('domum.unit', 'Unit', required=True)
    type = fields.Selection([
        ('storehouse', 'Storehouse'),
        ('parking', 'Parking')
        ], 'Type', required=True)

    @classmethod
    def __setup__(cls):
        super(Extension, cls).__setup__()
        cls._order.append(('name', 'ASC'))


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
