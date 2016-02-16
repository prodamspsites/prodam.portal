# -*- coding: utf-8 -*-
# import glob
# from Products.Five import BrowserView
# from DateTime import DateTime
# from plone import api
# from zope.component import getUtility
# from plone.i18n.normalizer.interfaces import IIDNormalizer
# from plone.namedfile.file import NamedBlobImage
# from unicodedata import normalize
# from plone.app.textfield.value import RichTextValue


# class MudaId(BrowserView):
#     """ normalizar Url de noticias á partir do título
#     inserir data de publicação da base legada do portal da prefeitura
#     mudar criador da noticia para Secretaria executiva de comunicação
#     """

#     # TODO: normalizar url utf-8
#     def mudar_id_noticias(self):
#         folder = self.context
#         catalog = folder.portal_catalog
#         path = '/'.join(folder.getPhysicalPath())
#         items = catalog(path=path)
#         cleanID = getUtility(IIDNormalizer)
#         ids = []
#         if items:
#             for i in items:
#                 titulo = i.Title.decode('utf-8')
#                 normalizedId = cleanID.normalize(titulo)
#                 if i.portal_type == 'News Item' and normalizedId not in folder.objectIds():
#                     folder.manage_renameObject(i.id, normalizedId)
#                     i.reindex
#                     ids += [i.id]

#         return ids

#     # TODO: inserir data de publicação e criador
#     def mudar_itens(self):

#         handle = open('/home/raphael/Documentos/datas.csv', 'a+')
#         folder = self.context
#         cleanID = getUtility(IIDNormalizer)

#         for line in handle.readlines():
#             titulo = line.split(';')[1].decode('utf-8')
#             data = line.split(';')[0]
#             normalizedId = cleanID.normalize(titulo)
#             try:
#                 noticia = folder[normalizedId]
#                 texto_novo = noticia.text.raw.replace('^',',')
#                 noticia.text = text=RichTextValue(texto_novo, 'text/html', 'text/x-html-safe', encoding='utf-8')
#                 noticia.setEffectiveDate(DateTime(data))
#                 noticia.setCreators("Secretaria Executiva de Comunicação")
#                 noticia.reindexObject()
#                 print 'criador alterado' + noticia.id
#             except:
#                 print 'erro no ' + normalizedId
#                 continue

#     # TODO: publicar noticias
#     def get_id(self):
#         catalog = self.context.portal_catalog
#         path = '/'.join(self.context.getPhysicalPath())
#         items = catalog(path=path,portal_type='News Item')
#         if items:
#             for i in items:
#                 status = i.portal_workflow.getInfoFor(i.getObject(), 'review_state')
#                 if status == 'private':
#                     i.portal_workflow.doActionFor(i.getObject(), 'publish')

#     def limpa_texto(self):
#         folder = self.context
#         catalog = folder.portal_catalog
#         noticias = catalog(portal_type="News Item")
#         # for noticia in noticias:
#         #     obj = noticia.getObject()
#         #     texto = obj.SearchableText()
#         import pdb; pdb.set_trace();

#     # TODO: importar as imagens da base legada do portal da prefeitura
#     def importar_imagens(self):
#         portal = api.portal.get()

#         folder = portal['noticia']
#         # handle = open('/home/raphael/noticias_id.csv', 'r+')
#         handle = open('/home/raphael/Documentos/testes/galeria.csv', 'r+')
#         cleanID = getUtility(IIDNormalizer)
#         # import pdb; pdb.set_trace();
#         thisIdAnterior = ""
#         for x in handle.readlines():
#             thisId  = x.split('§')[0]
#             tit_img = x.split('§')[2].decode('utf-8')
#             desc_img = x.split('§')[3].decode('utf-8')
#             if thisIdAnterior != thisId:
#                 lista_de_imagens = glob.glob('/home/raphael/Documentos/imagens/' + thisId + '/*.jpg')
#                 if lista_de_imagens:
#                     for imagem in lista_de_imagens:
#                         nome_img = imagem.split(str(thisId) + '/')[1][:-4].replace('_','-')
#                         img_id = cleanID.normalize(nome_img,max_length=1000)
#                         handle = open('/home/raphael/noticias_search.csv','r+')
#                         for line in handle.readlines():
#                             if line.split('§')[0] == thisId:
#                                 noticia = cleanID.normalize(line.split('§')[7].decode('utf-8'))
#                                 noticiaAtual = folder[noticia]
#                                 thisImage = noticiaAtual.invokeFactory('Image', img_id,title=tit_img,description=desc_img)
#                                 # if thisImage not in noticiaAtual.objectIds():
#                                 thisImage = noticiaAtual[thisImage]
#                                 url = glob.glob(imagem)
#                                 try:
#                                     # import pdb; pdb.set_trace();
#                                     thisImage.image =  NamedBlobImage(data=open(url[0],'r').read(), contentType='image/jpg', filename=u'image.jpg')
#                                 except Exception, e:
#                                     print e
#             thisIdAnterior = thisId

#     # TESTS
#     def erro_imagem(self):
#         catalog = self.context.portal_catalog

#         images = catalog(path='/Prefeitura/noticia',portal_type='Image')
#         print len(images)
#         for i in images:
#           #print '\n'
#           #print i.Title
#           #print i.getObject().absolute_url()
#           #print i.Description
#           if not isinstance(i.getObject().image,NamedBlobImage):
#             print str(i.getObject().absolute_url())
