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

from urllib.parse import urlencode

from zope.interface import Interface

from pyams_app_msc.feature.planning.interfaces import VERSION_INFO, VERSION_INFO_LABEL
from pyams_app_msc.shared.catalog import ICatalogEntryInfo, IWfCatalogEntry
from pyams_app_msc.shared.theater import IMovieTheater
from pyams_content.shared.common.portlet.interfaces import ISpecificitiesRenderer
from pyams_content.skin.interfaces import IPublicURL
from pyams_i18n.language import BASE_LANGUAGES
from pyams_layer.interfaces import IPyAMSLayer
from pyams_sequence.interfaces import ISequentialIdInfo
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.interfaces.url import ICanonicalURL
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import ViewContentProvider

from pyams_app_msc import _


@adapter_config(required=(IWfCatalogEntry, IPyAMSLayer, Interface),
                provides=ISpecificitiesRenderer)
@template_config(template='templates/specificities.pt', layer=IPyAMSLayer)
class CatalogEntrySpecificitiesRenderer(ViewContentProvider):
    """Catalog entry specificities renderer"""

    entry_info = None

    def update(self):
        super().update()
        self.entry_info = ICatalogEntryInfo(self.context, None)

    def render(self, template_name=''):
        if self.entry_info is None:
            return ''
        return super().render(template_name)

    def get_language(self, value):
        translate = self.request.localizer.translate
        return translate(BASE_LANGUAGES.get(value, _("(unknown)")))

    def get_version(self, value):
        translate = self.request.localizer.translate
        return translate(VERSION_INFO_LABEL.get(VERSION_INFO(value), _("(undefined)")))

    def get_duration(self, value):
        translate = self.request.localizer.translate
        hours = value // 60
        minutes = value % 60
        if hours == 0:
            return translate(_("{} minutes")).format(minutes)
        return translate(_("{}h {}min")).format(hours, minutes)


@adapter_config(required=(IWfCatalogEntry, IPyAMSLayer),
                provides=ICanonicalURL)
class CatalogEntryCanonicalURL(ContextRequestAdapter):
    """Catalog entry canonical URL"""

    def get_url(self, view_name=None, query=None):
        theater = get_parent(self.context, IMovieTheater)
        query = urlencode(query) if query else None
        return absolute_url(theater, self.request,
                            f"+/{ISequentialIdInfo(self.context).get_base_oid().strip()}"
                            f"::{self.context.content_url}"
                            f"{'/{}'.format(view_name) if view_name else '.html'}"
                            f"{'?{}'.format(query) if query else ''}")


@adapter_config(name='booking-new.html',
                required=(IWfCatalogEntry, IPyAMSLayer),
                provides=IPublicURL)
class CatalogEntryPublicURL(ContextRequestAdapter):
    """Catalog entry public URL"""

    def get_url(self):
        """Public URL getter"""
        return self.request.url
