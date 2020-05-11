# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.pool import Pool
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.modules.company.tests import create_company, set_company


class DomumTestCase(ModuleTestCase):
    'Test domum module'
    module = 'domum'

    @with_transaction()
    def test_domum(self):
        pool = Pool()
        Party = pool.get('party.party')
        Group = pool.get('domum.group')
        Unit = pool.get('domum.unit')
        Extension = pool.get('domum.unit.extension')
        UnitOwner = pool.get('domun.unit-party.owner')
        UnitResident = pool.get('domun.unit-party.resident')
        UnitAgent = pool.get('domun.unit-party.agent')

        company = create_company()
        with set_company(company):
            building, = Group.create([{
                'company': company,
                'name': 'Building',
                }])
            i = 1
            while i < 11:
                floor, = Group.create([{
                    'company': company,
                    'parent': building.id,
                    'name': 'Floor ' + str(i),
                    }])

                x = 1
                while x < 5:
                    party, = Party.create([{
                        'name': 'Apartment ' + str(x) + ' ' + floor.name,
                        'party_type': 'domum',
                        }])
                    Unit.create([{
                        'group': floor.id,
                        'type': 'apartment',
                        'party': party.id,
                        'state': 'unknown',
                        }])
                    x += 1
                i += 1


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        DomumTestCase))
    return suite
