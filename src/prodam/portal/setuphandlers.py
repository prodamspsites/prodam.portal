# -*- coding: utf-8 -*-


def importSteps(context):
    site = context.getSite()

    createObject(site, site, 'governo_municipal', 'Folder')

    createObject(site, site, 'consultas', 'Folder')

    createObject(site, 'governo_municipal', 'secretarias', 'Folder')

    createObject(site, 'governo_municipal', 'sub-prefeituras', 'Folder')
    createObject(site, 'governo_municipal', 'outros-orgaos', 'Folder')


def createObject(site, parent, id, portal_type):
    parent = site.restrictedTraverse(parent)
    if id not in parent.objectIds():
        parent.invokeFactory(portal_type, id)


def updateLinkObject(id, title, url):
    pass


def updateDefaultObject(id, title):
    pass
