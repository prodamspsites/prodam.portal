# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from plone import api


class governoMunicipal(BrowserView):

    def getSecretarias(self):
        secretarias = '<select name="lista-secretarias" id="lista-secretarias" class="lista-institucionais leave-page w50 lista-secretarias"><option disabled="" selected="" value="Secretarias">Secretarias</option>'
        portal = api.portal.get()
        try:
            rodape = portal['rodape']
            linkSecretarias = rodape.restrictedTraverse('prefeitura/secretarias')
            path = '/'.join(linkSecretarias.getPhysicalPath())
            link = portal.portal_catalog(path=path, portal_type="Link")
            for i in link:
                secretarias += '<option value="' + i.getObject().remoteUrl + '">' + i.Title + '</option>'
        except:
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/assistencia_social/">Assistência Social</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/comunicacao">Comunicação</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/controladoria_geral/">Controladoria Geral do Município</option>'
            secretarias += '<option value="http://cultura.prefeitura.sp.gov.br/">Cultura</option>'
            secretarias += '<option value="http://smdu.prefeitura.sp.gov.br/">Desenvolvimento Urbano</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos">Direitos Humanos e Cidadania</option>'
            secretarias += '<option value="http://educacao.prefeitura.sp.gov.br/">Educação</option>'
            secretarias += '<option value="http://esportes.prefeitura.sp.gov.br/">Esportes</option>'
            secretarias += '<option value="http://financas.prefeitura.sp.gov.br/">Finanças e Desenv. Econômico</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/gestao/">Gestão</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/governo/">Governo</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/habitacao/">Habitação</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/infraestrutura/">Infraestrutura Urbana</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/licenciamentos/">Licenciamento</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/negocios_juridicos/">Negócios Jurídicos</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/pessoa_com_deficiencia/">Pessoa com Deficiência</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/politicas_para_as_mulheres/">Políticas para as Mulheres</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/igualdade_racial/">Promoção da Igualdade Racial</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/relacoes_governamentais/">Relações Governamentais</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/relacoes_internacionais/">Relações Internacionais e Federativas</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/saude">Saúde</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/seguranca_urbana/">Segurança Urbana</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/servicos/">Serviços</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/subprefeituras/">Subprefeituras</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/trabalho/">Trabalho e Empreendedorismo</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/transportes">Transportes</option>'
            secretarias += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/meio_ambiente/">Verde e Meio Ambiente</option>'

        secretarias += '</select>'
        return secretarias

    def getSubPrefeituras(self):
        subprefeituras = '<select name="lista-subprefeituras" id="lista-subprefeituras" class="lista-institucionais leave-page lista-subprefeituras"><option disabled="" selected="" value="Subprefeituras">Subprefeituras</option>'
        portal = api.portal.get()

        try:
            rodape = portal['rodape']
            linkSubPrefeituras = rodape.restrictedTraverse('prefeitura/subprefeituras')
            path = '/'.join(linkSubPrefeituras.getPhysicalPath())
            link = portal.portal_catalog(path=path, portal_type="Link")
            for i in link:
                subprefeituras += '<option value="' + i.getObject().remoteUrl + '">' + i.Title + '</option>'

        except:
            subprefeituras += '<option value="http://aricanduva.prefeitura.sp.gov.br">Aricanduva/V.Formosa</option>'
            subprefeituras += '<option value="http://butanta.prefeitura.sp.gov.br">Butantã</option>'
            subprefeituras += '<option value="http://campolimpo.prefeitura.sp.gov.br">Campo Limpo</option>'
            subprefeituras += '<option value="http://capeladosocorro.prefeitura.sp.gov.br">Capela do Socorro</option>'
            subprefeituras += '<option value="http://casaverde.prefeitura.sp.gov.br/">Casa Verde</option>'
            subprefeituras += '<option value="http://cidadeademar.prefeitura.sp.gov.br">Cidade Ademar</option>'
            subprefeituras += '<option value="http://cidadetiradentes.prefeitura.sp.gov.br">Cidade Tiradentes</option>'
            subprefeituras += '<option value="http://ermelinomatarazzo.prefeitura.sp.gov.br">Ermelino Matarazzo</option>'
            subprefeituras += '<option value="http://freguesia.prefeitura.sp.gov.br">Freguesia do Ó/Brasilândia</option>'
            subprefeituras += '<option value="http://guaianases.prefeitura.sp.gov.br">Guaianases</option>'
            subprefeituras += '<option value="http://ipiranga.prefeitura.sp.gov.br">Ipiranga</option>'
            subprefeituras += '<option value="http://itaimpaulista.prefeitura.sp.gov.br">Itaim Paulista</option>'
            subprefeituras += '<option value="http://itaquera.prefeitura.sp.gov.br">Itaquera</option>'
            subprefeituras += '<option value="http://jabaquara.prefeitura.sp.gov.br">Jabaquara</option>'
            subprefeituras += '<option value="http://jacana-tremembe.prefeitura.sp.gov.br">Jaçanã/Tremembé</option>'
            subprefeituras += '<option value="http://lapa.prefeitura.sp.gov.br">Lapa</option>'
            subprefeituras += '<option value="http://mboimirim.prefeitura.sp.gov.br">M Boi Mirim</option>'
            subprefeituras += '<option value="http://mooca.prefeitura.sp.gov.br">Mooca</option>'
            subprefeituras += '<option value="http://parelheiros.prefeitura.sp.gov.br">Parelheiros</option>'
            subprefeituras += '<option value="http://penha.prefeitura.sp.gov.br">Penha</option>'
            subprefeituras += '<option value="http://perus.prefeitura.sp.gov.br">Perus</option>'
            subprefeituras += '<option value="http://pinheiros.prefeitura.sp.gov.br">Pinheiros</option>'
            subprefeituras += '<option value="http://pirituba.prefeitura.sp.gov.br">Pirituba/Jaraguá</option>'
            subprefeituras += '<option value="http://santana-tucuruvi.prefeitura.sp.gov.br">Santana/Tucuruvi</option>'
            subprefeituras += '<option value="http://santoamaro.prefeitura.sp.gov.br">Santo Amaro</option>'
            subprefeituras += '<option value="http://saomateus.prefeitura.sp.gov.br">São Mateus</option>'
            subprefeituras += '<option value="http://saomiguel.prefeitura.sp.gov.br">São Miguel</option>'
            subprefeituras += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/subprefeituras/sapopemba/">Sapopemba</option>'
            subprefeituras += '<option value="http://se.prefeitura.sp.gov.br/">Sé</option>'
            subprefeituras += '<option value="http://vilamaria-vilaguilherme.prefeitura.sp.gov.br">V.Maria/V.Guilherme</option>'
            subprefeituras += '<option value="http://vilamariana.prefeitura.sp.gov.br">Vila Mariana</option>'
            subprefeituras += '<option value="http://vilaprudente.prefeitura.sp.gov.br">Vila Prudente</option>'

        subprefeituras += '</select>'
        return subprefeituras

    def getOrgaos(self):
        orgaos = '<select name="lista-orgaos" id="lista-orgaos" class="lista-institucionais leave-page w50 lista-orgaos"><option disabled="" selected="" value="Orgaos">Outros órgãos</option>'
        portal = api.portal.get()

        try:
            rodape = portal['rodape']
            linkorgaos = rodape.restrictedTraverse('prefeitura/outros-orgaos')
            path = '/'.join(linkorgaos.getPhysicalPath())
            link = portal.portal_catalog(path=path, portal_type="Link")
            for i in link:
                orgaos += '<option value="' + i.getObject().remoteUrl + '">' + i.Title + '</option>'

        except:
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/ahm">Autarquia Hospitalar do Município de São Paulo - AHMSP</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/desenvolvimento_urbano/ctlu/index.php?p=853">Câmara Técnica de Legislação Urbanística – CTLU</option>'
            orgaos += '<option value="http://www.cgesp.org/">Centro de Gerenciamento de Emergências - CGE</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/licenciamentos/colegiados/index.php?p=148606">Comissão de Análise Integrada de Projetos de Edificações e de Parcelamento do Solo – CAIEPS</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/licenciamentos/colegiados/index.php?p=148608">Comissão de Avaliação de Empreendimentos Habitacionais de Interesse Social – CAEHIS</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/licenciamentos/colegiados/index.php?p=148605">Comissão de Edificações e Uso do Solo - CEUSO</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/desenvolvimento_urbano/cppu/index.php?p=16200">Comissão de Proteção à Paisagem Urbana – CPPU</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/orgaos_colegiados/index.php?p=204">Comissão Municipal de Direitos Humanos</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/poprua/comite/index.php?p=150036">Comitê Intersetorial da Política Municipal para a População em Situação de Rua</option>'
            orgaos += '<option value="http://www.cetsp.com.br/">Companhia de Engenharia de Trafégo - CET</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/habitacao/cohab/">Companhia Metropolitana de Habitação de São Paulo - COHAB-SP</option>'
            orgaos += '<option value="http://transparencia.prefeitura.sp.gov.br/admindireta/empresas/Paginas/SPSEC.aspx">Companhia Paulista de Securitização - SPSEC</option>'
            orgaos += '<option value="http://transparencia.prefeitura.sp.gov.br/admindireta/empresas/Paginas/SPDA.aspx">Companhia São Paulo de Desenvolvimento e Mobilização de Ativos - SPDA</option>'
            orgaos += '<option value="http://conselhodacidade.prefeitura.sp.gov.br/">Conselho da Cidade de São Paulo</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/desenvolvimento_urbano/fundurb/index.php?p=155886">Conselho Gestor do Fundo de Desenvolvimento Urbano - FUNDURB</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/educacao/cme/">Conselho Municipal da Educação - CME</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/pessoa_com_deficiencia/conselho/">Conselho Municipal da Pessoa com Deficiência - CMPD</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/assistencia_social/comas/">Conselho Municipal de Assistência Social - COMAS</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/lgbt/conselho/index.php?p=150958">Conselho Municipal de Atenção à Diversidade Sexual</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/trabalho/cmcti/">Conselho Municipal de Ciência, Tecnologia &amp; Inovação - CMCTI</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/habitacao/organizacao/cmh/index.php?p=139">Conselho Municipal de Habitação - CMH</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/desenvolvimento_urbano/cmpu/index.php?p=144874">Conselho Municipal de Política Urbana – CMPU</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/cultura/conpresp/">Conselho Municipal de Preservação ao Patrimônio Histórico - CONPRESP</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/saude/conselho_municipal/">Conselho Municipal de Saúde - CMS</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/subprefeituras/abastecimento/comusan/index.php?p=26221">Conselho Municipal de Segurança Alimentar e Nutricional - COMUSAN</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/planejamento/cmi/">Conselho Municipal de Tecnologia de Informação e Comunicação - CMTIC</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/financas/institucional/index.php?p=3182">Conselho Municipal de Tributos - CMT</option>'
            orgaos += '<option value="http://www.cidadedesaopaulo.com/comtur/">Conselho Municipal de Turismo - COMTUR</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/meio_ambiente/cades/index.php?p=3250">Conselho Municipal do Meio Ambiente e Desenvolvimento Sustentável - CADES</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/juventude/conselho/index.php?p=149694">Conselho Municipal dos Direitos da Juventude</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/direito_a_memoria_e_a_verdade/">Coordenação de Direito à Memória e à Verdade</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/edh/">Coordenação de Política sobre Drogas</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/poprua/">Coordenação de Políticas para a População em Situação de Rua</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/criancas_e_adolescentes/">Coordenação de Políticas para Crianças e Adolescentes</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/idosos/">Coordenação de Políticas para Idosos</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/juventude/">Coordenação de Políticas para Juventude</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/lgbt/">Coordenação de Políticas para LGBT</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/migrantes/">Coordenação de Políticas para Migrantes</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/servicos/inclusao_digital/">Coordenadoria de Conectividade e Convergência Digital - CCCD</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/seguranca_urbana/defesa_civil/">Defesa Civil</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/planejamento/prodam/">Empresa de Tecnologia da Informação e Comunicação do Município de São Paulo - PRODAM</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/planejamento/fundacao_paulistana/apresentacao/index.php?p=25342">Fundação Paulistana de Educação e Tecnologia</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/cultura/noticias/?p=9064">Fundação Theatro Municipal de São Paulo</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/direitos_humanos/idosos/conselho/">Grande Conselho Municipal do Idoso</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/seguranca_urbana/guarda_civil/">Guarda Municipal Metropolitana - GCM</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/saude/hospital_do_servidor_publico_municipal/">Hospital do Servidor Público Municipal - HSPM</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/saude/hospital_municipal_infantil_menino_jesus/">Hospital Municipal Infantil Menino Jesus - HMIMJ</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/iprem">Instituto de Previdência Municipal de São de Paulo - IPREM-SP</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/ouvidoria/">Ouvidoria Geral do Municipio de São Paulo - OGM</option>'
            orgaos += '<option value="http://www.spnegocios.com/">São Paulo Negócios - SP Negócios</option>'
            orgaos += '<option value="http://www.spobras.sp.gov.br/">São Paulo Obras - SPObras</option>'
            orgaos += '<option value="http://www.sptrans.com.br/">São Paulo Transportes - SPTrans</option>'
            orgaos += '<option value="http://www.cidadedesaopaulo.com/">São Paulo Turismo - SPTuris</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/desenvolvimento_urbano/sp_urbanismo/">São Paulo Urbanismo - SPUrbanismo</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/servicos/servico_funerario/">Serviço Funerário do Município de São de Paulo - SFMSP</option>'
            orgaos += '<option value="http://www.prefeitura.sp.gov.br/cidade/secretarias/trabalho/abastecimento/">Supervisão Geral de Abastecimento - SGA</option>'

        orgaos += '</select>'
        return orgaos
