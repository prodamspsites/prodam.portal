# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from DateTime import DateTime

class Agenda(BrowserView):
    pass

    def getDate(self):
        try:
            requested_date = self.request.form["date"]
            start_date = DateTime(requested_date)
            end_date = DateTime(requested_date + ' 23:59:59')
            date_range_query = { 'query':(start_date,end_date), 'range': 'min:max'}
            events = self.context.portal_catalog(portal_type='Event',
                                                 start={'query': start_date,
                                                        'range': 'min'},
                                                 end={'query': end_date,
                                                      'range': 'max'},
                                                 sort_on='start',
                                                 review_state='published')
            return events
        except:
            return False

# from zope.component import getMultiAdapter

# plone = getMultiAdapter((self.context, self.request), name="plone")
# time = DateTime()

# return plone.toLocalizedTime(time)
