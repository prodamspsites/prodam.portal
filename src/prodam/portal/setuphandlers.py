# -*- coding: utf-8 -*-
from plone.app.textfield.value import RichTextValue


def importSteps(context):
    site = context.getSite()
    createMaisBuscados(site)
    createFooter(site)


def createObj(site, objId, title, type, path, exclude_from_nav=False):
    try:
        parent = site.restrictedTraverse(path)
        if objId not in parent.objectIds():
            parent.invokeFactory(type, objId, title=title)
            obj = parent[objId]
            site.portal_workflow.doActionFor(obj, 'publish')
            obj.exclude_from_nav = exclude_from_nav
            site.portal_catalog.reindexObject(obj)
    except:
        pass


def createDoc(site, objId, title, path, text, exclude_from_nav=False):
    try:
        parent = site.restrictedTraverse(path)
        if objId not in parent.objectIds():
            parent.invokeFactory('Document', objId, title=title, text=RichTextValue(text, 'text/html', 'text/x-html-safe', encoding='utf-8'))
            obj = parent[objId]
            site.portal_workflow.doActionFor(obj, 'publish')
            obj.exclude_from_nav = exclude_from_nav
            site.portal_catalog.reindexObject(obj)
    except:
        pass


def createLinkObject(site, objId, title, path, url, exclude_from_nav=False):
    try:
        parent = site.restrictedTraverse(path)
        if objId not in parent.objectIds():
            parent.invokeFactory('Link', objId, title=title, remoteUrl=url)
            obj = parent[objId]
            site.portal_workflow.doActionFor(obj, 'publish')
            obj.exclude_from_nav = exclude_from_nav
            site.portal_catalog.reindexObject(obj)
    except:
        pass


def createChamada(site, objId, title, path, url, exclude_from_nav=False):
    try:
        parent = site.restrictedTraverse(path)
        if objId not in parent.objectIds():
            parent.invokeFactory('prodam.chamadas', objId, title=title, url=url)
            obj = parent[objId]
            site.portal_workflow.doActionFor(obj, 'publish')
            site.portal_catalog.reindexObject(obj)
            obj.exclude_from_nav = exclude_from_nav
    except:
        pass


def createFooter(site):
    createObj(site, 'rodape', 'Rodapé', 'Folder', '', exclude_from_nav=True)
    createGovernoMunicipal(site)
    createAconteceNaCidade(site)
    createSaoPauloPara(site)
    createAtendimento(site)
    createPrefeitura(site)
    createCanaisOficiais(site)
    createConsultas(site)
    createAplicativos(site)


def createGovernoMunicipal(site):
    createObj(site, 'governo-municipal', 'Governo Municipal', 'Folder', 'rodape', exclude_from_nav=True)

    url_site = site.absolute_url() + '/agenda'
    # createDoc(site, 'governo-municipal', 'Governo Municipal', 'rodape/governo-municipal', '<ul><li><span>Prefeito</span> <strong>João Dória</strong></li><li><a target="_blank" href="http://www.prefeitura.sp.gov.br/guiadeservicos/content/equipe-de-governo"><strong>Equipe de Governo</strong></a></li></ul><ul class="lista"><li><a href="../../agenda">Agenda do prefeito</a></li></ul>')
    createDoc(site, 'governo-municipal', 'Governo Municipal', 'rodape/governo-municipal', '<ul><li><span>Prefeito</span><strong>Fernando Haddad</strong></li><li><a target="_blank" href="http://www.prefeitura.sp.gov.br/guiadeservicos/content/equipe-de-governo"><strong>Equipe de Governo</strong></a></li></ul><ul class="lista"><li><a href="' + url_site + '">Agenda do prefeito</a></li></ul>')


