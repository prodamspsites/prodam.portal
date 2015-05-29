# -*- coding: utf-8 -*-
from plone.app.search.browser import Search as PloneSearch


class Search(PloneSearch):
    """Customize Plone Search
    """

    def rel(self):
        """Formata rel a ser utilizado no href de cada termo
        """
        return u'dc:subject foaf:primaryTopic'
