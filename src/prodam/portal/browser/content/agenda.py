# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from DateTime import DateTime
import locale
from prodam.portal.browser.content import configuracao
from plone import api


class Agenda(BrowserView):

    def getPrefeitoEmExercicio(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        print(session)
        if 'habilita_agenda_exercicio' in self.request:
            hae = self.request.form['habilita_agenda_exercicio']
            if hae == 'True':
                session.set("habilita_agenda_exercicio", True)
                return True
            else:
                session.set("habilita_agenda_exercicio", False)
                return False
        else:
            if 'habilita_agenda_exercicio' in session.keys():
                return session['habilita_agenda_exercicio']
            else:
                session.set("habilita_agenda_exercicio", True)
                return True

    def getDay(self):
        try:
            date = self.request.form['date']
            return date
        except:
            return DateTime().strftime('%m/%d/%Y')

    def getEvents(self):
        requested_date = self.getDay()
        start_date = DateTime(requested_date + ' 00:00')
        end_date = DateTime(requested_date + ' 23:59')
        exercicio = self.getPrefeitoEmExercicio()
        print('EXERCICIO: ' + str(exercicio))
        if exercicio:
            events = self.context.portal_catalog(portal_type='Event',
                                                 start={'query': [start_date, end_date], 'range': 'min:max'},
                                                 sort_on='start',
                                                 review_state='published',
                                                 habilita_agenda_exercicio=True)
        else:
            events = self.context.portal_catalog(portal_type='Event',
                                                 start={'query': [start_date, end_date], 'range': 'min:max'},
                                                 sort_on='start',
                                                 review_state='published',
                                                 habilita_agenda_exercicio=False)
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

    def getTitlePrefeito(self):
        year = self.getYearEvent()
        if year != '':
            if int(year) < 2017:
                return 'Prefeitos Anteriores'
            else:
                campo_aba_prefeito = self.getCampoAbaPrefeito()
                if campo_aba_prefeito is not None:
                    return campo_aba_prefeito.Title()
                else:
                    return u'Prefeito João Dória'
        else:
            campo_aba_prefeito = self.getCampoAbaPrefeito()
            if campo_aba_prefeito is not None:
                return campo_aba_prefeito.Title()
            else:
                return u'Prefeito João Dória'

    def getParametroConfiguracaoPrefeitoExercicio(self):
        res = configuracao.Configuracao.getParametroConfiguracaoPrefeitoExercicio()
        return res

    def getCampoAbaPrefeito(self):
        portal = api.portal.get()
        id = 'aba_prefeito'
        results = portal.portal_catalog(id=id, portal_type="aba_editavel")
        for i in results:
            return i.getObject()
        return None

    def getCampoAbaVice(self):
        portal = api.portal.get()
        id = 'aba_vice'
        results = portal.portal_catalog(id=id, portal_type="aba_editavel")
        for i in results:
            return i.getObject()
        return None

    def getCssClass(self):
        if self.getPrefeitoEmExercicio():
            return 'btn_agenda_ativo'
        else:
            return 'btn_agenda_inativo'
