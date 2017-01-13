from plone.indexer.decorator import indexer
from prodam.portal.interfaces import IProdamPortal


@indexer(IProdamPortal)
def autorIndexer(obj):
    if obj.autor is None:
        return None
    else:
        return obj.autor
