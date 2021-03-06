# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from StringIO import StringIO
from bs4 import BeautifulSoup
from cookielib import CookieJar
from gzip import GzipFile
from lxml import etree
from plone.memoize import ram
from time import localtime
from time import time
from twitter import Api
from urllib import urlencode
from urllib2 import HTTPCookieProcessor
from urllib2 import HTTPError
from urllib2 import ProxyHandler
from urllib2 import Request
from urllib2 import build_opener
try:
    import cPickle as pickle
except ImportError:
    import pickle


url_direct = {'pref-sp': 'http://www.capital.sp.gov.br/portal/',
              'transp-cptm': "http://www.cptm.sp.gov.br/Pages/Home.aspx",
              'transp-metro': "http://www.metro.sp.gov.br/Sistemas/direto-do-metro-via4/diretodoMetroHome.aspx",
              'transito-agora': "http://cetsp1.cetsp.com.br/monitransmapa/agora/",
              'qualidade-oxigenio': "http://sistemasinter.cetesb.sp.gov.br/Ar/php/ar_resumo_hora.php",
              'dash-aero': "http://voos.infraero.gov.br/hstvoos/RelatorioPortal.aspx",
              'ex-clima': "http://www.cgesp.org/v3/previsao_prefeitura_xml.jsp",
              'dash-rodisio': "http://misc.prefeitura.sp.gov.br/pmspws/rotation/data.json",
              'dash-aero-situacao': "http://www.infraero.gov.br/situacaoaeroporto/",
              'ex-clima-media': "http://www.saisp.br/cgesp/temp_media_prefeitura_sp.jsp"}


class StringCookieJar(CookieJar):
    def __init__(self, string=None, policy=None):
        CookieJar.__init__(self, policy)
        if string:
            self._cookies = pickle.loads(string)


