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

"""PyAMS_app_msc.feature.profile.skin module

"""

from zope.interface import Interface

from pyams_app_msc.feature.profile import IUserProfile
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.form import EditForm
from pyams_form.interfaces.form import IAJAXFormRenderer, IFormContent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_portal.skin.page import PortalContextIndexPage
from pyams_security.interfaces import LOGIN_REFERER_KEY
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@ajax_form_config(name='my-profile.html',
                  layer=IPyAMSLayer)
class UserProfileEditForm(EditForm, PortalContextIndexPage):
    """User profile edit form"""

    title = _("My user profile")
    legend = _("Account settings")

    fields = Fields(IUserProfile).omit('active')

    def update_actions(self):
        super().update_actions()
        action = self.actions.get('apply')
        if action is not None:
            action.add_class('btn-primary')

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        email = self.widgets.get('email')
        if email is not None:
            email.readonly = 'readonly'


@adapter_config(required=(Interface, IPyAMSLayer, UserProfileEditForm),
                provides=IFormContent)
def user_profile_edit_form_content(context, request, form):
    """User profile edit form content getter"""
    return IUserProfile(request)


@adapter_config(required=(Interface, IPyAMSLayer, UserProfileEditForm),
                provides=IAJAXFormRenderer)
class UserProfileEditFormRenderer(ContextRequestViewAdapter):
    """User profile edit form renderer"""

    def render(self, changes):
        result = {
            'status': 'redirect'
        }
        session = self.request.session
        if LOGIN_REFERER_KEY in session:
            result['location'] = f"{session[LOGIN_REFERER_KEY] or '/'}"
            del session[LOGIN_REFERER_KEY]
        else:
            result['location'] = '/'
        return result
