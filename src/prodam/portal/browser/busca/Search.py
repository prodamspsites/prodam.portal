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

    def types_list(self):
        lista_tipos_conteudo = Search.types_list(self)
        lista_tipos_validos = []
        return self.tipos_permitidos
        for item in lista_tipos_conteudo:
            if item in self.tipos_permitidos:
                lista_tipos_validos.append(item)
        return lista_tipos_validos

    def filter_query(self, query):
        qr = Search.filter_query(self, query)
        lista_tipos_conteudo = qr['portal_type']
        lista_tipos_validos = []
        for item in lista_tipos_conteudo:
            if item in self.tipos_permitidos:
                lista_tipos_validos.append(item)
        # qr['portal_type'] = lista_tipos_validos
        # print(qr)
        return qr

    @property
    def tipos_permitidos(self):
        lista_tipos_permitidos = ['News Item', 'service', 'Document', 'Link', 'section', 'Event', 'topic', 'Image', 'Google Video']
        return lista_tipos_permitidos
