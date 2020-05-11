# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import party
from . import domum


def register():
    Pool.register(
        party.Party,
        domum.Group,
        domum.Unit,
        domum.Extension,
        domum.UnitOwner,
        domum.UnitResident,
        domum.UnitAgent,
        module='domum', type_='model')
