# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from plone import api


class FooterPrefeitura(ViewletBase):

    def showCustomRodape(self):
        portal = api.portal.get()
        if 'rodape' in portal.objectIds():
            return True
        else:
            return False

    def getObjectInFooter(self, objPath):
        portal = api.portal.get()
        if 'rodape' in portal.objectIds():
            rodape = portal['rodape']
            obj = rodape.restrictedTraverse(objPath)
            return obj
        else:
            return False


class SPAgora(ViewletBase):
    pass
