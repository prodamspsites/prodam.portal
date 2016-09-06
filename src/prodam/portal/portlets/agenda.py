# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implements
import locale


class iAgendaPrefeito(IPortletDataProvider):

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
        title=_(u'Agenda URL'),
        description=_(u'This is the view more link'),
        required=True)


class Assignment(base.Assignment):

    implements(iAgendaPrefeito)

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
            return 'Agenda do Prefeito'


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/agenda.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def render(self):
        return self._template()

    def getPortletTitle(self):
        if self.data.header:
            return self.data.header
        else:
            return 'Youtube'

    def getMoreLink(self):
        return self.data.more

    def getEvents(self):
        requested_date = DateTime().strftime('%m/%d/%Y')
        start_date = DateTime(requested_date + ' 00:00')
        end_date = DateTime(requested_date + ' 23:59')
        events = self.context.portal_catalog(portal_type='Event',
                                             start={'query': [start_date, end_date],
                                                    'range': 'min:max'},
                                             sort_on='start',
                                             review_state='published')
        return events

    def getYearEvent(self):
        if('year' in self.request):
            return self.request.form['year']
        else:
            return ''

    def getMonthEvent(self):
        if('month' in self.request):
            return self.request.form['month']
        else:
            return ''

    def getDayEvent(self):
        if('day' in self.request):
            return self.request.form['day']
        else:
            return ''

    def getTitle(self):
        requested_date = DateTime(self.getDay())
        locale.setlocale(locale.LC_TIME, "pt_BR")
        title = ''
        isToday = requested_date.isCurrentDay()
        title = isToday and 'HOJE: ' or title
        encode_data_iso = unicode(requested_date.strftime('%A, %d de %B de %Y'), 'iso-8859-1')
        title += encode_data_iso
        return title


class AddForm(base.AddForm):
    form_fields = form.Fields(iAgendaPrefeito)
    label = _(u'Add agenda portlet')
    description = _(u'Shows events.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(iAgendaPrefeito)
    label = _(u'Editar portlet de agenda')
    description = _(u'Shows events')
