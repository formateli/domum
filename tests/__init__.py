# This file is part of domum module.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.domum.tests.domum_test import \
            suite, create_group_units
except ImportError:
    from .domum_test import suite, create_group_units

__all__ = ['suite', 'create_group_units']
