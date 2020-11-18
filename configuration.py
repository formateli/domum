# This file is part of domum module.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelSingleton, ModelView, ModelSQL, fields
from trytond.modules.company.model import CompanyMultiValueMixin

__all__ = [
        'Configuration',
        ]


class Configuration(
        ModelSingleton, ModelSQL, ModelView, CompanyMultiValueMixin):
    'Domum Configuration'
    __name__ = 'domum.configuration'
    unit_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ], 'Default Unit Type')
