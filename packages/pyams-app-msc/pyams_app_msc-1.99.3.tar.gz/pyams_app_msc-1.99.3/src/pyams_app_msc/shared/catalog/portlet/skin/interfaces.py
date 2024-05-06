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

from zope.schema import Bool, Int

from pyams_content.shared.view.portlet.skin import IViewItemsPortletPanelsRendererSettings

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class ICatalogViewItemsPortletPanelsRendererSettings(IViewItemsPortletPanelsRendererSettings):
    """Catalog view items portlet panels renderers settings"""

    display_sessions = Bool(title=_("Display sessions"),
                            description=_("If 'no', incoming sessions will not be displayed"),
                            required=True,
                            default=True)

    sessions_weeks = Int(title=_("Sessions weeks"),
                         description=_("Number of weeks to display sessions"),
                         required=True,
                         default=4)

    display_free_seats = Bool(title=_("Display free seats"),
                              description=_("If 'no', number of free seats is not displayed"),
                              required=True,
                              default=True)
