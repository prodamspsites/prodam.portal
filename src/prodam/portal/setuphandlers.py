# -*- coding: utf-8 -*-


def importSteps(context):
    site = context.getSite()
    createMaisBuscados(site)


def createObj(site, objId, title, type, path, exclude_from_nav=False):
    try:
        parent = site.restrictedTraverse(path)
        if objId not in parent.objectIds():
            parent.invokeFactory(type, objId, title=title)
            obj = parent[objId]
            site.portal_workflow.doActionFor(obj, 'publish')
            obj.exclude_from_nav = exclude_from_nav
            site.portal_catalog.reindexObject(obj)
    except:
        pass


def createLinkObject(site, objId, title, path, url, exclude_from_nav=False):
    try:
        parent = site.restrictedTraverse(path)
        if objId not in parent.objectIds():
            parent.invokeFactory('Link', objId, title=title, remoteUrl=url)
            obj = parent[objId]
            site.portal_workflow.doActionFor(obj, 'publish')
            obj.exclude_from_nav = exclude_from_nav
            site.portal_catalog.reindexObject(obj)
    except:
        pass


def createChamada(site, objId, title, path, url, exclude_from_nav=False):
    try:
        parent = site.restrictedTraverse(path)
        if objId not in parent.objectIds():
            parent.invokeFactory('prodam.chamadas', objId, title=title, url=url)
            obj = parent[objId]
            site.portal_workflow.doActionFor(obj, 'publish')
            site.portal_catalog.reindexObject(obj)
            obj.exclude_from_nav = exclude_from_nav
    except:
        pass


def createMaisBuscados(site):
    createObj(site, 'img-admin', 'Imagens admin', 'Folder', '', exclude_from_nav=True)
    createObj(site, 'alertas', 'Alertas', 'Folder', '', exclude_from_nav=True)
    createObj(site, 'mais-buscados', 'Mais Buscados', 'Folder', '', exclude_from_nav=True)
    createChamada(site, 'iptu', 'IPTU', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwxMDc2LDExNDYsOTUx')
    createChamada(site, 'bilhete-unico', 'Bilhete Único', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwzOSw0MDgsNDE3LDEwNw')
    createChamada(site, 'consulta-itinerario', 'Consulta Itinerário', 'mais-buscados', 'http://www.sptrans.com.br/itinerarios/')
    createChamada(site, 'iluminacao-publica', 'Iluminação Pública', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwzMiw5ODUsMTE1Mg')
    createChamada(site, 'coleta-de-lixo', 'Coleta de Lixo', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwzMiwxMDUyLDExNTk=')
    createChamada(site, 'rede-municipal-de-saude', 'Rede municipal de saúde', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwzNiwxMTU0')
    createChamada(site, 'nota-fiscal-paulistana', 'Nota fiscal Paulistana', 'mais-buscados', '/portal/secoes/nav-empresa/#/MiwxMTU=')
    createChamada(site, 'construcoes-e-reformas', 'Construções e reformas', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwxMDc2LDExMjQ=')
    createChamada(site, 'vagas-em-escolas', 'Vagas em escolas', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwzNCw5MzMsNjIw')
    createChamada(site, 'operacao-cata-bagulho', 'Operação Cata-Bagulho', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwzMiwxMDUyLDExNjY=')
