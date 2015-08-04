# -*- coding: utf-8 -*-

from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implements


class iCarrossel(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u'Portlet header'),
        description=_(u'Title of the rendered portlet'),
        required=True)

    show_header = schema.Bool(
        title=_(u'Show portlet header'),
        description=_(u''),
        required=True,
        default=False)

    urls = schema.Text(
        title=_(u'URL dos Vídeos'),
        description=_(u'Lista com links dos vídeos a serem exibidos'),
        required=True)


class Assignment(base.Assignment):

    implements(iCarrossel)

    def __init__(self, header=u'', show_header=False, urls=None):
        self.header = header
        self.show_header = show_header
        self.urls = urls

    @property
    def title(self):
        if self.header:
            return self.header
        else:
            return 'Youtube'


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/carrossel.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def render(self):
        return self._template()

    @property
    def getVideos(self):
        return self.data.urls


class AddForm(base.AddForm):
    form_fields = form.Fields(iCarrossel)
    label = _(u'Add carrossel Portlet')
    description = _(u'Exibe vídeos em carrossel.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(iCarrossel)
    label = _(u'Editar portlet de carrossel')
    description = _(u'Exibe vídeos em carrossel.')
