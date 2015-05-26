# -*- coding: utf-8 -*-
""" Modulo que implementa o viewlet de logo"""
from plone.app.layout.viewlets.common import LogoViewlet as ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class LogoViewlet(ViewletBase):
    ''' Viewlet de titulo para logo
    '''
    # Indica qual o template sera usado por este viewlet
    index = ViewPageTemplateFile('templates/logo.pt')

    def portal(self):
        ps = self.context.restrictedTraverse('@@plone_portal_state')
        portal = ps.portal()
        return portal

    def title(self):
        ''' Retorna o titulo do portal
        '''
        portal = self.portal()
        return getattr(portal, 'title', 'Nome do Site')

    def description(self):
        ''' Retorna uma breve descricao do portal
        '''
        portal = self.portal()
        return getattr(portal, 'description', '')
