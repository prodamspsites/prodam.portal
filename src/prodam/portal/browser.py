# -*- coding: utf-8 -*-
from zope.site.hooks import getSite
from z3c.form import form
from z3c.form import button
from collective.transmogrifier.transmogrifier import Transmogrifier


class ImportForm(form.Form):

    @button.buttonAndHandler(u'Import News')
    def handle_import_news(self, action):
        transmogrifier = Transmogrifier(getSite())
        transmogrifier(u'news-import')
