from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection
from zope.interface import classProvides
from zope.interface import implements
from DateTime import DateTime


class AddTypeSection(object):
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
            item['_path'] = '/noticia/' + str(path)
            item['_folder'] = '/noticia/' + str(path)
            item['_creator'] = 'secom'
            item['_ExpirationDate'] = DateTime("2016-02-02")
            item['_transitions'] = ('publish',)
            yield item
