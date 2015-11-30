# -*- coding: utf-8 -*-
from Products.Five import BrowserView


class Agenda(BrowserView):
    pass

    def getDate(self):
        try:
            date = self.request.form["date"]
            return date
        except:
            return False

# from DateTime import DateTime
# from zope.component import getMultiAdapter

# plone = getMultiAdapter((self.context, self.request), name="plone")
# time = DateTime()

# return plone.toLocalizedTime(time)
