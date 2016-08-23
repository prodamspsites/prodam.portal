# -*- coding: utf-8 -*-
# import glob
# import csv
# import time
# import re
import os
from Products.Five import BrowserView
# from DateTime import DateTime
from plone import api
# from zope.component import getUtility
# from plone.i18n.normalizer.interfaces import IIDNormalizer
# from plone.namedfile.file import NamedBlobImage
# from urllib2 import Request, urlopen, URLError, HTTPError


class MudaId(BrowserView):
    """ normalizar Url de noticias á partir do título
    inserir data de publicação da base legada do portal da prefeitura
    mudar criador da noticia para Secretaria executiva de comunicação
    """

    # TODO: normalizar url utf-8
    # def mudar_id_noticias(self):
    #     folder = self.context
    #     catalog = folder.portal_catalog
    #     path = '/'.join(folder.getPhysicalPath())
    #     items = catalog(path=path)
    #     cleanID = getUtility(IIDNormalizer)
    #     ids = []
    #     if items:
    #         for i in items:
    #             titulo = i.Title.decode('utf-8')
    #             normalizedId = cleanID.normalize(titulo)
    #             if i.portal_type == 'News Item' and normalizedId not in folder.objectIds():
    #                 folder.manage_renameObject(i.id, normalizedId)
    #                 i.reindex
    #                 ids += [i.id]
    #
    #     return ids

    # TODO: inserir data de publicação e criador
    # def titulo(self):
    #
    #     folder = self.context
    #     catalog = folder.portal_catalog
    #     path = '/'.join(folder.getPhysicalPath())
    #     items = catalog(path=path)
    #     if items:
    #         for item in items:
    #             # print item.Title.replace('¢',',')
    #             try:
    #                 pasta = folder[item.id]
    #                 desc = item.Description.replace('¢',',')
    #                 pasta.setDescription(desc)
    #                 pasta.reindexObject()
    #                 print 'passou--'+str(item.Description)
    #             except KeyError, e:
    #                 print 'erro'
    # TODO: inserir data de publicação e criador
    # def mudar_itens(self):
    #
    #     handle = open('/home/raphael/Documentos/datas.csv', 'a+')
    #     folder = self.context
    #     cleanID = getUtility(IIDNormalizer)
    #
    #     for line in handle.readlines():
    #         titulo = line.split(';')[1].decode('utf-8')
    #         data = line.split(';')[0]
    #         normalizedId = cleanID.normalize(titulo)
    #         try:
    #             noticia = folder[normalizedId]
    #             noticia.setEffectiveDate(DateTime(data))
    #             noticia.setCreators("Secretaria Executiva de Comunicação")
    #             noticia.reindexObject()
    #             print 'criador alterado' + noticia.id
    #         except:
    #             print 'erro no ' + normalizedId
    #             continue

    # TODO: publicar noticias
    # def get_id(self):
    #     catalog = self.context.portal_catalog
    #     path = '/'.join(self.context.getPhysicalPath())
    #     items = catalog(path=path)
    #     if items:
    #         for i in items:
    #             status = i.portal_workflow.getInfoFor(i.getObject(), 'review_state')
    #             if status == 'private':
    #                 i.portal_workflow.doActionFor(i.getObject(), 'publish')

    def refactor(self):
        handle = os.path.abspath('data/atualizado.csv')
        portal = api.portal.get()
        folder = portal['noticia']
        datas = open(handle, 'r+').readlines()
        for data in datas:
            try:
                news = folder[data.split(",")[0]]
                if data.split(',')[2] != "\n":
                    texto = news.text.output
                    news.text = texto.replace(data.split(',')[1], data.split(',')[2])
                    news.reindexObject()
                    print "mudou" + str(data.split(',')[1]) + "por" + str(data.split(',')[2])
            except Exception, e:
                print e

    # def urlprefeitura(self):
    #     catalog = self.context.portal_catalog
    #     path = '/'.join(self.context.getPhysicalPath())
    #     items = catalog(portal_type="News Item", path=path)
    #     if items:
    #         handle = open('/home/raphaeliarussi/RAPHAEL_URL123','a+')
    #         dicionario = {}
    #         for i in items:
    #             # import pdb; pdb.set_trace();
    #             try:
    #                 body = i.getObject().text.output
    #                 urls = re.findall(r'src=[\'"]?([^\'" >]+)',body)
    #                 for url in urls:
    #                     print i.id+","+url
    #             except AttributeError:
    #                 body = unicode("")
    #     else:
    #         print 'nenhum item encontrado'
    #     return dicionario

    # def stealStuff(self,noticia,file_mode,base_url):
    #     #create the url and the request
    #     file_name = base_url.split("/")[-1]
    #     url = base_url
    #     req = Request(url)
    #
    #     # Open the url
    #     try:
    #         f = urlopen(req)
    #         print "downloading " + url
    #         time.sleep( 1 )
    #         # Open our local file for writing
    #         local_file = open("imagens/"+file_name, "w" + file_mode)
    #         # import pdb; pdb.set_trace();
    #         #Write to our local file
    #         local_file.write(f.read())
    #         local_file.close()
    #         portal = api.portal.get()
    #         folder = portal['noticia']
    #         try:
    #             pasta_imagem = folder[noticia]
    #             imgId = unicode(file_name.split(".")[0])
    #             if imgId.startswith('_'):
    #                 imgId = 'n'+imgId
    #             pasta_imagem.invokeFactory('Image',imgId)
    #             pasta_imagem[imgId].image = NamedBlobImage(data=open("imagens/"+file_name).read(), contentType='image/jpg', filename=imgId)
    #             print 'passou'+unicode(file_name.split(".")[0])
    #         except Exception:
    #             print 'erro'+noticia
    #
    #     #handle errors
    #     except HTTPError, e:
    #         pass
    #     except URLError, e:
    #         pass

    # TODO: importar as imagens da base legada do portal da prefeitura

    # def removeImgs(self):
    #     portal = api.portal.get()
    #     folder = portal['noticia']
    #     noticias = folder.getFolderContents()
    #     for n in noticias:
    #         if n.getObject().getFolderContents():
    #             lista_de_imagens = []
    #             for i in n.getObject().getFolderContents():
    #                 lista_de_imagens.append(i.id)
    #             n.getObject().manage_delObjects(lista_de_imagens)

    # def importar_imagens_hd(self):
    #
    #     # portal = api.portal.get()
    #     # folder = portal['noticia']
    #     handle = open('/home/raphaeliarussi/img_altaresolucao.csv', 'r+')
    #     for x in handle.readlines():
    #         id = x.split(',')[0]
    #         imagem = x.split(',')[1]
    #         # print ','.join([id,imagem])
    #         # import pdb; pdb.set_trace()
    #         self.invoke_importar_imagens_hd(id, imagem)

    # def invoke_importar_imagens_hd(self, id, imagem):
    #     #create the url and the request
    #     try:
    #         portal = api.portal.get()
    #         folder = portal['noticia']
    #         noticia = folder[id]
    #         texto = noticia.text.raw
    #         urls = re.findall('http[s]?://(?:[www.prefeitura.sp.gov.br/])+(?:/[^/#?]+)+\.(?:jpg|gif|png)', texto)
    #         if type(urls) is list and len(urls) > 0:
    #             for url in urls:
    #                 req = Request(str(url))
    #                 # print imagem
    #                 filename= url.split('/')[-1].split('.')[0]
    #                 f = urlopen(req)
    #                 print "downloading " + imagem
    #                 time.sleep( 1 )
    #                 # Open our local file for writing
    #                 local_file = open("imagens_hd/"+filename, "wb")
    #                 local_file.write(f.read())
    #                 local_file.close()
    #                 cleanID = getUtility(IIDNormalizer)
    #                 titulo_plone = cleanID.normalize(filename)
    #                 folder_imagem = portal['imagens-alta-resolucao']
    #                 if not titulo_plone in folder_imagem.objectIds():
    #                     folder_imagem.invokeFactory('Image', titulo_plone)
    #
    #                 folder_imagem[titulo_plone].image = NamedBlobImage(data=open("imagens_hd/"+filename).read(), contentType='image/jpg', filename=unicode(titulo_plone))
    #                 image_path = folder_imagem[titulo_plone].absolute_url()
    #                 if url in texto:
    #                     noticia.texto = texto.replace(url, unicode(image_path))
    #                     print url
    #                     print image_path
    #                     print id

            # print tex//t
            # if imagem in texto:
            #     n.text = text.replace(imagem, image_path)
            #     print i.id
            # try:
            #     pasta_imagem = folder[noticia]
            #     imgId = unicode(file_name.split(".")[0])
            #     if imgId.startswith('_'):
            #         imgId = 'n'+imgId
            #     pasta_imagem.invokeFactory('Image',imgId)
            #     pasta_imagem[imgId].image = NamedBlobImage(data=open("imagens/"+file_name).read(), contentType='image/jpg', filename=imgId)
            #     print 'passou'+unicode(file_name.split(".")[0])
            # except Exception:
            #     print 'erro'+noticia

        # handle errors
        # except HTTPError, e:
        #     pass
        # except URLError, e:
        #     pass

    # def importar_imagens(self):
    #
    #     # portal = api.portal.get()
    #     # folder = portal['noticia']
    #     handle = open('/home/raphaeliarussi/Documentos/imagem.csv', 'r+')
    #     cleanID = getUtility(IIDNormalizer)
    #     for x in handle.readlines():
    #         titulo_imagem = x.split('§')[2].replace(' ','-').decode('utf-8')
    #         imagem = x.split('§')[3]
    #         noticia = x.split('§')[4].decode('utf-8')
    #         noticia = cleanID.normalize(noticia)
    #
    #         self.stealStuff(noticia,"b",imagem)
