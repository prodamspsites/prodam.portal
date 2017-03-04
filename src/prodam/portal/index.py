from plone.indexer.decorator import indexer
from prodam.portal.interfaces import IProdamPortal


@indexer(IProdamPortal)
def autorIndexer(obj):
    if obj.autor is None:
        return None
    else:
        return obj.autor


@indexer(IProdamPortal)
def emExercicioIndexer(obj):
    if obj.habilita_agenda_exercicio is None:
        return None
    else:
        return obj.habilita_agenda_exercicio