class SpAgora(BrowserView):
    """
    return: content to site url_direct
    """
    soup = None
    tree = None

    def __init__(self, context, request, state=None, proxy=None, max_retries=3):
        """Classe para fazer scrap class spagora args:
        @state: Estado de scrapper anterior obtido via .get_state()
        @proxy: Proxy HTTP
        """
        self.context = context
        self.request = request
        self.max_retries = max_retries
        if state:
            self._form_data = state['form_data']
            self._cj = StringCookieJar(state['cookies'])
        else:
            self._cj = StringCookieJar()

        cookie_handler = HTTPCookieProcessor(self._cj)
        if proxy is None:
            self._opener = build_opener(cookie_handler)
        else:
            proxy_handler = ProxyHandler({'http': proxy, })
            self._opener = build_opener(cookie_handler, proxy_handler)

    def getContent(self, url, data=None, referer=None):
        """
        return content cookie html in response decode utf-8 to BeautifulSoup
        """
        encoded_data = urlencode(data) if data else None
        # if referer is None: url
        default_headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9 ( .NET CLR 3.5.30729; .NET4.0E)',
                           'Accept-Language': 'pt-br;q=0.5',
                           'Accept-Charset': 'utf-8;q=0.7,*;q=0.7',
                           'Accept-Encoding': 'gzip',
                           'Connection': 'close',
                           'Cache-Control': 'no-cache',
                           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                           'Referer': referer}

        req = Request(url, encoded_data, default_headers, origin_req_host=referer)

        retries = 0
        try:
            handle = self._opener.open(req)
        except HTTPError:
            retries += 1
            if retries > self.max_retries:
                raise
        if handle.info().get('Content-Encoding') == 'gzip':
            data = handle.read()
            buf = StringIO(data)
            f = GzipFile(fileobj=buf)
            response = f.read()
        else:
            response = handle.read()
        # return response.decode('utf-8')
        return response

    """
    ##########################################################################
                                  SpAgora capa
    ##########################################################################
    """
    @ram.cache(lambda *args: time() // (60 * 15))
    def getPrincipal(self):
        """
        return content head apresentation ['in the morning','in the afternoon','in the evening','at night']
        """
        try:
            self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima-media")))
            temp_media = self.getTempMedia()
            hour = localtime(time()).tm_hour
            self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima")))
            prevision = self.getHour(hour)

            content = '<ul id="servicos-externos" style="display: block;">' \
                      '<li class="ex-clima"><div class="dash-border"><strong class="titulo-dash">Tempo' \
                      '</strong><div class="tempo-g nb"></div><div class="t-media"><span>Média</span>' \
                      '<span id="CGE-media" class="amarelo bold">' + temp_media + '</span></div><div class="tempestade">' \
                      '<span>Potencial <div class="raio"></div></span>' \
                      '<span id="status-temp" class="amarelo">' + prevision + '</span></div></div>' \
                      '<div class="ex-hover"><div></div></div></li>'
        except:
            content = self.getContentExcept(class_li='ex-clima', text_div='CGEb')

        try:
            self.soup = BeautifulSoup(self.getContent(url_direct.get('qualidade-oxigenio')))
            qualidade_ar = self.getDescQualidade()
            content += '<!-- AR -->' \
                       '<li class="ex-ar"><div class="dash-border"><strong class="titulo-dash">Qualidade do Ar</strong>'\
                       '<div class="dash-img o2quali"></div><b class="bullet-verde em2">' + qualidade_ar + '</b></div>' \
                       '<div class="ex-hover"><div></div></div></li>'
        except:
            content += self.getContentExcept(class_li='ex-ar', text_div='Qualidade do Ar')

        content += '<!-- Aeroportos -->' \
                   '<li class="ex-aero">' \
                   '<div class="dash-border"><strong class="titulo-dash">Aero</strong>' \
                   '<br>Consultar situação</div>' \
                   '</li>'

        content += '<!-- Transporte público -->' \
                   '<li class="ex-publico">' \
                   '<div class="dash-border">' \
                   '<strong class="titulo-dash">Transporte Público</strong>' \
                   '<div class="dash-img"></div>' \
                   '<a href="http://www.sptrans.com.br/itinerarios/" target="_blank" class="azul-pq">Busca de itinerários</a>' \
                   '</div>' \
                   '<div class="ex-hover"><div></div></div>' \
                   '</li>'

        try:
            self.soup = BeautifulSoup(self.getContent(url_direct.get('transito-agora')))
            lentidao = self.getLentidao()
            content += '<!-- Trânsito-->' \
                       '<li class="ex-transito"><div class="dash-border"><strong class="titulo-dash">' \
                       'Trânsito</strong><div class="dash-img semaforo"></div>' \
                       '<b class="amarelo em15" id="lento">' + lentidao + 'km</b><br>' \
                       '<span class="em09 bold">de lentidão</span><br><span class="kmStatus verde">' \
                       '<i class="ball-status verde"></i>livre</span></div><div class="ex-hover"><div></div></div></li>'
        except:
            content += self.getContentExcept(class_li='ex-transito', text_div='Transito')

        try:
            self.soup = BeautifulSoup(self.getContent(url_direct.get('dash-rodisio')))
            placa_rodisio = self.getRestricaoPlacaFinal()
            content += '<!-- Rodizio -->' \
                       '<li class="ex-rodizio">' \
                       '<div class="dash-border"><strong class="titulo-dash">Rodízio</strong>' \
                       '<div class="dash-img"></div><b id="rodizio_hoje"></b>Placas final <br>' \
                       '<b class="azul-gd">' + placa_rodisio + '</b> </div><div class="ex-hover">' \
                       '<div></div></div>' \
                       '</li></ul>'
        except:
            content += self.getContentExcept(class_li='ex-rodizio', text_div='Rodízio')
        return content

    def getHour(self, hour):
        if int(hour) >= 6 and int(hour) < 13:
            return self.getPrevManha()
        elif int(hour) >= 13 and int(hour) < 19:
            return self.getPrevTarde()
        elif int(hour) >= 19 and int(hour) <= 23:
            return self.getPrevNoite()
        elif int(hour) >= 0 and int(hour) < 6:
            return self.getPrevMadrugada()

    def getContentExcept(self, class_li, text_div):
        """
        return content to except in case error
        """
        content = '<li class="' + class_li + '">' \
                  '<div class="dash-border"><strong class="titulo-dash">' + text_div + '</strong>' \
                  '<br>Não foi possível carregar informações</div>' \
                  '</li>'
        return content

    """
    ##########################################################################
                               Clima & Temperatura
    ##########################################################################
    """
    prevision = {'NB': 'Nubrado',
                 'EN': 'Encoberto',
                 'PI': 'Pancadas Isoladas',
                 'PC': 'Pancadas Chuvas',
                 'CV': 'Chuva'}

    @ram.cache(lambda *args: time() // (60 * 15))
    def getClima(self):
        """
        return: content clima and details

        """
        self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima-media")))
        temp_media = self.getTempMedia()

        self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima")))
        temp_maxima = self.getTempMaxima()
        temp_minima = self.getTempMinima()
        prev_manha = self.getPrevManha()
        prev_tarde = self.getPrevTarde()
        prev_noite = self.getPrevNoite()
        prev_madrugada = self.getPrevMadrugada()
        umidade_ar_max = self.getUmidadeArMax()
        umidade_ar_min = self.getUmidadeArMin()
        hora_nascer_sol = self.getHoraNascerSol()
        hora_por_sol = self.getHoraPorSol()

        clima_html = '<div id="call-clima" class="dash" style="display: block;">' \
                     '<h3>' \
                     'Tempo ' \
                     '<em class="fonte">Fonte: CGE</em>' \
                     '</h3> ' \
                     '<button class="fechar-dash">X</button>' \
                     '<div id="temp-bloco">' \
                     '<div id="t-agora" class="tempo-g nb"></div>' \
                     '<div id="t-media">' \
                     '<small class="em08">Temperatura Média</small>' \
                     '<br>' \
                     '<span id="temp-media" class="amarelo em18">' \
                     '%s° </span>' % temp_media + \
                     '</div>' \
                     '<div id="minXmax">' \
                     '<div id="new-max">' \
                     '<span class="tmax"></span>' \
                     '%s°' % temp_maxima + \
                     '</div>' \
                     '<div id="new-min">' \
                     '<span class="tmin"></span>' \
                     '%s°' % temp_minima + \
                     '</div>' \
                     '</div>' \
                     '</div>' \
                     '<ul id="dia-todo">' \
                     '<li>' \
                     '<strong class="azul-pq em08">Manhâ</strong>' \
                     '<div class="tempo-p nb-pq"></div>' \
                     '<div class="raio"></div>' \
                     '<span class="em07 bold amarelo">' \
                     '%s </span>' % prev_manha + \
                     '</li>' \
                     '<li>' \
                     '<strong class="azul-pq em08">Tarde</strong>' \
                     '<div class="tempo-p pi-pq"></div>' \
                     '<div class="raio"></div>' \
                     '<span class="em07 bold amarelo">' \
                     '%s </span>' % prev_tarde + \
                     '</li>' \
                     '<li>' \
                     '<strong class="azul-pq em08">Noite</strong>' \
                     '<div class="tempo-p nb-pq-noite"></div>' \
                     '<div class="raio"></div>' \
                     '<span class="em07 bold amarelo">' \
                     '%s </span>' % prev_noite + \
                     '</li>' \
                     '<li>' \
                     '<strong class="azul-pq em08">Madrugada</strong>' \
                     '<div class="tempo-p pc-pq-noite"></div>' \
                     '<div class="raio"></div>' \
                     '<span class="em07 bold amarelo">' \
                     '%s </span>' % prev_madrugada + \
                     '</li>' \
                     '</ul>' \
                     '<div id="tempor-outras">' \
                     '<div class="a-40 bold">' \
                     '<small class="em07">' \
                     '<span id="div" class="gotas"></span>' \
                     'Umidade relativa do ar' \
                     '</small>' \
                     '<div class="a-half em13">' \
                     '<span class="tmax"></span> ' \
                     '%s' % umidade_ar_max + \
                     '</div>' \
                     '<div class="a-half em13">' \
                     '<span class="tmin"></span> ' \
                     '%s' % umidade_ar_min + \
                     '</div>' \
                     '</div>' \
                     '<div class="sol-box">' \
                     '<div id="sol"></div>' \
                     '<div class="a-half">' \
                     '<small class="amarelo em14">' \
                     '%s </small> ' % hora_nascer_sol + \
                     '<small class="em07">Nascer do sol</small>' \
                     '</div>' \
                     '<div class="a-half">' \
                     '<small class="amarelo em14">' \
                     '%s </small> ' % hora_por_sol + \
                     '<small class="em07">Por do sol</small>' \
                     '</div>' \
                     '</div>' \
                     '</div>' \
                     '</div>'
        return clima_html

    @ram.cache(lambda *args: time() // (60 * 15))
    def getTempMedia(self):
        """
        return temperature median in moment
        """
        temp_media = float(self.soup.media.text)
        temperature = str(int(round(temp_media)))
        return temperature

    @ram.cache(lambda *args: time() // (60 * 15))
    def getPrevision(self, period=None):
        """
        :return: prevision time in day
        """
        try:
            prevision = str(self.soup.dia.findAll('ct', {'periodo': period})[0].text[-2:])
            prevision = self.prevision.get(prevision)
            return prevision
        except:
            print('Type of weather forecasting not set ')

    @ram.cache(lambda *args: time() // (60 * 15))
    def getWeather(self, type):
        """
        :return: weather condicion in day
        """
        return self.soup.dia.findAll(type)[0].text

    @ram.cache(lambda *args: time() // (60 * 15))
    def getTempMaxima(self):
        """
        return time morning
        """
        temp_max = str(self.getWeather('temp-max')[:-2])
        return temp_max

    @ram.cache(lambda *args: time() // (60 * 15))
    def getTempMinima(self):
        """
        return temperature minimo
        """
        temp_min = str(self.getWeather('temp-min')[:-2])
        return temp_min

    @ram.cache(lambda *args: time() // (60 * 15))
    def getPrevManha(self):
        """
        return prevision time morning
        """
        return self.getPrevision('Manhã')

    @ram.cache(lambda *args: time() // (60 * 15))
    def getPrevTarde(self):
        """
        return time afternoon
        """
        return self.getPrevision('Tarde')

    @ram.cache(lambda *args: time() // (60 * 15))
    def getPrevNoite(self):
        """
        return time night
        """
        return self.getPrevision('Noite')

    @ram.cache(lambda *args: time() // (60 * 15))
    def getPrevMadrugada(self):
        """
        return time dawn
        """
        return self.getPrevision('Madrugada')

    @ram.cache(lambda *args: time() // (60 * 15))
    def getUmidadeArMax(self):
        """
        return unit ar max
        """
        return str(self.getWeather('umid-max')[:2]) + '%'

    @ram.cache(lambda *args: time() // (60 * 15))
    def getUmidadeArMin(self):
        """
        return unit ar min
        """
        return str(self.getWeather('umid-min')[:2]) + '%'

    @ram.cache(lambda *args: time() // (60 * 15))
    def getHoraNascerSol(self):
        """
        return hour sunrise
        """
        return str(self.getWeather('sunrise')[:-1])

    @ram.cache(lambda *args: time() // (60 * 15))
    def getHoraPorSol(self):
        """
        return sunset time
        """
        return str(self.getWeather('sunset')[:-1])

    """
    ##########################################################################
                               Qualidade do Ar
    ##########################################################################
    """
    @ram.cache(lambda *args: time() // (60 * 15))
    def getQualidadeAr(self):
        """
        return: content qualidade do ar
        """
        self.soup = BeautifulSoup(self.getContent(url_direct.get("qualidade-oxigenio")))
        tips = self.getEfeitoSaude()

        quality_ar_html = '<div id="call-ar" class="dash" style="display: block;">' \
                          '<h3>' \
                          'Qualidade do Ar ' \
                          '<em class="fonte">Fonte: CETESB</em>' \
                          '</h3> ' \
                          '<button class="fechar-dash">X</button>' \
                          '<div class="O2"></div>' \
                          '<div id="o2mapa">' \
                          '<div class="kineticjs-content" role="presentation" style="position: relative; display: inline-block; width: 300px; height: 160px;">' \
                          '<canvas width="300" height="160" style="padding: 0px; margin: 0px; border: 0px; position: absolute; top: 0px; left: 0px; ' \
                          'width: 300px; height: 160px; background: transparent;"></canvas>' \
                          '</div>' \
                          '</div>' \
                          '<ol id="dica">'
        for tip in tips:
            quality_ar_html += '<li>' \
                               '<i></i>' + tip['quality'] + '</li>'
        quality_ar_html += '</ol> </div>'
        return quality_ar_html

    @ram.cache(lambda *args: time() // (60 * 15))
    def getEfeitoSaude(self):
        """
        return list efect quality life
        """
        list_quality = []
        content_list = self.soup.findAll('td', {'colspan': '4', 'bgcolor': '#e2ecf5'})
        for quality in content_list:
            _quality = quality.text[2:].strip()
            if _quality != '--':
                list_quality.append({'quality': _quality})
        return list_quality

    @ram.cache(lambda *args: time() // (60 * 15))
    def getDescQualidade(self, local='Itaquera'):
        """
        return type description qualidaty atmosfera
        """
        quality = int(self.soup.find('td', text=local).parent.find('td', width=50).text)
        if quality >= 0 and quality <= 40:
            descript = 'Boa'
        elif quality >= 41 and quality <= 80:
            descript = 'Moderado'
        elif quality >= 81 and quality <= 120:
            descript = 'Ruim'
        elif quality >= 121 and quality <= 200:
            descript = 'Muito Ruim'
        elif quality >= 200:
            descript = 'Pessimo'
        return descript

    """
    ##########################################################################
                            Situação Aeroportos
    ##########################################################################
    """
    list_aeport = {'sbsp': {'codigo': 'CGH',
                            'name': 'Congonhas',
                            'local': 'Sao Paulo - Congonhas-SP',
                            'site': 'http://www.infraero.gov.br/index.php/aeroportos/sao-paulo/aeroporto-de-sao-paulo-congonhas.html'},
                   'sbgr': {'codigo': 'GRU',
                            'name': 'Guarulhos',
                            'local': 'Sao Paulo - Guarulhos-SP',
                            'site': 'http://www.gru.com.br/pt-br'},
                   'sbmt': {'codigo': 'MAE',
                            'name': 'Cpo. de Marte',
                            'local': 'Sao Paulo - Cpo de Marte-SP',
                            'site': 'http://www.infraero.gov.br/index.php/aeroportos/sao-paulo/aeroporto-campo-de-marte.html'},
                   'sbkp': {'codigo': 'VCP',
                            'name': 'Viracopos',
                            'local': 'Campinas-SP',
                            'site': 'http://www.viracopos.com/passageiros/voos/'}}

    situation_aeport = {'pontoVerde': 'Operando Normalmente',
                        'pontoAmarelo': 'Restrições meteorológicas',
                        'pontoVermelho': 'Fechado operações',
                        'pontoBranco': 'Indisponivel no momento'}

    @ram.cache(lambda *args: time() // (60 * 15))
    def getAeroporto(self):
        """
        return: content situation aeroport and conditional voo
        """
        aeport_html = '<div id="call-aero" class="dash" style="display: block;">' \
                      '<h3>' \
                      'Aeroportos '\
                      '<em class="em08 fonte">Fonte: Infraero e GRU</em>' \
                      '</h3>' \
                      '<button class="fechar-dash">X</button>' \
                      '<ul id="aero-lista">'

        list_aeport_voo = None
        list_aeport_status = self.getSituacaoAeroporto()
        list_aeport_voo = self.getSituacaoAeroportoVoo(list_aeport_status)
        for aeport in list_aeport_voo:
            cod_aeport = aeport.get('codigo')
            cod_aeport_class = cod_aeport.lower()
            name_aeport = aeport.get('name')
            status_aeport = aeport.get('status')
            name_class = aeport.get('name_class')
            voo_atrasado = aeport.get('atrasados')
            voo_cancelado = aeport.get('cancelados')
            site_aeport = aeport.get('site')

            aeport_html += '<li class="%s"><strong class="aeronome">' % cod_aeport_class + \
                           '<abbr>%s</abbr> - %s</strong>' % (cod_aeport, name_aeport) + \
                           '<br><span class="%s"><b class="ball-status %s">' % (name_class, name_class) + \
                           '</b>%s</span>' % status_aeport

            if voo_atrasado is None or voo_cancelado is None:
                aeport_html += '<br><a href="%s"' % site_aeport + \
                               'class="link-aero" target="_blank">Clique e consulte</a>' \
                               '</li><li class="%s">' % cod_aeport
            else:
                aeport_html += '<small><strong class="aeronome"><br><span class="txt-right">Vôos atrasados:</span>' \
                               '<span class="txt-left azul-pq">%s</span>' % voo_atrasado + \
                               '<br><span class="txt-right">Vôos cancelados:</span>' \
                               '<span class="txt-left azul-pq">%s</span></small></li>' % voo_cancelado
        aeport_html += '</ul></div>'
        return aeport_html

    @ram.cache(lambda *args: time() // (60 * 15))
    def getSituacaoAeroporto(self):
        """
        return situation status retrict conditional aeport
        """
        soup = BeautifulSoup(self.getContent(url_direct.get('dash-aero-situacao')))
        list_situation = []
        for aeport in self.list_aeport.keys():
            element = soup.findAll('li', {'id': aeport})[0]
            name_class = element.get('class')[0]
            list_aeport = self.list_aeport.get(aeport)
            list_situation.append({'sigla': aeport,
                                   'name': list_aeport.get('name'),
                                   'local': list_aeport.get('local'),
                                   'codigo': list_aeport.get('codigo'),
                                   'status': self.situation_aeport.get(name_class),
                                   'name_class': name_class,
                                   'site': list_aeport.get('site')})
        return list_situation

    @ram.cache(lambda *args: time() // (60 * 15))
    def getSituacaoAeroportoVoo(self, list_aeport=[]):
        """
        return situation voo in aeport
        """
        soup = BeautifulSoup(self.getContent(url_direct.get('dash-aero')))
        aeport = None
        for aeport in list_aeport:
            aeport_status = soup.find('td', text=aeport.get('local'))
            if aeport_status:
                _aeport_status = aeport_status.parent.findAll('span')
                aeport['atrasados'] = str(_aeport_status[0].text)
                aeport['cancelados'] = str(_aeport_status[8].text)
            else:
                aeport['atrasados'] = None
                aeport['cancelados'] = None
        return list_aeport

    """
    ##########################################################################
                       Transporte Publico CPTM e Metro
    ##########################################################################
    """
    @ram.cache(lambda *args: time() // (60 * 15))
    def getTransportePublico(self):
        """
        return content transporte publico
        """
        # line_metro = []
        # transp_cptm = self.getStatusCptm()
        # transp_metro = self.getStatusMetro()

        # for metro in transp_metro:
        #     line_metro.append(metro.text.split('\n')[4].strip())
        circulacao_metro = None
        circulacao_cptm = None
        transp_publica_html = '<div id="call-publi" class="dash" style="display: block;">' \
                              '<h3>Transporte Público</h3> <button class="fechar-dash">X</button>' \
                              '<ul>' \
                              '<li>' \
                              '<div class="status"><i class="verde"></i></div>' \
                              '<div class="mini Mbus"></div>' \
                              '<span id="spT-twitter">Confira os itinerários das 151 linhas de ônibus do #Noturno,' \
                              'a Rede de ônibus da Madrugada: <a href="http://www.sptrans.co" target="_blank">Mais</a></span>' \
                              '</li>' \
                              '<li>' \
                              '<div class="status"><i class="amarelo"></i></div>' \
                              '<div class="mini Mmetro"></div>' \
                              '<span id="t-metro">%s</span>' % circulacao_metro + \
                              '</li>' \
                              '<li>' \
                              '<div class="status"><i class="vermelho"></i></div>' \
                              '<div class="mini Mcptm"></div>' \
                              '<span id="t-cptm">%s</span>' % circulacao_cptm + \
                              '</li>' \
                              '</ul>' \
                              '<a href="http://www.sptrans.com.br/itinerarios/" target="_blank" class="link-amarelo">Consultar itinerários</a>' \
                              '</div>'
        return transp_publica_html

    @ram.cache(lambda *args: time() // (60 * 15))
    def getStatusCptm(self):
        """
        return situation transport public cptm
        """
        soup = BeautifulSoup(self.getContent(url_direct.get('transp-cptm')))
        transp_cptm = soup.find('div', attrs={'class': 'situacao_linhas'}).findAll('span')
        situacao = [tag for tag in transp_cptm if "status_normal" in tag.attrs['class']]
        return situacao[0].text

    @ram.cache(lambda *args: time() // (60 * 15))
    def getStatusMetro(self):
        """
        return situation transport public
        """
        status_metro = []
        soup = BeautifulSoup(self.getContent(url_direct.get('transp-metro')))
        # import pdb; pdb.set_trace()
        transp_metro = soup.find('ul', {'id': 'statusLinhaMetro'}).findAll('div')
        for metro in transp_metro:
            status_metro.append(metro)
            # status_metro.append(metro.text.split('\n')[4].strip())
        return transp_metro

    """
    ##########################################################################
                                Transito por zona
    ##########################################################################
    """
    @ram.cache(lambda *args: time() // (60 * 15))
    def getTransito(self):
        """
        return: content transtito.
        """
        self.tree = etree.HTML(self.getContent(url_direct.get('transito-agora')))
        transito_zona_oeste = self.getTransZonaOeste()
        transito_zona_norte = self.getTransZonaNorte()
        transito_zona_leste = self.getTransZonaLeste()
        transito_zona_sul = self.getTransZonaSul()

        transito_html = '<div id="call-trans" class="dash" style="display: block;">' \
                        '<h3>Trânsito</h3>' \
                        '<button class="fechar-dash">X</button><div class="tran-total">' \
                        '<div class="ttotal"><span class="amarelo em14 bold">75 km</span>' \
                        '<br><small class="bold em09">de lentidão</small></div>' \
                        '<div class="ttotal amarelo"><br>' \
                        '<span class="amarelo bolinha"></span>regular</div></div>' \
                        '<hr class="pont"><div id="sp-mapa"><ul id="lentidao">' \
                        '<li id="kmOeste" class="amarelo">%s</li>' + transito_zona_oeste + \
                        '<li id="kmNorte" class="amarelo">%s</li>' % transito_zona_norte + \
                        '<li id="kmLeste" class="amarelo">%s</li>' % transito_zona_leste + \
                        '<li id="kmSul" class="amarelo">%s</li>' % transito_zona_sul + \
                        '</ul></div> <div class="bloco-linha">' \
                        '<a href="http://www.cetsp.com.br/transito-agora/mapa-de-fluidez.aspx" class="azul-pq" target="_blank">Mapa de fluidez</a>' \
                        '<a href="http://www.cetsp.com.br/transito-agora/transito-nas-principais-vias.aspx" target="_blank" class="azul-pq">Lentidão por corredor</a>' \
                        '</div></div>'
        return transito_html

    @ram.cache(lambda *args: time() // (60 * 15))
    def getContentTransito(self, chave):
        """
        return content transit with parameters id
        """
        content = self.tree.xpath("string(//div[@id='%s'])" % chave).split(' ')[0]
        return content

    @ram.cache(lambda *args: time() // (60 * 15))
    def getLentidao(self):
        """
        return showness in zone
        """
        lentidao = self.getContentTransito('lentidao')
        return lentidao

    @ram.cache(lambda *args: time() // (60 * 15))
    def getTransZonaNorte(self):
        """
        return transit in zone norte
        """
        trans_zona_norte = self.getContentTransito('NorteLentidao')
        return trans_zona_norte

    @ram.cache(lambda *args: time() // (60 * 15))
    def getTransZonaLeste(self):
        """
        return transit in zone leste
        """
        trans_zona_leste = self.getContentTransito('LesteLentidao')
        return trans_zona_leste

    @ram.cache(lambda *args: time() // (60 * 15))
    def getTransZonaCentro(self):
        """
        return transit in zone center
        """
        trans_zona_centro = self.getContentTransito('CentroLentidao')
        return trans_zona_centro

    @ram.cache(lambda *args: time() // (60 * 15))
    def getTransZonaOeste(self):
        """
        return transit in zone oeste
        """
        trans_zona_oeste = self.getContentTransito('OesteLentidao')
        return trans_zona_oeste

    @ram.cache(lambda *args: time() // (60 * 15))
    def getTransZonaSul(self):
        """
        return transit in zone sul
        """
        trans_zona_sul = self.getContentTransito('SulLentidao')
        return trans_zona_sul

    """
    ##########################################################################
                           Rodizio e Área de restrição
    ##########################################################################
    """
    @ram.cache(lambda *args: time() // (60 * 15))
    def getRodisio(self):
        """
        return: content rodozio
        """
        self.soup = BeautifulSoup(self.getContent(url_direct.get('dash-rodisio')))
        planas_final = self.getRestricaoPlacaFinal()
        placa_horario_inicio = self.getPlacaHorarioInicio()
        placa_horario_final = self.getPlacaHorarioFinal()
        rodizio_html = '<div id="call-rodizio" class="dash" style="display: block;">' \
                       '<h3>Rodízio</h3> ' \
                       '<button class="fechar-dash">X</button>' \
                       '<div id="mapa-rodizio"></div><ul class="rod-3col"><li>' \
                       '<span class="em08 bold">Placas final:</span><br>' \
                       '<span class="amarelo em15">%s</span></li><li>' % planas_final + \
                       '<span class="em08 bold">Horário:</span><br>' \
                       '<small class="amarelo em1">%s</small><br>' % placa_horario_inicio + \
                       '<small class="amarelo em1">%s</small></li>' % placa_horario_final + \
                       '<li><span class="em08 bold">Penalidade:</span><br>' \
                       '<small class="amarelo em10">R$85,13</small>' \
                       '<small class="amarelo em08"> e 4pts na carteira</small></li></ul></div>'
        return rodizio_html

    @ram.cache(lambda *args: time() // (60 * 15))
    def getRestricaoPlacaFinal(self):
        """
        return restrict placa final
        """
        import ast
        restricao_placa_final = ast.literal_eval(self.soup.text).get('Rotation').get('desc')
        return restricao_placa_final

    @ram.cache(lambda *args: time() // (60 * 15))
    def getPlacaHorarioInicio(self):
        """
        return placa horario inicio
        """
        placa_horario_inicio = '7h às 10h'
        return placa_horario_inicio

    @ram.cache(lambda *args: time() // (60 * 15))
    def getPlacaHorarioFinal(self):
        """
        return placa horario final
        """
        placa_horario_final = '17h às 20h'
        return placa_horario_final

    """
    ##########################################################################
                           Tweets
    ##########################################################################
    """

    @ram.cache(lambda *args: time() // (60 * 15))
    def getTweets(self, consumer_key='OOXF8haUGyWq2YNoSciDTLGXd', consumer_secret='sZfagT290goGqJG94H0Nng2gsEStqvpEbz3wEw0UTHgboxrUmh', access_token_secret='A0DEgOpSCTu44NZcyMHCtXdNBFq8vsFwMKSv7Neenl7AY', access_token='3397165841-g80Y2QqVEEjhzqMsQTDBpyWiz1Mcm0pwv519GfN', screen_name='saopaulo_agora', count=5):
        api = Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_token_secret)
        try:
            api.VerifyCredentials()
            statuses = api.GetUserTimeline(screen_name=screen_name)[:int(count)]
            ocorrencias = []

            for i in statuses:
                status = '<h4>Alertas <a href="https://twitter.com/%s">@%s</a></h4>' % (screen_name, screen_name)
                status += '<a href="https://twitter.com/' + screen_name + '/statuses/' + str(i.id) + '" target="_blank">' + str(i.text) + '<time>' + str(i.relative_created_at) + '</time></a>'
                ocorrencias.append(status)
            return ocorrencias
        except:
            return False
