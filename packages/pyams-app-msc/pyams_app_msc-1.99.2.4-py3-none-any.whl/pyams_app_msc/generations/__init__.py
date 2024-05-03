#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

from importlib import import_module

from pyams_app_msc.feature.booking.interfaces import IBookingInfo
from pyams_app_msc.feature.planning.interfaces import ISession
from pyams_app_msc.interfaces import MSC_CONTRIBUTOR_ROLE, MSC_MANAGER_ROLE, MSC_OPERATOR_ROLE, MSC_READER_ROLE
from pyams_app_msc.reference.structure import IStructureTypeTable
from pyams_app_msc.shared.catalog.interfaces import ICatalogEntryInfo
from pyams_catalog.generations import check_required_indexes
from pyams_catalog.index import DatetimeIndexWithInterface, FieldIndexWithInterface, KeywordIndexWithInterface
from pyams_catalog.interfaces import MINUTE_RESOLUTION
from pyams_content.generations import check_required_tables, check_required_tools
from pyams_security.index import PrincipalsRoleIndex
from pyams_site.generations import check_required_utilities
from pyams_site.interfaces import ISiteGenerations
from pyams_utils.registry import utility_config


REQUIRED_UTILITIES = ()

REQUIRED_TABLES = (
    (IStructureTypeTable, 'structures-types'),
)

REQUIRED_TOOLS = (
)

REQUIRED_INDEXES = (
    ('role:msc:manager', PrincipalsRoleIndex, {
        'role_id': MSC_MANAGER_ROLE
    }),
    ('role:msc:operator', PrincipalsRoleIndex, {
        'role_id': MSC_OPERATOR_ROLE
    }),
    ('role:msc:contributor', PrincipalsRoleIndex, {
        'role_id': MSC_CONTRIBUTOR_ROLE
    }),
    ('role:msc:reader', PrincipalsRoleIndex, {
        'role_id': MSC_READER_ROLE
    }),
    ('catalog_audience', KeywordIndexWithInterface, {
        'interface': ICatalogEntryInfo,
        'discriminator': 'audiences'
    }),
    ('planning_start_date', DatetimeIndexWithInterface, {
        'interface': ISession,
        'discriminator': 'start_date',
        'resolution': MINUTE_RESOLUTION
    }),
    ('planning_end_date', DatetimeIndexWithInterface, {
        'interface': ISession,
        'discriminator': 'end_date',
        'resolution': MINUTE_RESOLUTION
    }),
    ('planning_room', FieldIndexWithInterface, {
        'interface': ISession,
        'discriminator': 'room'
    }),
    ('booking_session', FieldIndexWithInterface, {
        'interface': IBookingInfo,
        'discriminator': 'session_index'
    }),
    ('booking_recipient', FieldIndexWithInterface, {
        'interface': IBookingInfo,
        'discriminator': 'recipient'
    }),
    ('booking_status', FieldIndexWithInterface, {
        'interface': IBookingInfo,
        'discriminator': 'status'
    })
)


@utility_config(name='PyAMS MSC application', provides=ISiteGenerations)
class MSCGenerationsChecker:
    """MSC package generations checker"""

    order = 200
    generation = 1

    def evolve(self, site, current=None):
        """Check for required utilities, tables and tools"""
        check_required_utilities(site, REQUIRED_UTILITIES)
        check_required_tables(site, REQUIRED_TABLES)
        check_required_tools(site, REQUIRED_TOOLS)
        check_required_indexes(site, REQUIRED_INDEXES)

        if not current:
            current = 1
        for generation in range(current, self.generation):
            module_name = f'pyams_app_msc.generations.evolve{generation}'
            module = import_module(module_name)
            module.evolve(site)