def createAconteceNaCidade(site):
    createObj(site, 'acontece-na-cidade', 'Acontece na Cidade', 'Folder', 'rodape', exclude_from_nav=True)
    createLinkObject(site, 'ultimas-noticias', 'Últimas notícias', 'rodape/acontece-na-cidade', '/Prefeitura/noticia')
    createLinkObject(site, 'itinerarios-de-onibus', 'Itinerários de ônibus', 'rodape/acontece-na-cidade', 'http://www.sptrans.com.br/itinerarios/')
    createLinkObject(site, 'mapa-de-servicos', 'Mapa de serviços', 'rodape/acontece-na-cidade', '/Prefeitura/mapa')


def createSaoPauloPara(site):
    createObj(site, 'sao-paulo-para', 'São Paulo para', 'Folder', 'rodape', exclude_from_nav=True)
    createLinkObject(site, 'cidadao', 'Cidadão', 'rodape/sao-paulo-para', '/Prefeitura/cidadao')
    createLinkObject(site, 'empresa', 'Empresa', 'rodape/sao-paulo-para', '/Prefeitura/empresa')
    createLinkObject(site, 'turista', 'Turista', 'rodape/sao-paulo-para', '/Prefeitura/turista')
    createLinkObject(site, 'servidor', 'Servidor', 'rodape/sao-paulo-para', '/Prefeitura/servidor')


def createAtendimento(site):
    createObj(site, 'atendimento', 'Atendimento', 'Folder', 'rodape', exclude_from_nav=True)
    createDoc(site, 'atendimento', 'Atendimento', 'rodape/atendimento', '<ul class="box_content"><li><a target="_blank" aria-label="Faça sua Solicitação" href="http://sac.prefeitura.sp.gov.br Faça sua Solicitação</a></li></ul>')


