# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.domum.tests.domum_test import suite
except ImportError:
    from .domum_test import suite

__all__ = ['suite']
