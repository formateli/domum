# This file is part of domum module.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.pool import Pool
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.modules.company.tests import create_company, set_company

__all__ = ['create_group_units']


class DomumTestCase(ModuleTestCase):
    'Test domum module'
    module = 'domum'

    @with_transaction()
    def test_domum(self):
        pool = Pool()
        Configuration = pool.get('domum.configuration')
        Extension = pool.get('domum.unit.extension')
        UnitOwner = pool.get('domun.unit-party.owner')
        UnitResident = pool.get('domun.unit-party.resident')
        UnitAgent = pool.get('domun.unit-party.agent')

        company = create_company()
        with set_company(company):
            building, units = create_group_units(company)


def create_group_units(company):
    pool = Pool()
    Party = pool.get('party.party')
    Address = pool.get('party.address')
    Group = pool.get('domum.group')
    Unit = pool.get('domum.unit')

    group, = Group.create([{
        'company': company,
        'name': 'Domum Group',
        }])

    units = []
    i = 1
    while i < 11:
        floor, = Group.create([{
            'company': company,
            'parent': group.id,
            'name': 'Floor ' + str(i),
            }])

        x = 1
        while x < 5:
            party = Party(
                name='Apartment ' + str(x) + ' ' + floor.name,
                party_type='domum',
                addresses=[Address(name='Main Address')]
                )
            party.save()

            units += Unit.create([{
                    'group': floor.id,
                    'type': 'apartment',
                    'party': party.id,
                    'state': 'unknown',
                    }])
            x += 1
        i += 1

    return group, units


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        DomumTestCase))
    return suite
