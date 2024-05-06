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

from pyams_app_msc.shared.theater.interfaces import IMovieTheater
from pyams_app_msc.shared.theater.zmi.interfaces import IMovieTheaterCatalogPresentationMenu
from pyams_form.ajax import ajax_form_config
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.interfaces import MANAGE_TEMPLATE_PERMISSION
from pyams_portal.zmi.interfaces import IPortalContextPresentationMenu
from pyams_portal.zmi.presentation import PortalContextPresentationEditForm, PortalContextTemplateLayoutMenu, \
    PortalContextTemplateLayoutView
from pyams_viewlet.manager import viewletmanager_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem

from pyams_app_msc import _


@viewletmanager_config(name='catalog-presentation.menu',
                       context=IMovieTheater, layer=IAdminLayer,
                       manager=IPortalContextPresentationMenu, weight=30,
                       provides=IMovieTheaterCatalogPresentationMenu,
                       permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterCatalogPresentationMenu(NavigationMenuItem):
    """Movie theater catalog presentation menu"""

    label = _("Catalog presentation")
    icon_class = 'fas fa-film'
    href = '#catalog-presentation.html'


@ajax_form_config(name='catalog-presentation.html',
                  context=IMovieTheater, layer=IPyAMSLayer,
                  permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterCatalogPresentationEditForm(PortalContextPresentationEditForm):
    """Portal context footer presentation edit form"""

    title = _("Catalog template configuration")

    page_name = 'catalog'


@viewlet_config(name='catalog-template-layout.menu',
                context=IMovieTheater, layer=IAdminLayer,
                manager=IMovieTheaterCatalogPresentationMenu, weight=10,
                permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterCatalogTemplateLayoutMenu(PortalContextTemplateLayoutMenu):
    """Movie theater catalog template layout menu"""

    label = _("Catalog layout")
    href = '#catalog-template-layout.html'

    page_name = 'catalog'


@pagelet_config(name='catalog-template-layout.html',
                context=IMovieTheater, layer=IPyAMSLayer,
                permission=MANAGE_TEMPLATE_PERMISSION)
class MovieTheaterCatalogTemplateLayoutView(PortalContextTemplateLayoutView):
    """Movie theater catalog template layout view"""

    page_name = 'catalog'
