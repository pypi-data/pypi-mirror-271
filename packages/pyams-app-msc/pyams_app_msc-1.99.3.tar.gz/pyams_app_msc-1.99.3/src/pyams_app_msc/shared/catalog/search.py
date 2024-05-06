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

from elasticsearch_dsl import Q
from hypatia.interfaces import ICatalog
from hypatia.query import Any

from pyams_content.shared.view.interfaces import IWfView
from pyams_content.shared.view.interfaces.query import IViewUserQuery
from pyams_content_es.shared.view.interfaces import IEsViewUserQuery
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.registry import get_utility


@adapter_config(name='audience',
                required=IWfView,
                provides=IViewUserQuery)
class CatalogAudienceQuery(ContextAdapter):
    """Catalog audience query"""

    @staticmethod
    def get_user_params(request):
        """User params getter"""
        audience = request.params.get('audience')
        if not audience:
            return
        if isinstance(audience, str):
            audience = audience.split(',')
        catalog = get_utility(ICatalog)
        yield Any(catalog['catalog_audience'], audience)


@adapter_config(name='audience',
                required=IWfView,
                provides=IEsViewUserQuery)
class EsCatalogAudienceQuery(ContextAdapter):
    """Elasticsearch catalog audience query"""

    @staticmethod
    def get_user_params(request):
        """User params getter"""
        audience = request.params.get('audience')
        if not audience:
            return
        if isinstance(audience, str):
            audience = audience.split(',')
        yield Q('terms',
                **{'catalog_info.audiences': audience})