def createPrefeitura(site):
    createObj(site, 'prefeitura', 'Prefeitura', 'Folder', 'rodape', exclude_from_nav=True)
    createObj(site, 'secretarias', 'Secretarias', 'Folder', 'rodape/prefeitura', exclude_from_nav=True)
    createLinkObject(site, 'assistencia-social', 'Assistência Social', 'rodape/prefeitura/secretarias', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/assistencia_social')
    createLinkObject(site, 'comunicacao', 'Comunicação', 'rodape/prefeitura/secretarias', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/comunicacao')
    createLinkObject(site, 'controladoria-geral-do-municipio', 'Controladoria Geral do Município', 'rodape/prefeitura/secretarias', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/controladoria_geral')
    createLinkObject(site, 'cultura', 'Cultura', 'rodape/prefeitura/secretarias', 'http://cultura.prefeitura.sp.gov.br')
    createLinkObject(site, 'urbano', 'Urbano', 'rodape/prefeitura/secretarias', 'http://smdu.prefeitura.sp.gov.br Desenvolvimento')
    createLinkObject(site, 'direitos-humanos-e-cidadania', 'Direitos Humanos e Cidadania', 'rodape/prefeitura/secretarias', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos')
    createLinkObject(site, 'educacao', 'Educação', 'rodape/prefeitura/secretarias', 'http://educacao.prefeitura.sp.gov.br')
    createLinkObject(site, 'esportes', 'Esportes', 'rodape/prefeitura/secretarias', 'http://esportes.prefeitura.sp.gov.br')
    createLinkObject(site, 'finanças-e-desenv-economico', 'Finanças e Desenv. Econômico', 'rodape/prefeitura/secretarias', 'http:// financas.prefeitura.sp.gov.br')
    createLinkObject(site, 'gestao', 'Gestão', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/gestao')
    createLinkObject(site, 'governo', 'Governo', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/governo')
    createLinkObject(site, 'habitacao', 'Habitação', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/habitacao')
    createLinkObject(site, 'infraestrutura-urbana', 'Infraestrutura Urbana', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/infraestrutura')
    createLinkObject(site, 'licenciamento', 'Licenciamento', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/licenciamentos')
    createLinkObject(site, 'negocios-juridicos', 'Negócios Jurídicos', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/negocios_juridicos')
    createLinkObject(site, 'pessoa-com-deficiencia', 'Pessoa com Deficiência', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/pessoa_com_deficiencia')
    createLinkObject(site, 'politicas-para-as-mulheres', 'Políticas para as Mulheres', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/politicas_para_as_mulheres')
    createLinkObject(site, 'promocao-da-igualdade-racial', 'Promoção da Igualdade Racial', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/igualdade_racial')
    createLinkObject(site, 'relacoes-governamentais', 'Relações Governamentais', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/relacoes_governamentais')
    createLinkObject(site, 'relacoes-internacionais-e-federativas', 'Relações Internacionais e Federativas', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/relacoes_internacionais')
    createLinkObject(site, 'saude', 'Saúde', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/saude')
    createLinkObject(site, 'segurança-urbana', 'Segurança Urbana', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/seguranca_urbana')
    createLinkObject(site, 'servicos', 'Serviços', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/servicos')
    createLinkObject(site, 'subprefeituras', 'Subprefeituras', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/subprefeituras')
    createLinkObject(site, 'trabalho-e-empreendedorismo', 'Trabalho e Empreendedorismo', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/trabalho')
    createLinkObject(site, 'transportes', 'Transportes', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/transportes')
    createLinkObject(site, 'verde-e-meio-ambiente', 'Verde e Meio Ambiente', 'rodape/prefeitura/secretarias', 'http:// www.prefeitura.sp.gov.br/cidade/secretarias/meio_ambiente')

    createObj(site, 'subprefeituras', 'Subprefeituras', 'Folder', 'rodape/prefeitura', exclude_from_nav=True)
    createLinkObject(site, 'aricanduva-v-formosa', 'Aricanduva/V.Formosa', 'rodape/prefeitura/subprefeituras', 'http://aricanduva.prefeitura.sp.gov.br')
    createLinkObject(site, 'butanta', 'Butantã', 'rodape/prefeitura/subprefeituras', 'http://butanta.prefeitura.sp.gov.br')
    createLinkObject(site, 'campo-limpo', 'Campo Limpo', 'rodape/prefeitura/subprefeituras', 'http://campolimpo.prefeitura.sp.gov.br')
    createLinkObject(site, 'capela-do-socorro', 'Capela do Socorro', 'rodape/prefeitura/subprefeituras', 'http://capeladosocorro.prefeitura.sp.gov.br')
    createLinkObject(site, 'casa-verde', 'Casa Verde', 'rodape/prefeitura/subprefeituras', 'http://casaverde.prefeitura.sp.gov.br/')
    createLinkObject(site, 'cidade-ademar', 'Cidade Ademar', 'rodape/prefeitura/subprefeituras', 'http://cidadeademar.prefeitura.sp.gov.br')
    createLinkObject(site, 'cidade-tiradentes', 'Cidade Tiradentes', 'rodape/prefeitura/subprefeituras', 'http://cidadetiradentes.prefeitura.sp.gov.br')
    createLinkObject(site, 'ermelino-matarazzo', 'Ermelino Matarazzo', 'rodape/prefeitura/subprefeituras', 'http://ermelinomatarazzo.prefeitura.sp.gov.br')
    createLinkObject(site, 'freguesia-do-o-brasilandia', 'Freguesia do Ó/Brasilândia', 'rodape/prefeitura/subprefeituras', 'http://freguesia.prefeitura.sp.gov.br')
    createLinkObject(site, 'guaianases', 'Guaianases', 'rodape/prefeitura/subprefeituras', 'http://guaianases.prefeitura.sp.gov.br')
    createLinkObject(site, 'ipiranga', 'Ipiranga', 'rodape/prefeitura/subprefeituras', 'http://ipiranga.prefeitura.sp.gov.br')
    createLinkObject(site, 'itaim-paulista', 'Itaim Paulista', 'rodape/prefeitura/subprefeituras', 'http://itaimpaulista.prefeitura.sp.gov.br')
    createLinkObject(site, 'itaquera', 'Itaquera', 'rodape/prefeitura/subprefeituras', 'http://itaquera.prefeitura.sp.gov.br')
    createLinkObject(site, 'jabaquara', 'Jabaquara', 'rodape/prefeitura/subprefeituras', 'http://jabaquara.prefeitura.sp.gov.br')
    createLinkObject(site, 'jacana-tremembe', 'Jaçanã/Tremembé', 'rodape/prefeitura/subprefeituras', 'http://jacana-tremembe.prefeitura.sp.gov.br')
    createLinkObject(site, 'lapa', 'Lapa', 'rodape/prefeitura/subprefeituras', 'http://lapa.prefeitura.sp.gov.br')
    createLinkObject(site, 'm-boi-mirim', 'M Boi Mirim', 'rodape/prefeitura/subprefeituras', 'http://mboimirim.prefeitura.sp.gov.br')
    createLinkObject(site, 'mooca', 'Mooca', 'rodape/prefeitura/subprefeituras', 'http://mooca.prefeitura.sp.gov.br')
    createLinkObject(site, 'parelheiros', 'Parelheiros', 'rodape/prefeitura/subprefeituras', 'http://parelheiros.prefeitura.sp.gov.br')
    createLinkObject(site, 'penha', 'Penha', 'rodape/prefeitura/subprefeituras', 'http://penha.prefeitura.sp.gov.br')
    createLinkObject(site, 'perus', 'Perus', 'rodape/prefeitura/subprefeituras', 'http://perus.prefeitura.sp.gov.br')
    createLinkObject(site, 'pinheiros', 'Pinheiros', 'rodape/prefeitura/subprefeituras', 'http://pinheiros.prefeitura.sp.gov.br')
    createLinkObject(site, 'pirituba-jaragua', 'Pirituba/Jaraguá', 'rodape/prefeitura/subprefeituras', 'http://pirituba.prefeitura.sp.gov.br')
    createLinkObject(site, 'santana-tucuruvi', 'Santana/Tucuruvi', 'rodape/prefeitura/subprefeituras', 'http://santana-tucuruvi.prefeitura.sp.gov.br')
    createLinkObject(site, 'santo-amaro', 'Santo Amaro', 'rodape/prefeitura/subprefeituras', 'http://santoamaro.prefeitura.sp.gov.br')
    createLinkObject(site, 'sao-mateus', 'São Mateus', 'rodape/prefeitura/subprefeituras', 'http://saomateus.prefeitura.sp.gov.br')
    createLinkObject(site, 'sao-miguel', 'São Miguel', 'rodape/prefeitura/subprefeituras', 'http://saomiguel.prefeitura.sp.gov.br')
    createLinkObject(site, 'sapopemba', 'Sapopemba', 'rodape/prefeitura/subprefeituras', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/subprefeituras/sapopemba/')
    createLinkObject(site, 'se', 'Sé', 'rodape/prefeitura/subprefeituras', 'http://se.prefeitura.sp.gov.br/')
    createLinkObject(site, 'v-maria-v-guilherme', 'V.Maria/V.Guilherme', 'rodape/prefeitura/subprefeituras', 'http://vilamaria-vilaguilherme.prefeitura.sp.gov.br')
    createLinkObject(site, 'vila-mariana', 'Vila Mariana', 'rodape/prefeitura/subprefeituras', 'http://vilamariana.prefeitura.sp.gov.br')
    createLinkObject(site, 'vila-prudente', 'Vila Prudente', 'rodape/prefeitura/subprefeituras', 'http://vilaprudente.prefeitura.sp.gov.br')

    createObj(site, 'outros-orgaos', 'Outros Órgãos', 'Folder', 'rodape/prefeitura', exclude_from_nav=True)
    createLinkObject(site, 'autarquia-hospitalar-do-municipio-de-sao-paulo-ahmsp', 'Autarquia Hospitalar do Município de São Paulo - AHMSP', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/ahm')
    createLinkObject(site, 'camara-tecnica-de-legislacao-urbanistica-ctlu', 'Câmara Técnica de Legislação Urbanística – CTLU', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/desenvolvimento_urbano/ctlu/index.php?p=853')
    createLinkObject(site, 'centro-de-gerenciamento-de-emergencias', 'Centro de Gerenciamento de Emergências - CGE', 'rodape/prefeitura/outros-orgaos', 'http://www.cgesp.org/')
    createLinkObject(site, 'comissao-de-analise-integrada-de-projetos-de-edificacoes-e-de-parcelamento-do-solo', 'Comissão de Análise Integrada de Projetos de Edificações e de Parcelamento do Solo – CAIEPS', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/licenciamentos/colegiados/index.php?p=148606')
    createLinkObject(site, 'comissao-de-avaliacao-de-empreendimentos-habitacionais-de-interesse-social', 'Comissão de Avaliação de Empreendimentos Habitacionais de Interesse Social – CAEHIS', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/licenciamentos/colegiados/index.php?p=148608')
    createLinkObject(site, 'comissao-de-edificacoes-e-uso-do-solo', 'Comissão de Edificações e Uso do Solo - CEUSO', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/licenciamentos/colegiados/index.php?p=148605')
    createLinkObject(site, 'comissao-de-protecao-a-paisagem-urbana', 'Comissão de Proteção à Paisagem Urbana – CPPU', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/desenvolvimento_urbano/cppu/index.php?p=16200')
    createLinkObject(site, 'comissao-municipal-de-direitos-humanos', 'Comissão Municipal de Direitos Humanos', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/orgaos_colegiados/index.php?p=204')
    createLinkObject(site, 'comite-intersetorial-da-politica-municipal-para-a-população-em-situacao-de-rua', 'Comitê Intersetorial da Política Municipal para a População em Situação de Rua', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/poprua/comite/index.php?p=150036')
    createLinkObject(site, 'companhia-de-engenharia-de-trafego', 'Companhia de Engenharia de Trafégo - CET', 'rodape/prefeitura/outros-orgaos', 'http://www.cetsp.com.br/')
    createLinkObject(site, 'companhia-metropolitana-de-habitação-de-sao-paulo', 'Companhia Metropolitana de Habitação de São Paulo - COHAB-SP', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/habitacao/cohab/')
    createLinkObject(site, 'companhia-paulista-de-securitizacao', 'Companhia Paulista de Securitização - SPSEC', 'rodape/prefeitura/outros-orgaos', 'http://transparencia.prefeitura.sp.gov.br/admindireta/empresas/Paginas/SPSEC.aspx')
    createLinkObject(site, 'companhia-sao-paulo-de-desenvolvimento-e-mobilização-de-ativos', 'Companhia São Paulo de Desenvolvimento e Mobilização de Ativos - SPDA', 'rodape/prefeitura/outros-orgaos', 'http://transparencia.prefeitura.sp.gov.br/admindireta/empresas/Paginas/SPDA.aspx')
    createLinkObject(site, 'conselho-da-cidade-de-sao-paulo', 'Conselho da Cidade de São Paulo', 'rodape/prefeitura/outros-orgaos', 'http://conselhodacidade.prefeitura.sp.gov.br/')
    createLinkObject(site, 'conselho-gestor-do-fundo-de-desenvolvimento-urbano', 'Conselho Gestor do Fundo de Desenvolvimento Urbano - FUNDURB', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/desenvolvimento_urbano/fundurb/index.php?p=155886')
    createLinkObject(site, 'conselho-municipal-da-educação', 'Conselho Municipal da Educação - CME', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/educacao/cme/')
    createLinkObject(site, 'conselho-municipal-da-pessoa-com-deficiencia', 'Conselho Municipal da Pessoa com Deficiência - CMPD', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/pessoa_com_deficiencia/conselho/')
    createLinkObject(site, 'conselho-municipal-de-assistencia-social', 'Conselho Municipal de Assistência Social - COMAS', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/assistencia_social/comas/')
    createLinkObject(site, 'conselho-municipal-de-atencao-a-diversidade-sexual', 'Conselho Municipal de Atenção à Diversidade Sexual', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/lgbt/conselho/index.php?p=150958')
    createLinkObject(site, 'conselho-municipal-de-ciencia-tecnologia-inovação', 'Conselho Municipal de Ciência, Tecnologia &amp; Inovação - CMCTI', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/trabalho/cmcti/')
    createLinkObject(site, 'conselho-municipal-de-habitacao', 'Conselho Municipal de Habitação - CMH', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/habitacao/organizacao/cmh/index.php?p=139')
    createLinkObject(site, 'conselho-municipal-de-politica-urbana', 'Conselho Municipal de Política Urbana – CMPU', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/desenvolvimento_urbano/cmpu/index.php?p=144874')
    createLinkObject(site, 'conselho-municipal-de-preservaçao-ao-patrimonio-histórico', 'Conselho Municipal de Preservação ao Patrimônio Histórico - CONPRESP', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/cultura/conpresp/')
    createLinkObject(site, 'conselho-municipal-de-saude', 'Conselho Municipal de Saúde - CMS', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/saude/conselho_municipal/')
    createLinkObject(site, 'conselho-municipal-de-seguranca-alimentar-e-autricional', 'Conselho Municipal de Segurança Alimentar e Nutricional - COMUSAN', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/subprefeituras/abastecimento/comusan/index.php?p=26221')
    createLinkObject(site, 'conselho-municipal-de-tecnologia-de-informacao-e-comunicacao', 'Conselho Municipal de Tecnologia de Informação e Comunicação - CMTIC', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/planejamento/cmi/')
    createLinkObject(site, 'conselho-municipal-de-tributos', 'Conselho Municipal de Tributos - CMT', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/financas/institucional/index.php?p=3182')
    createLinkObject(site, 'conselho-municipal-de-turismo', 'Conselho Municipal de Turismo - COMTUR', 'rodape/prefeitura/outros-orgaos', 'http://www.cidadedesaopaulo.com/comtur/')
    createLinkObject(site, 'conselho-municipal-do-meio-ambiente-e-desenvolvimento-sustentavel', 'Conselho Municipal do Meio Ambiente e Desenvolvimento Sustentável - CADES', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/meio_ambiente/cades/index.php?p=3250')
    createLinkObject(site, 'conselho-municipal-dos-direitos-da-juventude', 'Conselho Municipal dos Direitos da Juventude', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/juventude/conselho/index.php?p=149694')
    createLinkObject(site, 'coordenacao-de-direito-a-memoria-e-a-verdade', 'Coordenação de Direito à Memória e à Verdade', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/direito_a_memoria_e_a_verdade/')
    createLinkObject(site, 'coordenacao-de-politica-sobre-drogas', 'Coordenação de Política sobre Drogas', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/edh/')
    createLinkObject(site, 'coordenacao-de-politicas-para-a-populacao-em-situacao-de-rua', 'Coordenação de Políticas para a População em Situação de Rua', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/poprua/')
    createLinkObject(site, 'coordenacao-de-politicas-para-criancas-e-adolescentes', 'Coordenação de Políticas para Crianças e Adolescentes', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/criancas_e_adolescentes/')
    createLinkObject(site, 'coordenacao-de-politicas para Idosos', 'Coordenação de Políticas para Idosos', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/idosos/')
    createLinkObject(site, 'coordenacao-de-politicas-para-juventude', 'Coordenação de Políticas para Juventude', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/juventude/')
    createLinkObject(site, 'coordenacao-de-politicas-para-lgbt', 'Coordenação de Políticas para LGBT', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/lgbt/')
    createLinkObject(site, 'coordenacao-de-politicas-para-migrantes', 'Coordenação de Políticas para Migrantes', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/migrantes/')
    createLinkObject(site, 'coordenadoria-de-conectividade-e-convergencia-digital', 'Coordenadoria de Conectividade e Convergência Digital - CCCD', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/servicos/inclusao_digital/')
    createLinkObject(site, 'defesa-civil', 'Defesa Civil', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/subprefeituras/defesa_civil/')
    createLinkObject(site, 'empresa-de-tecnologia-da-informacao-e-comunicacao-do-municipio-de-sao-paulo', 'Empresa de Tecnologia da Informação e Comunicação do Município de São Paulo - PRODAM', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/gestao/prodam/')
    createLinkObject(site, 'fundacao-paulistana-de-educacao-e-tecnologia', 'Fundação Paulistana de Educação e Tecnologia', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/planejamento/fundacao_paulistana/apresentacao/index.php?p=25342')
    createLinkObject(site, 'fundacao-theatro-municipa-de-sao-paulo', 'Fundação Theatro Municipal de São Paulo', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/cultura/noticias/?p=9064')
    createLinkObject(site, 'grande-conselho-municipal-do-idoso', 'Grande Conselho Municipal do Idoso', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/idosos/conselho/')
    createLinkObject(site, 'guarda-municipal-metropolitana', 'Guarda Municipal Metropolitana - GCM', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/seguranca_urbana/guarda_civil/')
    createLinkObject(site, 'hospital-do-servidor-publico-municipal', 'Hospital do Servidor Público Municipal - HSPM', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/saude/hospital_do_servidor_publico_municipal/')
    createLinkObject(site, 'hospital-municipal-infantil-menino-jesus', 'Hospital Municipal Infantil Menino Jesus - HMIMJ', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/saude/hospital_municipal_infantil_menino_jesus/')
    createLinkObject(site, 'instituto-de-previdencia-municipal-de-são-de-paulo', 'Instituto de Previdência Municipal de São de Paulo - IPREM-SP', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/iprem')
    createLinkObject(site, 'ouvidoria-geral-do-municipio-de-sao-paulo', 'Ouvidoria Geral do Municipio de São Paulo - OGM', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/ouvidoria/')
    createLinkObject(site, 'sao-paulo-negocios', 'São Paulo Negócios - SP Negócios', 'rodape/prefeitura/outros-orgaos', 'http://www.spnegocios.com/')
    createLinkObject(site, 'sao-paulo-obras', 'São Paulo Obras - SPObras', 'rodape/prefeitura/outros-orgaos', 'http://www.spobras.sp.gov.br/')
    createLinkObject(site, 'sao-paulo-transportes', 'São Paulo Transportes - SPTrans', 'rodape/prefeitura/outros-orgaos', 'http://www.sptrans.com.br/')
    createLinkObject(site, 'sao-paulo-turismo', 'São Paulo Turismo - SPTuris', 'rodape/prefeitura/outros-orgaos', 'http://www.cidadedesaopaulo.com/')
    createLinkObject(site, 'sao-paulo-urbanismo', 'São Paulo Urbanismo - SPUrbanismo', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/desenvolvimento_urbano/sp_urbanismo/')
    createLinkObject(site, 'servico-funerario-do-municipio-de São de Paulo', 'Serviço Funerário do Município de São de Paulo - SFMSP', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/servicos/servico_funerario/')
    createLinkObject(site, 'supervisao-geral-de-abastecimento', 'Supervisão Geral de Abastecimento - SGA', 'rodape/prefeitura/outros-orgaos', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/trabalho/abastecimento/')


def createCanaisOficiais(site):
    createObj(site, 'canais-oficiais', 'Canais Oficiais', 'Folder', 'rodape', exclude_from_nav=True)
    createDoc(site, 'canais-oficiais', 'Canais Oficiais', 'rodape/canais-oficiais', '<ul class="social_footer" id="social_footer"><li><a target="_blank" href="https://www.facebook.com/PrefSP"><span id="facebook">Facebook</span></a></li><li><a target="_blank" href="http://www.twitter.com/prefsp"><span id="twitter">Twitter</span></a></li><li><a target="_blank" href="http://www.youtube.com/prefeiturasaopaulo"><span id="youtube">Youtube</span></a></li><li style="clear: both;padding-top: 14px;"><a target="_blank" href="http://www.docidadesp.imprensaoficial.com.br"><span id="diario"></span>Diário Oficial</a></li></ul>')


def createConsultas(site):
    createObj(site, 'consultas', 'Consultas', 'Folder', 'rodape', exclude_from_nav=True)
    createLinkObject(site, 'leis-municipais', 'Leis Municipais', 'rodape/consultas', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/negocios_juridicos/cadastro_de_leis/index.php?p=325')
    createLinkObject(site, 'pesquisa-de-processos', 'Pesquisa de Processos', 'rodape/consultas', 'http://www3.prodam.sp.gov.br/simproc/simproc.asp')
    createLinkObject(site, 'licitacoes', 'Licitações', 'rodape/consultas', 'http://e-negocioscidadesp.prefeitura.sp.gov.br/')
    createLinkObject(site, 'ata-de-registro-de-precos', 'Ata de Registro de Preços', 'rodape/consultas', 'http://www.prefeitura.sp.gov.br/cidade/secretarias/planejamento/links/index.php?p=24208')


def createAplicativos(site):
    createObj(site, 'aplicativos', 'Aplicativos', 'Folder', 'rodape', exclude_from_nav=True)
    createDoc(site, 'aplicativos', 'Aplicativos', 'rodape/aplicativos', '<ul><li><a target="_blank" class="app-icone app-iphone" href="https://itunes.apple.com/us/app/prefeitura-sao-paulo/id829248485?mt=8"><img height="45px" width="118px" src="++resource++prodam.portal/img/icon_appestore_disponivel.png"></a></li><li><a target="_blank" class="app-icone app-android" href="https://play.google.com/store/apps/details?id=br.inf.call.dashboard_sp"><img height="45px" width="118px" src="++resource++prodam.portal/img/icon_googleplay.png"></a></li></ul>')


def createMaisBuscados(site):
    createObj(site, 'mais-buscados', 'Mais Buscados', 'Folder', '', exclude_from_nav=True)
    createChamada(site, 'iptu', 'IPTU', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwxMDc2LDExNDYsOTUx')
    createChamada(site, 'bilhete-unico', 'Bilhete Único', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwzOSw0MDgsNDE3LDEwNw')
    createChamada(site, 'consulta-itinerario', 'Consulta Itinerário', 'mais-buscados', 'http://www.sptrans.com.br/itinerarios/')
    createChamada(site, 'iluminacao-publica', 'Iluminação Pública', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwzMiw5ODUsMTE1Mg')
    createChamada(site, 'coleta-de-lixo', 'Coleta de Lixo', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwzMiwxMDUyLDExNTk=')
    createChamada(site, 'rede-municipal-de-saude', 'Rede municipal de saúde', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwzNiwxMTU0')
    createChamada(site, 'nota-fiscal-paulistana', 'Nota fiscal Paulistana', 'mais-buscados', '/portal/secoes/nav-empresa/#/MiwxMTU=')
    createChamada(site, 'construcoes-e-reformas', 'Construções e reformas', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwxMDc2LDExMjQ=')
    createChamada(site, 'vagas-em-escolas', 'Vagas em escolas', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwzNCw5MzMsNjIw')
    createChamada(site, 'operacao-cata-bagulho', 'Operação Cata-Bagulho', 'mais-buscados', '/portal/secoes/nav-cidadao/#/MSwzMiwxMDUyLDExNjY=')
