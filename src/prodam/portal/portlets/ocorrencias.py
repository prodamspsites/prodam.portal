# -*- coding: utf-8 -*-

from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implements
from twitter import Api
from pymongo import MongoClient

from time import strptime, mktime, localtime
from zope.i18n import translate


class iOcorrencias(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u'Portlet header'),
        description=_(u'Title of the rendered portlet'),
        required=True)

    show_header = schema.Bool(
        title=_(u'Show portlet header'),
        description=_(u''),
        required=True,
        default=False)

    user = schema.TextLine(
        title=_(u'Twitter user name'),
        description=_(u''),
        required=False)

    count = schema.TextLine(
        title=_(u'Number of tweets to show'),
        description=_(u''),
        required=False)

    consumer_key = schema.TextLine(
        title=_(u'Twitter Consumer key'),
        description=_(u'Used by twitter API'),
        required=False)

    consumer_secret = schema.TextLine(
        title=_(u'Twitter Consumer secret'),
        description=_(u'Used by twitter API'),
        required=False)

    access_token = schema.TextLine(
        title=_(u'Access token'),
        description=_(u'Used by twitter API'),
        required=False)

    token_secret = schema.TextLine(
        title=_(u'Access token secret'),
        description=_(u'Used by twitter API'),
        required=False)

    hide = schema.Bool(
        title=_(u'Hide portlet'),
        description=_(u'Tick this box if you want to temporarily hide '
                      'the portlet without losing your information.'),
        required=True,
        default=False)


class Assignment(base.Assignment):

    implements(iOcorrencias)

    def __init__(self, header=u'', show_header=False, user=None, count=None, consumer_key=None, consumer_secret=None, access_token=None, token_secret=None, fax=None, hide=False):
        self.header = header
        self.show_header = show_header
        self.user = user
        self.count = count
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.token_secret = token_secret
        self.hide = hide

    @property
    def title(self):
        if self.header:
            return self.header
        else:
            return 'Twitter'


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/twitter.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return not self.data.hide
    """
    def getTweets(self):
        api = Api(consumer_key=self.data.consumer_key, consumer_secret=self.data.consumer_secret, access_token_key=self.data.access_token, access_token_secret=self.data.token_secret)
        try:
            api.VerifyCredentials()
            statuses = api.GetUserTimeline(screen_name=self.data.user)[:int(self.data.count)]
            ocorrencias = []

            for i in statuses:
                status = '<a href="https://twitter.com/' + self.data.user + '/statuses/' + str(i.id) + '" target="_blank">'
                status += '<time>' + str(i.relative_created_at) + '</time><p>' + str(i.text) + '</p></a>'
                ocorrencias.append(status)
            return ocorrencias
        except:
            return False
    """

    def getTweets(self):
        mongo_client = MongoClient('mongodb://mongo0.prodam:27017')
        database = mongo_client.prodam
        tweets = database.tweets.find()
        if tweets.count > 0:
            ocorrencias = []
            for i in tweets:
                print i
                text = ""
                try:
                    dtt = str(i["created_at"])
                    dtf = self.relative_time(str(self.converteTweetData(dtt)))
                except:
                    dtf = False

                if dtf:
                    text = '<a href="' + i["url"] + '" target="_blank"> <time>' + dtf + '</time><p>' + str(i["text"]) + '</p></a>'
                else:
                    text = '<a href="' + i["url"] + '" target="_blank"><p>' + str(i["text"]) + '</p></a>'

                ocorrencias.append(text)
            return ocorrencias

    def getTitle(self):
        if self.data.header:
            return self.data.header
        else:
            return 'twitter'

    def relative_time(self, dateString, currentTime=None):
        """Take the created_at timestamp string and convert
        it to a relative text expression
        """
        _partialMinute = 45 * 60
        _partialHour = 90 * 60
        _fullDay = 24 * 60 * 60
        _twoDays = _fullDay * 2
        if currentTime is not None:
            now = currentTime
        else:
            now = mktime(localtime())
        import math
        date = dateString.replace(' +0000', '')
        parsed = mktime(strptime(date, '%a %b %d %H:%M:%S %Y'))
        delta = now - parsed
        if delta < 60:
            return translate('Há 1 minuto')
        elif delta < 120:
            return translate('Há 2 minuto')
        elif delta < _partialMinute:
            return translate('Há %d minutos') % (delta / 60)
        elif delta < _partialHour:
            return translate('Há 1 hora atrás')
        elif delta < _fullDay:
            d = math.ceil(delta / 3600)
            return translate('Há %d horas atrás') % d
        elif delta < _twoDays:
            return translate('Há 1 dia atrás')
        else:
            return translate('Há %d dias atrás') % (delta / 86400)

    def converteTweetData(self, dt):
        import datetime
        try:
            import pytz
            eastern = pytz.timezone('America/Sao_Paulo')
            test2 = datetime.datetime.strptime(str(dt), '%a %b %d %H:%M:%S +0000 %Y')
            test3 = pytz.utc.localize(test2)
            test4 = test3.astimezone(eastern)
            return test4.strftime('%a %b %d %H:%M:%S +0000 %Y')
        except:
            print('NAO FOI POSSIVEL IMPORTAR BIBLIOTECA PYTZ')


class AddForm(base.AddForm):
    form_fields = form.Fields(iOcorrencias)
    label = _(u'Add Events Portlet')
    description = _(u'Show last events')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(iOcorrencias)
    label = _(u'Edit Events Portlet')
    description = _(u'Show last events')
