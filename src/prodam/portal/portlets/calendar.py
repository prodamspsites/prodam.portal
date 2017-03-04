# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets.calendar import Renderer as BaseRenderer
from Products.CMFCalendar.CalendarTool import calendar
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
# from zope.component import getMultiAdapter
from Products.CMFPlone.utils import safe_unicode


class Renderer(BaseRenderer):
    render = ViewPageTemplateFile('templates/calendar.pt')

    def getPrefeitoEmExercicio(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        if 'habilita_agenda_exercicio' in session.keys():
            return session['habilita_agenda_exercicio']
        else:
            return True

    def checkIsDayEvent(self, day):
        day_event = self.request.get('day', 0)
        if(day_event == ''):
            return False
        if(int(day_event) == int(day)):
            return True
        else:
            return False

    def _getCalendar(self):
        """ Wrapper to ensure we set the first day of the week every time
        """
        calendar.setfirstweekday(6)
        return calendar

    def isToday(self, day):
        """Returns True if the given day and the current month and year equals
           today, otherwise False.
        """
        return self.now[2] == day and self.now[1] == self.month and self.now[0] == self.year

    def getEventsForCalendar(self, month='1', year='2002'):
        context = aq_inner(self.context)
        year = self.year
        month = self.month
        # portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        # navigation_root_path = portal_state.navigation_root_path()
        weeks = self.getEventsForCatalog(month, year)
        for week in weeks:
            for day in week:
                daynumber = day['day']
                if daynumber == 0:
                    continue
                day['is_today'] = self.isToday(daynumber)
                if day['event']:
                    cur_date = DateTime(year, month, daynumber)
                    localized_date = [self._ts.ulocalized_time(cur_date, context=context, request=self.request)]
                    day['eventstring'] = '\n'.join(localized_date + [' %s' % self.getEventString(e) for e in day['eventslist']])
                    day['date_string'] = '%s-%s-%s' % (year, month, daynumber)
        return weeks

    def getEventString(self, event):
        start = event['start'] and ':'.join(event['start'].split(':')[:2]) or ''
        end = event['end'] and ':'.join(event['end'].split(':')[:2]) or ''
        title = safe_unicode(event['title']) or u'event'

        if start and end:
            eventstring = "%s-%s %s" % (start, end, title)
        elif start:  # can assume not event['end']
            eventstring = "%s - %s" % (start, title)
        elif event['end']:  # can assume not event['start']
            eventstring = "%s - %s" % (title, end)
        else:  # can assume not event['start'] and not event['end']
            eventstring = title

        return eventstring

    def getEventsForCatalog(self, month='1', year='2002'):
        """ recreates a sequence of weeks, by days each day is a mapping.
            {'day': #, 'url': None}
        """
        year = int(year)
        month = int(month)
        # daysByWeek is a list of days inside a list of weeks, like so:
        # [[0, 1, 2, 3, 4, 5, 6],
        #  [7, 8, 9, 10, 11, 12, 13],
        #  [14, 15, 16, 17, 18, 19, 20],
        #  [21, 22, 23, 24, 25, 26, 27],
        #  [28, 29, 30, 31, 0, 0, 0]]
        daysByWeek = self._getCalendar().monthcalendar(year, month)
        weeks = []

        events = self.buscaEventosPorData(year, month)

        for week in daysByWeek:
            days = []
            for day in week:
                if day in events:
                    days.append(events[day])
                else:
                    days.append({'day': day, 'event': 0, 'eventslist': []})

            weeks.append(days)

        return weeks

    """
       Sobrescrita do método que efetivamente faz a busca:
       Products.CMFCalendar-2.2.3-py2.7.egg/Products/CMFCalendar/CalendarTool.py
    """
    def buscaEventosPorData(self, year, month):
        """ given a year and month return a list of days that have events
        """
        # XXX: this method violates the rules for tools/utilities:
        # it depends on a non-utility tool
        year = int(year)
        month = int(month)
        last_day = self._getCalendar().monthrange(year, month)[1]
        first_date = self.getBeginAndEndTimes(1, month, year)[0]
        last_date = self.getBeginAndEndTimes(last_day, month, year)[1]

        ctool = getToolByName(self, 'portal_catalog')

        habilita_agenda_exercicio = self.getPrefeitoEmExercicio()

        query = ctool(portal_type=('Event',),
                      review_state=('published',),
                      start={'query': last_date, 'range': 'max'},
                      end={'query': first_date, 'range': 'min'},
                      sort_on='start',
                      habilita_agenda_exercicio=habilita_agenda_exercicio)

        # compile a list of the days that have events
        eventDays = {}
        for daynumber in range(1, 32):  # 1 to 31
            eventDays[daynumber] = {'eventslist': [],
                                    'event': 0,
                                    'day': daynumber}
        includedevents = []
        for result in query:
            if result.getRID() in includedevents:
                break
            else:
                includedevents.append(result.getRID())
            event = {}
            # we need to deal with events that end next month
            if result.end.greaterThan(last_date):
                eventEndDay = last_day
                event['end'] = None
            else:
                eventEndDay = result.end.day()
                if result.end == result.end.earliestTime():
                    event['end'] = (result.end - 1).latestTime().Time()
                else:
                    event['end'] = result.end.Time()
            # and events that started last month
            if result.start.lessThan(first_date):
                eventStartDay = 1
                event['start'] = None
            else:
                eventStartDay = result.start.day()
                event['start'] = result.start.Time()

            event['title'] = result.Title or result.getId

            if eventStartDay != eventEndDay:
                allEventDays = range(eventStartDay, eventEndDay + 1)
                eventDays[eventStartDay]['eventslist'].append({'end': None,
                                                               'start': result.start.Time(),
                                                               'title': event['title']})
                eventDays[eventStartDay]['event'] = 1

                for eventday in allEventDays[1:-1]:
                    eventDays[eventday]['eventslist'].append(
                        {'end': None,
                         'start': None,
                         'title': event['title']})
                    eventDays[eventday]['event'] = 1

                if (result.end == result.end.earliestTime() and event['end'] is not None):
                    # ends some day this month at midnight
                    last_day_data = eventDays[allEventDays[-2]]
                    last_days_event = last_day_data['eventslist'][-1]
                    last_days_event['end'] = (result.end - 1).latestTime().Time()
                else:
                    eventDays[eventEndDay]['eventslist'].append(
                        {'end': event['end'],
                         'start': None,
                         'title': event['title']})
                    eventDays[eventEndDay]['event'] = 1
            else:
                eventDays[eventStartDay]['eventslist'].append(event)
                eventDays[eventStartDay]['event'] = 1
            # This list is not uniqued and isn't sorted
            # uniquing and sorting only wastes time
            # and in this example we don't need to because
            # later we are going to do an 'if 2 in eventDays'
            # so the order is not important.
            # example:  [23, 28, 29, 30, 31, 23]
        return eventDays

    def getBeginAndEndTimes(self, day, month, year):
        """ Get two DateTime objects representing the beginning and end
        of the given day
        """
        day = int(day)
        month = int(month)
        year = int(year)

        begin = DateTime('%d/%02d/%02d 00:00:00' % (year, month, day))
        end = DateTime('%d/%02d/%02d 23:59:59' % (year, month, day))

        return (begin, end)
