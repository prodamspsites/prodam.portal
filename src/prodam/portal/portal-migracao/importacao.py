# -*- coding: utf-8 -*-
import glob
from Products.Five import BrowserView
from DateTime import DateTime
from plone import api
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.namedfile.file import NamedBlobImage


class MudaId(BrowserView):
    """ normalizar Url de noticias á partir do título
    inserir data de publicação da base legada do portal da prefeitura
    mudar criador da noticia para Secretaria executiva de comunicação
    """

    # TODO: normalizar url utf-8
    def mudar_id_noticias(self):
        folder = self.context
        catalog = folder.portal_catalog
        path = '/'.join(folder.getPhysicalPath())
        items = catalog(path=path)
        cleanID = getUtility(IIDNormalizer)
        ids = []
        if items:
            for i in items:
                titulo = i.Title.decode('utf-8')
                normalizedId = cleanID.normalize(titulo)
                if i.portal_type == 'News Item' and normalizedId not in folder.objectIds():
                    folder.manage_renameObject(i.id, normalizedId)
                    i.reindex
                    ids += [i.id]

        return ids

    # TODO: inserir data de publicação e criador
    def mudar_itens(self):

        handle = open('/home/raphael/Documentos/datas.csv', 'a+')
        folder = self.context
        cleanID = getUtility(IIDNormalizer)

        for line in handle.readlines():
            titulo = line.split(';')[1].decode('utf-8')
            data = line.split(';')[0]
            normalizedId = cleanID.normalize(titulo)
            try:
                noticia = folder[normalizedId]
                noticia.setEffectiveDate(DateTime(data))
                noticia.setCreators("Secretaria Executiva de Comunicação")
                noticia.reindexObject()
                print 'criador alterado' + noticia.id
            except:
                print 'erro no ' + normalizedId
                continue

    # TODO: publicar noticias
    def get_id(self):
        catalog = self.context.portal_catalog
        path = '/'.join(self.context.getPhysicalPath())
        items = catalog(path=path)
        if items:
            for i in items:
                status = i.portal_workflow.getInfoFor(i.getObject(), 'review_state')
                if status == 'private':
                    i.portal_workflow.doActionFor(i.getObject(), 'publish')

    # TODO: importar as imagens da base legada do portal da prefeitura
    def importar_imagens(self):
        portal = api.portal.get()

        folder = portal['noticia']
        handle = open('/home/raphael/noticias_id.csv', 'r+')

        cleanID = getUtility(IIDNormalizer)
        for x in handle.readlines():
            thisId = x.split('§')[0]
            titulo_noticia = x.split('§')[1].decode('utf-8')

            lista_de_imagens = glob.glob('/home/raphael/Documentos/imagens/' + thisId + '/*.jpg')
            if lista_de_imagens:
                url = glob.glob('/home/raphael/Documentos/imagens/' + thisId + '/*.jpg')[0]
                url_imagem = glob.glob('/home/raphael/Documentos/imagens/' + thisId + '/*.jpg')[0].split(str(thisId) + '/')[1]

                normalizedId = cleanID.normalize(titulo_noticia)
                imagem = folder[normalizedId]
                imagem.image = NamedBlobImage(data=open(url).read(), contentType='image/jpg', filename=unicode(url_imagem))
