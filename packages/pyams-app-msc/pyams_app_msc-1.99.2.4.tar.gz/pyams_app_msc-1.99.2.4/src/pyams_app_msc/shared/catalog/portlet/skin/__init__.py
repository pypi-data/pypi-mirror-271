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

from datetime import datetime, timedelta

from hypatia.catalog import CatalogQuery
from hypatia.interfaces import ICatalog
from hypatia.query import And, Eq, Ge, Le
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.feature.booking.interfaces import IBookingContainer
from pyams_app_msc.feature.planning.interfaces import ISession, VERSION_INFO, VERSION_INFO_ABBR
from pyams_app_msc.shared.catalog.interfaces import ICatalogEntry
from pyams_app_msc.shared.catalog.portlet.skin.interfaces import ICatalogViewItemsPortletPanelsRendererSettings
from pyams_catalog.query import CatalogResultSet
from pyams_content.shared.view.portlet.interfaces import IViewItemsPortletSettings
from pyams_content.shared.view.portlet.skin import ViewItemsPortletPanelsRenderer, \
    ViewItemsPortletPanelsRendererSettings
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.interfaces import IPortalContext, IPortletRenderer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config, get_interface_base_name
from pyams_utils.registry import get_utility
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@factory_config(ICatalogViewItemsPortletPanelsRendererSettings)
class CatalogViewItemsPortletPanelsRendererSettings(ViewItemsPortletPanelsRendererSettings):
    """Catalog view items portlet panels renderer settings"""

    display_sessions = FieldProperty(ICatalogViewItemsPortletPanelsRendererSettings['display_sessions'])
    sessions_weeks = FieldProperty(ICatalogViewItemsPortletPanelsRendererSettings['sessions_weeks'])
    display_free_seats = FieldProperty(ICatalogViewItemsPortletPanelsRendererSettings['display_free_seats'])


@adapter_config(name='catalog-panels',
                required=(IPortalContext, IPyAMSLayer, Interface, IViewItemsPortletSettings),
                provides=IPortletRenderer)
@template_config(template='templates/view-catalog-panels.pt',
                 layer=IPyAMSLayer)
class CatalogViewItemsPortletPanelsRenderer(ViewItemsPortletPanelsRenderer):
    """Catalog view items portlet catalog panels renderer"""

    label = _("Catalog entries with next planned sessions")
    weight = 40

    settings_interface = ICatalogViewItemsPortletPanelsRendererSettings

    def get_sessions(self, wf_entry):
        """Display incoming sessions for provided catalog entry"""
        entry = get_parent(wf_entry, ICatalogEntry)
        catalog = get_utility(ICatalog)
        intids = get_utility(IIntIds)
        now = tztime(datetime.utcnow())
        query = And(Eq(catalog['object_types'], get_interface_base_name(ISession)),
                    Eq(catalog['parents'], intids.queryId(entry)),
                    Ge(catalog['planning_start_date'], now),
                    Le(catalog['planning_end_date'], now + timedelta(weeks=self.renderer_settings.sessions_weeks)))
        yield from sorted(filter(lambda x: x.extern_bookable,
                                 CatalogResultSet(CatalogQuery(catalog).query(query))),
                          key=lambda x: x.start_date)

    def get_version(self, session):
        """Get displayed version of provided entry"""
        if not session.version:
            return ''
        version = VERSION_INFO_ABBR.get(VERSION_INFO(session.version))
        if not version:
            return ''
        translate = self.request.localizer.translate
        return f'- {translate(version)}'

    @staticmethod
    def get_free_seats(session):
        """Get free seats for provided session"""
        bookings = IBookingContainer(session, None)
        if bookings is None:
            return session.capacity, session.capacity
        return session.capacity - bookings.get_confirmed_seats(), session.capacity
