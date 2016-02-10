# -*- coding: utf-8 -*-
from zope.interface import classProvides, implements
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection
from unicodedata import normalize


class NormalizaTitle(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous

    def __iter__(self):
        for item in self.previous:
            path = item['title'].lower().replace(' ', '-')
            path = normalize('NFKD', path.decode('utf-8')).encode('ASCII', 'ignore')
            item['_path'] = '/noticia/' + path
            item['_transitions'] = ('publish', )
            yield item
