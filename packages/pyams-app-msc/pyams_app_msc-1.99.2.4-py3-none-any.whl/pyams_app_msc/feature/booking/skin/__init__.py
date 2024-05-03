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

from pyramid.decorator import reify
from zope.interface import Interface
from zope.schema import Bool, Text, TextLine

from pyams_app_msc.feature.booking import IBookingContainer, IBookingInfo
from pyams_app_msc.feature.planning import IPlanning, IPlanningTarget
from pyams_app_msc.feature.planning.interfaces import VERSION_INFO_VOCABULARY
from pyams_app_msc.interfaces import CREATE_BOOKING_PERMISSION
from pyams_form.ajax import ajax_form_config
from pyams_form.button import Buttons, handler
from pyams_form.field import Fields
from pyams_form.form import AddForm
from pyams_form.interfaces import HIDDEN_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.skin.page import PortalContextIndexPage
from pyams_skin.interfaces.viewlet import IFormHeaderViewletManager
from pyams_skin.schema.button import SubmitButton
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.date import format_datetime
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import Viewlet, viewlet_config

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


class IBookingAddFormInfo(IBookingInfo):
    """Booking add form interface"""

    session_id = TextLine(title=_("Session ID"),
                          required=True)

    comments = Text(title=_("Comments"),
                    description=_("You can add optional comments to your booking request"),
                    required=False)

    send_confirmation = Bool(title=_("Get confirmation message?"),
                             description=_("If 'yes', a confirmation message will be sent to you to "
                                           "acknowledge the booking"),
                             required=True,
                             default=True)


class IBookingAddFormButtons(Interface):
    """Booking add form buttons interface"""

    add = SubmitButton(name='add',
                       title=_("Add booking for this session"))


@ajax_form_config(name='booking-new.html',
                  context=IPlanningTarget, layer=IPyAMSLayer,
                  permission=CREATE_BOOKING_PERMISSION)
class BookingAddForm(AddForm, PortalContextIndexPage):
    """Booking add form"""

    legend = _("Your new booking properties")

    fields = Fields(IBookingAddFormInfo).select('session_id', 'nb_participants',
                                                'nb_accompanists', 'nb_groups', 'cultural_pass',
                                                'comments', 'send_confirmation')
    buttons = Buttons(IBookingAddFormButtons)

    content_factory = IBookingInfo
    _edit_permission = CREATE_BOOKING_PERMISSION

    @reify
    def session(self):
        """Session getter"""
        session_id_widget = self.widgets.get('session_id')
        if session_id_widget is not None:
            session_id = session_id_widget.value
        else:
            session_id = self.request.params.get('session_id')
        if session_id:
            planning = IPlanning(self.context)
            return planning.get(session_id)
        return None

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        session_id = self.widgets.get('session_id')
        if session_id is not None:
            session_id.mode = HIDDEN_MODE
            if 'session_id' in self.request.params:
                session_id.value = self.request.params['session_id']

    @handler(buttons['add'])
    def handle_add(self, action):
        super().handle_add(self, action)

    def update_content(self, obj, data):
        data = data.get(self, data)
        for name in ('nb_participants', 'nb_accompanists', 'nb_groups', 'cultural_pass',
                     'comments', 'send_confirmation'):
            setattr(obj, name, data.get(name))
        obj.recipient = self.request.principal.id
        obj.creator = self.request.principal.id

    def add(self, obj):
        del obj.session
        container = IBookingContainer(self.session, None)
        if container is not None:
            container.append(obj)


@viewlet_config(name='booking-new.header',
                context=IPlanningTarget, layer=IPyAMSLayer, view=BookingAddForm,
                manager=IFormHeaderViewletManager, weight=10)
@template_config(template='templates/booking-new-header.pt',
                 layer=IPyAMSLayer)
class NewBookingHeader(Viewlet):
    """New booking header viewlet"""

    @property
    def start_date(self):
        start_date = self.view.session.start_date
        return format_datetime(start_date)

    def get_version(self):
        version = VERSION_INFO_VOCABULARY.by_value.get(self.view.session.version)
        if not version:
            return None
        return self.request.localizer.translate(version.title)


@adapter_config(required=(IPlanningTarget, IPyAMSLayer, BookingAddForm),
                provides=IAJAXFormRenderer)
class BookingAddFormRenderer(ContextRequestViewAdapter):
    """Booking add form renderer"""

    def render(self, changes):
        if changes is None:
            return
        return {
            'status': 'redirect',
            'location': absolute_url(self.context, self.request, 'booking-ok.html')
        }


@pagelet_config(name='booking-ok.html',
                layer=IPyAMSLayer)
@template_config(template='templates/booking-ok.pt',
                 layer=IPyAMSLayer)
class BookingOKView(PortalContextIndexPage):
    """Booking acknowledge view"""
