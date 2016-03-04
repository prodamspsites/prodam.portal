# -*- coding: utf-8 -*

from Products.Five import BrowserView
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone import api
from DateTime import DateTime
from datetime import datetime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class Admin(BrowserView):
    def getHref(self):
        try:
            href = self.request.form['href']
        except:
            href = None
        return href


class createAlertas(BrowserView):
    def __call__(self):
        img = self.getImg() or None
        titulo = self.getTitulo() or None
        descricao = self.getDescricao() or None
        start = self.getStart() or None
        end = self.getEnd() or None
        if img and titulo:
            self.createAlerta(img, titulo, descricao, start, end)

    def createAlerta(self, img, titulo, descricao, start, end):
        portal = api.portal.get()
        folder = portal['alertas']
        cleanID = getUtility(IIDNormalizer)
        objID = 'alerta-' + cleanID.normalize(str(DateTime()))
        if start and end:
            start = DateTime(start)
            end = DateTime(end)
            folder.invokeFactory('alerta', objID, titulo=titulo, descricao=descricao, img=img, start=datetime(start.year(), start.month(), start.day(), start.hour(), start.minute()), end=datetime(end.year(), end.month(), end.day(), end.hour(), end.minute()))
            obj = folder[objID]
            obj.exclude_from_nav = True
            portal.portal_workflow.doActionFor(obj, 'publish')
            obj.setEffectiveDate(DateTime())
            obj.setExpirationDate(end)
            portal.portal_catalog.reindexObject(obj)
        else:
            folder.invokeFactory('alerta', objID, titulo=titulo, descricao=descricao, img=img)
            obj = folder[objID]
            obj.exclude_from_nav = True
            portal.portal_workflow.doActionFor(obj, 'publish')
            obj.setEffectiveDate(DateTime())
            portal.portal_catalog.reindexObject(obj)

    def getImg(self):
        try:
            img = self.request.form['img']
        except:
            img = None
        return img

    def getTitulo(self):
        try:
            titulo = self.request.form['titulo']
        except:
            titulo = None
        return titulo

    def getDescricao(self):
        try:
            descricao = self.request.form['descricao']
        except:
            descricao = None
        return descricao

    def getStart(self):
        try:
            start = self.request.form['start']
        except:
            start = None
        return start

    def getEnd(self):
        try:
            end = self.request.form['end']
        except:
            end = None
        return end


class SPAgora(BrowserView):
    pass


class SPAgoraEditar(BrowserView):
    def __call__(self):
        painelid, propertyTitle, propertyText = self.getPainelId()
        titulo = self.getTitulo() or None
        ativarEdicao = self.getAtivarEdicao() or None
        texto = self.getTexto() or None
        editar = self.getEditar() or None
        portal = api.portal.get()
        if painelid and titulo and editar:
            self.createTitulo(portal, propertyTitle, titulo)
            if ativarEdicao and texto:
                self.createTexto(portal, propertyText, texto)
        if editar and painelid and not ativarEdicao:
            self.delTitulo(portal, propertyText)
        if editar and painelid and not titulo:
            self.delTitulo(portal, propertyTitle)
        return ViewPageTemplateFile('templates/admin/spagora_editar_painel.pt')(self)

    def getPainelId(self):
        try:
            painelid = self.request.form['painelid']
            propertyTitle = painelid + '-titulo'
            propertyText = painelid + '-texto'
        except:
            painelid = None
            propertyTitle = None
            propertyText = None
        return painelid, propertyTitle, propertyText

    def getTitulo(self):
        try:
            titulo = self.request.form['titulo']
        except:
            titulo = None
        return titulo

    def getAtivarEdicao(self):
        try:
            ativarEdicao = self.request.form['ativarEdicao']
        except:
            ativarEdicao = None
        return ativarEdicao

    def getTexto(self):
        try:
            texto = self.request.form['texto']
        except:
            texto = None
        return texto

    def getEditar(self):
        try:
            editar = self.request.form['editar']
        except:
            editar = None
        return editar

    def getPainelTitulo(self):
        try:
            painelid = self.request.form["id"]
        except:
            painelid = ''
        portal = api.portal.get()
        propertyTitle = painelid + '-titulo'
        print propertyTitle
        if portal.hasProperty(propertyTitle):
            return portal.getProperty(propertyTitle)
        else:
            return ''

    def getPainelText(self):
        try:
            painelid = self.request.form["id"]
        except:
            painelid = ''
        portal = api.portal.get()
        propertyTitle = painelid + '-texto'
        print propertyTitle
        if portal.hasProperty(propertyTitle):
            return portal.getProperty(propertyTitle)
        else:
            return ''

    def createTitulo(self, portal, propertyTitle, titulo):
        if not portal.hasProperty(propertyTitle):
            portal.manage_addProperty(id=propertyTitle, type='string', value=titulo)
        elif portal.hasProperty(propertyTitle):
            portal.manage_delProperties([propertyTitle])
            portal.manage_addProperty(id=propertyTitle, type='string', value=titulo)

    def createTexto(self, portal, propertyText, texto):
        if not portal.hasProperty(propertyText):
            portal.manage_addProperty(id=propertyText, type='string', value=texto)
        elif portal.hasProperty(propertyText):
            portal.manage_delProperties([propertyText])
            portal.manage_addProperty(id=propertyText, type='string', value=texto)

    def delTexto(self, portal, propertyText):
        if portal.hasProperty(propertyText):
            portal.manage_delProperties([propertyText])

    def delTitulo(self, portal, propertyTitle):
        if portal.hasProperty(propertyTitle):
            portal.manage_delProperties([propertyTitle])

    def getId(self):
        try:
            pannelid = self.request.form['id']
            return pannelid
        except:
            return False


class ListaAlertas(BrowserView):
    def __call__(self):
        try:
            id = self.request.form['id']
            portal = api.portal.get()
            folder = portal['alertas']
            obj = folder[id]
            portal.portal_workflow.doActionFor(obj, 'retract')
            portal.portal_catalog.reindexObject(obj)
        except:
            pass
        try:
            del_id = self.request.form['del_id']
            portal = api.portal.get()
            folder = portal['alertas']
            folder.manage_delObjects([del_id])
        except:
            pass
        return ViewPageTemplateFile('templates/admin/lista_alertas.pt')(self)

    def retornaTitulo(self, obj):
        return obj.getObject().titulo.raw

    def retornaImagem(self, obj):
        return obj.getObject().img.raw

    def retornaDescricao(self, obj):
        return obj.getObject().descricao.raw

    def getAlertaAtivo(self):
        catalog = self.context.portal_catalog
        now = DateTime()
        alerta = catalog(portal_type='alerta', review_state='published', start={'query': [now], 'range': 'max'}, end={'query': [now], 'range': 'min'}, sort_on='start')
        return alerta

    def getListaAlertas(self):
        catalog = self.context.portal_catalog
        alertas = catalog(portal_type='alerta')
        return alertas
