from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection
from zope.interface import classProvides
from zope.interface import implements


class AddTypeSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __iter__(self):
        for item in self.previous:
            path = item['title'].lower().replace(' ', '-')

            item['_path'] = '/Prefeitura/noticia/' + path
            item['_type'] = 'News Item'
            item['title'] = path
            item['description'] = path
            yield item
