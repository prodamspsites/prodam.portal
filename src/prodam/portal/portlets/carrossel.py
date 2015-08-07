# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
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

    count = schema.Int(
        title=_(u'Number of items to show'),
        description=_(u'Total itens that should be displayed'),
        required=True,
        default=4)

    more = schema.TextLine(
        title=_(u'Youtube channel URL'),
        description=_(u'This is the view more link'),
        required=True)


class Assignment(base.Assignment):

    implements(iCarrossel)

    def __init__(self, header=u'', show_header=False, count=4, more=''):
        self.header = header
        self.show_header = show_header
        self.count = count
        self.more = more

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

    def getTitle(self):
        if self.data.header:
            return self.data.header
        else:
            return 'Youtube'

    def getMoreLink(self):
        return self.data.more

    @property
    def getVideos(self):
        count = self.data.count
        catalog = getToolByName(self, 'portal_catalog')
        videos = catalog(portal_type='Google Video', sort_on='Date', sort_order='Descending')[:count]
        return videos


class AddForm(base.AddForm):
    form_fields = form.Fields(iCarrossel)
    label = _(u'Add carrossel Portlet')
    description = _(u'Shows videos from youtube.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(iCarrossel)
    label = _(u'Editar portlet de carrossel')
    description = _(u'Shows videos from youtube')
