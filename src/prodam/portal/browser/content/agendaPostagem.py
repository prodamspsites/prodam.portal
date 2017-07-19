# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from DateTime import DateTime
import locale


class AgendaPostagem(BrowserView):

    def getDay(self):
        try:
            date = self.request.form['date']
            return date
        except:
            return DateTime().strftime('%m/%d/%Y')

    def getPostagens(self):
        requested_date = self.getDay()
        start_date = DateTime(requested_date + ' 00:00')
        end_date = DateTime(requested_date + ' 23:59')
        try:
            events = self.context.portal_catalog(portal_type='agenda',
                                                 data_da_agenda={'query': [start_date, end_date], 'range': 'min:max'},
                                                 review_state='published')
            return events
        except Exception as inst:
            print("Erro na consulta de postagnes")
            print(inst)
            return []

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
