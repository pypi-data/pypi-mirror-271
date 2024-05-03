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

from ZODB.interfaces import IConnection
from persistent import Persistent
from zope.container.contained import Contained
from zope.location.interfaces import ISublocations
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.traversing.interfaces import ITraversable

from pyams_app_msc.interfaces import MANAGE_THEATER_PERMISSION
from pyams_app_msc.shared.theater import ICinemaAudienceContainerTarget, IMovieTheater
from pyams_app_msc.shared.theater.interfaces.audience import AUDIENCES_VOCABULARY, CINEMA_AUDIENCE_CONTAINER_KEY, \
    ICinemaAudience, ICinemaAudienceContainer
from pyams_catalog.utils import index_object
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.container import BTreeOrderedContainer
from pyams_utils.factory import factory_config
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config


@factory_config(ICinemaAudience)
class CinemaAudience(Persistent, Contained):
    """Cinema audience persistent class"""

    active = FieldProperty(ICinemaAudience['active'])
    name = FieldProperty(ICinemaAudience['name'])
    age_min = FieldProperty(ICinemaAudience['age_min'])
    age_max = FieldProperty(ICinemaAudience['age_max'])
    comment = FieldProperty(ICinemaAudience['comment'])
    contact = FieldProperty(ICinemaAudience['contact'])
    notepad = FieldProperty(ICinemaAudience['notepad'])


@factory_config(ICinemaAudienceContainer)
class CinemaAudienceContainer(BTreeOrderedContainer):
    """Cinema audience container persistent class"""

    def get_active_items(self):
        """Active items iterator"""
        yield from filter(lambda x: x.active, self.values())


@adapter_config(required=ICinemaAudienceContainerTarget,
                provides=ICinemaAudienceContainer)
def cinema_audience_container(context):
    """Cinema audience container adapter"""
    return get_annotation_adapter(context, CINEMA_AUDIENCE_CONTAINER_KEY,
                                  ICinemaAudienceContainer,
                                  name='++audience++')


@adapter_config(name='audience',
                required=ICinemaAudienceContainerTarget,
                provides=ITraversable)
class CinemaAudienceContainerTraverser(ContextAdapter):
    """Cinema audience container traverser"""

    def traverse(self, name, furtherPath):
        """Traverse target to audiences container"""
        return ICinemaAudienceContainer(self.context)


@adapter_config(name='audiences',
                required=ICinemaAudienceContainerTarget,
                provides=ISublocations)
class CinemaAudienceSublocations(ContextAdapter):
    """Cinema audiences sub-locations"""

    def sublocations(self):
        """Sub-locations getter"""
        yield from ICinemaAudienceContainer(self.context).values()


@adapter_config(required=ICinemaAudience,
                provides=IViewContextPermissionChecker)
class CinemaAudiencePermissionChecker(ContextAdapter):
    """Cinema audience permission checker"""

    edit_permission = MANAGE_THEATER_PERMISSION


@vocabulary_config(name=AUDIENCES_VOCABULARY)
class CinemaAudiencesVocabulary(SimpleVocabulary):
    """Cinema audiences vocabulary"""

    def __init__(self, context):
        terms = []
        theater = get_parent(context, IMovieTheater)
        if theater is not None:
            terms = sorted([
                SimpleTerm(item.__name__, title=item.name)
                for item in ICinemaAudienceContainer(theater).get_active_items()
            ], key=lambda x: x.title)
        super().__init__(terms)
