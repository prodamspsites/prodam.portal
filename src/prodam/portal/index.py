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


@indexer(IProdamPortal)
def nomePrefeitoIndexer(obj):
    if obj.nome_prefeito is None:
        return None
    else:
        return obj.nome_prefeito


@indexer(IProdamPortal)
def dataEventoIndexer(obj):
    if obj.data_evento is None:
        return None
    else:
        return obj.data_evento


@indexer(IProdamPortal)
def dataDaAgendaIndexer(obj):
    if obj.data_da_agenda is None:
        return None
    else:
        return obj.data_da_agenda
