# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from DateTime import DateTime


class Agenda(BrowserView):

    def getDay(self):
        try:
            return self.form["date"]
        except:
            return DateTime().strftime('%m/%d/%Y')

    def getEvents(self):
        requested_date = self.getDay()
        start_date = DateTime(requested_date)
        end_date = DateTime(requested_date + ' 23:59:59')
        events = self.context.portal_catalog(portal_type='Event',
                                             start={'query': start_date,
                                                    'range': 'min'},
                                             end={'query': end_date,
                                                  'range': 'max'},
                                             sort_on='start',
                                             review_state='published')
        return events

    def getTitle(self):
        requested_date = DateTime(self.getDay())
        title = ''
        isToday = requested_date.isCurrentDay()
        title = isToday and 'HOJE: ' or title
        title += requested_date.strftime('%A, %d de %B de %Y')

        return title
