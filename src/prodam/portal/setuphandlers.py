# -*- coding: utf-8 -*-


def importSteps(context):
    site = context.getSite()

    createObj(site, 'exemplo-de-subpasta', 'Exemplo de subpasta', 'Folder', 'governo_municipal/secretarias')
    createLinkObject(site, 'exemplo-de-link', 'Exemplo de link', '', 'http://localhost:8080/Prefeitura/secretaria-de-esportes')


def createObj(site, objId, title, type, path):
    try:
        parent = site.restrictedTraverse(path)
        if objId not in parent.objectIds():
            parent.invokeFactory(type, objId, title=title)
            obj = parent[objId]
            parent.portal_workflow.doActionFor(obj, 'publish')
            parent.portal_catalog.reindexObject(obj)
    except:
        pass


def createLinkObject(site, objId, title, path, url):
    try:
        parent = site.restrictedTraverse(path)
        if objId not in parent.objectIds():
            parent.invokeFactory('Link', objId, title=title, remoteUrl=url)
            obj = parent[objId]
            parent.portal_workflow.doActionFor(obj, 'publish')
            parent.portal_catalog.reindexObject(obj)
    except:
        pass


def updateDefaultObject(id, title):
    pass
