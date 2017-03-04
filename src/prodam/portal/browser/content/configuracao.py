# -*- coding: utf-8 -*

from plone import api
"""Esta classe é responsável por implementar e controlar certas configurações que permitem que o sistema se comporte
de acordo com estas configurações.
Geralmente, uma vez implementados, estes parâmetros são configuráveis na seguinte tela:
http://adm.capital.sp.gov.br/admin-alertas
"""


class Configuracao:
    @staticmethod
    def IdParametroConfiguracaoAbreDashboard():
        return 'habilita-dashboard'

    @staticmethod
    def getParametroConfiguracaoAbreDashboard():
        portal = api.portal.get()
        id = Configuracao.IdParametroConfiguracaoAbreDashboard()
        results = portal.portal_catalog(id=id, portal_type="parametro_de_configuracao")
        for i in results:
            return i.getObject()
        return None

    @staticmethod
    def setParametroConfiguracaoAbreDashboard(habilita):
        portal = api.portal.get()
        try:
            id = Configuracao.IdParametroConfiguracaoAbreDashboard()
            results = portal.portal_catalog(id=id, portal_type="parametro_de_configuracao")
            for i in results:
                i.getObject().habilitado = habilita
                portal.portal_catalog.reindexObject(i.getObject())
        except:
            pass

    @staticmethod
    def IdParametroConfiguracaoPrefeitoExercicio():
        return 'prefeito-exercicio'

    @staticmethod
    def getParametroConfiguracaoPrefeitoExercicio():
        portal = api.portal.get()
        id = Configuracao.IdParametroConfiguracaoPrefeitoExercicio()
        results = portal.portal_catalog(id=id, portal_type="parametro_de_configuracao")
        for i in results:
            return i.getObject()
        return None

    @staticmethod
    def setParametroConfiguracaoPrefeitoExercicio(habilita):
        portal = api.portal.get()
        try:
            id = Configuracao.IdParametroConfiguracaoPrefeitoExercicio()
            results = portal.portal_catalog(id=id, portal_type="parametro_de_configuracao")
            for i in results:
                i.getObject().habilitado = habilita
                portal.portal_catalog.reindexObject(i.getObject())
        except:
            pass
