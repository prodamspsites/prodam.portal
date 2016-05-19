# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets.calendar import Renderer as BaseRenderer


class Renderer(BaseRenderer):
    render = ViewPageTemplateFile('templates/calendar.pt')

    def checkIsDayEvent(self, day):
        day_event = self.request.get('day', 0)
        if(day_event == ''):
            return False
        if(int(day_event) == int(day)):
            return True
        else:
            return False
