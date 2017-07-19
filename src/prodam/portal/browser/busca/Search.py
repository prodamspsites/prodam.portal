# -*- coding: utf-8 -*-

from DateTime import DateTime
from plone.app.search.browser import Search

MULTISPACE = u'\u3000'.encode('utf-8')
EVER = DateTime('1970-01-03')


class SearchOrdered(Search):

    def results(self, query=None, batch=True, b_size=10, b_start=0):
        if query is None:
            query = {}
            query['sort_on'] = 'Date'
            query['sort_order'] = 'descending'
        return Search.results(self, query, batch, b_size, b_start)
