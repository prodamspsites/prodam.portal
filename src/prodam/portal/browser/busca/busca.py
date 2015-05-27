# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Acquisition import aq_inner
from plone.app.search.browser import Search as PloneSearch
from urllib import urlencode
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory


class Search(PloneSearch):
    """Customize Plone Search
    """

    def rel(self):
        """Formata rel a ser utilizado no href de cada termo
        """
        return u'dc:subject foaf:primaryTopic'
