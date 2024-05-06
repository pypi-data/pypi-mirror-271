#
# Copyright (c) 2015-2024 Thierry Florac <tflorac AT ulthar.net>
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

from pyramid.httpexceptions import HTTPForbidden, HTTPInternalServerError
from pyramid.view import view_config
from zope.copy import copy
from zope.interface import Interface

from pyams_app_msc.zmi import msc
from pyams_content.component.gallery import IGalleryContainer, IGalleryFile
from pyams_content.component.gallery.zmi import GalleryMediasViewlet, GalleryView
from pyams_content.component.illustration import IIllustration
from pyams_content.interfaces import MANAGE_CONTENT_PERMISSION
from pyams_content.shared.common import IWfSharedContent
from pyams_i18n.interfaces import INegotiator
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.permission import get_edit_permission
from pyams_skin.interfaces.viewlet import IContextActionsViewletManager
from pyams_skin.viewlet.actions import ContextAction
from pyams_template.template import override_template
from pyams_utils.registry import get_utility
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


@viewlet_config(name='set-content-illustration.action',
                context=IGalleryFile, layer=IAdminLayer, view=Interface,
                manager=IContextActionsViewletManager, weight=30,
                permission=MANAGE_CONTENT_PERMISSION)
class GalleryFileIllustrationGetter(ContextAction):
    """Gallery file illustration getter"""

    def __new__(cls, context, request, view, manager):
        gallery = get_parent(context, IGalleryContainer)
        if gallery is not None:
            edit_permission = get_edit_permission(request, context=gallery, view=view)
            if not request.has_permission(edit_permission, context=context):
                return None
        return ContextAction.__new__(cls)

    hint = _("Set as content illustration")
    css_class = 'btn-sm px-1'
    icon_class = 'fas fa-file-image'

    def get_href(self):
        """Icon URL getter"""
        return None

    click_handler = 'MyAMS.msc.catalog.setIllustrationFromGallery'

    def update(self):
        super().update()
        msc.need()


@view_config(name='set-content-illustration.json',
             context=IGalleryContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def set_content_illustration(request):
    """Set content illustration from medias gallery file"""
    translate = request.localizer.translate
    name = request.params.get('object_name')
    if not name:
        return {
            'status': 'message',
            'messagebox': {
                'status': 'error',
                'message': translate(_("No provided object_name argument!"))
            }
        }
    container = request.context
    if name not in container:
        return {
            'status': 'message',
            'messagebox': {
                'status': 'error',
                'message': translate(_("Given element name doesn't exist!"))
            }
        }
    content = get_parent(container, IWfSharedContent)
    if content is None:
        return {
            'status': 'message',
            'messagebox': {
                'status': 'error',
                'message': translate(_("Can't find illustration target!"))
            }
        }
    permission = get_edit_permission(request, content)
    if permission is None:
        raise HTTPInternalServerError("Missing permission definition!")
    if not request.has_permission(permission, context=content):
        raise HTTPForbidden()
    illustration = IIllustration(content, None)
    if illustration is None:
        return {
            'status': 'message',
            'messagebox': {
                'status': 'error',
                'message': translate(_("No illustration on content!"))
            }
        }
    media = container[name]
    negotiator = get_utility(INegotiator)
    illustration.title = media.title
    illustration.alt_title = media.alt_title
    illustration.description = media.description
    illustration.author = media.author
    illustration.data = {
        negotiator.server_language: copy(media.data)
    }
    return {
        'status': 'success',
        'message': translate(_("Content illustration has been updated successfully."))
    }


override_template(GalleryMediasViewlet,
                  template='templates/gallery-medias.pt',
                  layer=IAdminLayer)

override_template(GalleryView,
                  template='templates/gallery-view.pt',
                  layer=IAdminLayer)
