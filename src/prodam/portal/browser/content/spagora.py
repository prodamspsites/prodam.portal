# -*- coding: utf-8 -*-
import urllib
import json
from Products.Five import BrowserView
from StringIO import StringIO
from bs4 import BeautifulSoup
from cookielib import CookieJar
from gzip import GzipFile
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
              'dash-rodizio': "http://misc.prefeitura.sp.gov.br/pmspws/rotation/data.json",
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
        return response

    @ram.cache(lambda *args: time() // (60 * 15))
    def getAirQuality(self):
        try:
            self.soup = BeautifulSoup(self.getContent(url_direct.get('qualidade-oxigenio')))
            qualidade_ar = self.getDescQualidade()
            content = qualidade_ar
        except:
            content = self.getContentExcept(class_li='ex-ar', text_div='Qualidade do Ar')
        return content

    @ram.cache(lambda *args: time() // (60 * 15))
    def getMeansOfTransportation(self):
        content = ''
        try:
            html_transporte_publico = self.getTransportePublico()
            content += html_transporte_publico
        except:
            content += self.getContentExcept(class_li='ex-transito', text_div='Transito')
        return content

    @ram.cache(lambda *args: time() // (60 * 15))
    def getTraffic(self):
        content = ''
        try:
            quantidade_km_transito = self.getTransito()
            content += quantidade_km_transito
        except:
            content += self.getContentExcept(class_li='ex-transito', text_div='Transito')
        return content

    @ram.cache(lambda *args: time() // (60 * 15))
    def getCarRotation(self):
        content = ''
        try:
            rodizio = self.getRodizio()
            content += rodizio
        except:
            content += self.getContentExcept(class_li='ex-rodizio', text_div='Rodízio')
        return content

    @ram.cache(lambda *args: time() // (60 * 15))
    def getAirportStatus(self):
        pass

    @ram.cache(lambda *args: time() // (60 * 15))
    def getAirportFlights(self):
        pass

    # @ram.cache(lambda *args: time() // (60 * 15))
    # def getWeatherSp(self):
    #   content = ''
    #   try:
    #       self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima-media")))
    #       temp_media = self.getTempMedia()
    #       hour = localtime(time()).tm_hour
    #       self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima")))
    #       prevision = self.getHour(hour)
    #       content += "<h5>Temperatura</h5>"
    #       content += 'Temperatura média: %s e Previsao: %s' % (temp_media, prevision)
    #       clima = self.getClima()
    #       content += "<h2>Clima</h2>"
    #       content += "<p>Clima: %s" % clima
    #   except:
    #       content = self.getContentExcept(class_li='ex-clima', text_div='CGEb')
    #   return content

    @ram.cache(lambda *args: time() // (60 * 15))
    def getPrincipal(self):
        content = ''

        self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima-media")))
        temp_media = self.getTempMedia()
        hour = localtime(time()).tm_hour
        self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima")))
        dia = self.soup.findAll('dia')
        potencial = dia[0].parent.find('ct', {'periodo': self.getPeriod(hour)})

        content += '<li class="ex-clima ver-mais">' \
                   '<a href="#verMais">' \
                   '<div class="dash-border">' \
                   '<strong class="titulo-dash">Tempo</strong>' \
                   '<div class="tempo-g nb"></div>' \
                   '<div class="t-media"><span>Média</span><span id="CGE-media" class="amarelo bold">' + temp_media + '°</span></div>' \
                   '<div class="tempestade">' \
                   '<span>Potencial <div class="raio"></div></span>' \
                   '<span id="status-temp" class="amarelo">' + str(potencial['pt']) + '</span>' \
                   '</div>' \
                   '</div>' \
                   '</a>' \
                   '</li>'

        content += '<li class="ex-ar ver-mais">' \
                   '<a href="#verMais">' \
                   '<div class="dash-border">' \
                   '<strong class="titulo-dash">Qualidade do Ar</strong>' \
                   '<div class="dash-img o2quali"></div>' \
                   '<b class="bullet-verde em2">' + self.getAirQuality() + '</b>' \
                   '</div>' \
                   '</a>' \
                   '</li>'

        content += '<li class="ex-aero ver-mais">' \
                   '<a href="#verMais">' \
                   '<div class="dash-border">' \
                   '<strong class="titulo-dash">Aeroportos</strong>' \
                   '<div class="dash-img"></div>' \
                   '<span id="aero-status">Consulte situação</span>' \
                   '</div>' \
                   '</a>' \
                   '</li>'

        content += '<li class="ex-publico ver-mais">' \
                   '<a href="#verMais">' \
                   '<div class="dash-border">' \
                   '<strong class="titulo-dash">Transporte Público</strong>' \
                   '<div class="dash-img"></div>' \
                   '<a href="http://www.sptrans.com.br/itinerarios/" target="_blank" class="azul-pq">Busca de itinerários</a>' \
                   '</div>' \
                   '</a>' \
                   '</li>'

        self.soup = BeautifulSoup(self.getContent(url_direct.get('transito-agora')))

        total_km_lentidao = self.soup.find('div', {"id": 'lentidao'}).string

        content += '<li class="ex-transito ver-mais">' \
                   '<a href="#verMais">' \
                   '<div class="dash-border">' \
                   '<strong class="titulo-dash">Trânsito</strong>' \
                   '<div class="dash-img semaforo"></div>' \
                   '<div id="call-trans" class="dash" style="display: block;">' \
                   '<div class="tran-total">' \
                   '<div class="ttotal"><span class="amarelo em14 bold"> ' + total_km_lentidao + 'km</span><br>' \
                   '<small class="bold em09">de lentidão</small></div>' \
                   '<span class="kmStatus verde"><i class="ball-status verde"></i>livre</span></div>' \
                   '</div></div>' \
                   '</a>' \
                   '</li>'

        url_rodizio = url_direct.get('dash-rodizio')
        placas_final_url_return = urllib.urlopen(url_rodizio)
        data_result = json.loads(placas_final_url_return.read())
        placa = data_result['Rotation']['desc']

        content += '<li class="ex-rodizio ver-mais">' \
                   '<div class="dash-border">' \
                   '<strong class="titulo-dash">Rodízio</strong>' \
                   '<div class="dash-img"></div>' \
                   '<ul class="rod-3col">' \
                   '<li><span class="em08 bold"><small>Placas final:</small></span><br><span class="azul-pq em15">' + str(placa) + '</span></li:' \
                   '</ul></div>' \
                   '</a>' \
                   '</li>'

        return content

    def getPeriod(self, hour):
        if int(hour) >= 6 and int(hour) < 13:
            return 'Manhã'
        elif int(hour) >= 13 and int(hour) < 19:
            return 'Tarde'
        elif int(hour) >= 19 and int(hour) <= 23:
            return 'Noite'
        elif int(hour) >= 0 and int(hour) < 6:
            return 'Madrugada'

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
    def getDescQualidade(self, local='Congonhas'):
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

    # @ram.cache(lambda *args: time() // (60 * 15))
    # def testeAeroporto(self):
    #     soup = BeautifulSoup(self.getContent(url_direct.get('dash-aero-situacao')))
    #     retorno = {}
    #     content = ''
    #     for aeroporto in self.list_aeport:
    #         aeroporto_congonhas = soup.find(id=aeroporto)
    #         situacao_aeroporto = self.situation_aeport[aeroporto_congonhas['class'][0]]
    #         retorno[aeroporto] = {'aeroporto': self.list_aeport[aeroporto]['local'],'status': situacao_aeroporto}

    #     for x in retorno:
    #         content += '<p> %s </p>' % retorno[x]['aeroporto']
    #         content += '<p> %s </p>' % retorno[x]['status']

    #     return content

    # @ram.cache(lambda *args: time() // (60 * 15))
    # def testeAeroportoVoo(self):
    #     soup = BeautifulSoup(self.getContent(url_direct.get('dash-aero')))
    #     content = ''
    #     for x in self.list_aeport:
    #         local = self.list_aeport[x]['local']
    #         situacao = soup.find('td', text=local)
    #         if situacao:
    #             voos = situacao.parent.findAll('span')
    #             content += '<p>cancelado: %s e atrasado %s</p>' % (voos[8].text,voos[0].text)
    #         else:
    #             content += '<p>Consulte situação</p>'
    #     return content

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
        return self.list_aeport.keys()
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
        return: Informações de Vôo dos aeroportos da cidade de São Paulo
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
        return: Informações do Transporte Público
        """
        status_metro_sp = self.getStatusMetro()
        status_trens_sp = self.getStatusMetro()
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
                              '<span id="t-metro">%s</span>' % status_metro_sp + \
                              '</li>' \
                              '<li>' \
                              '<div class="status"><i class="vermelho"></i></div>' \
                              '<div class="mini Mcptm"></div>' \
                              '<span id="t-cptm">%s</span>' % status_trens_sp + \
                              '</li>' \
                              '</ul>' \
                              '<a href="http://www.sptrans.com.br/itinerarios/" target="_blank" class="link-amarelo">Consultar itinerários</a>' \
                              '</div>'
        return transp_publica_html

    @ram.cache(lambda *args: time() // (60 * 15))
    def getStatusCptm(self):
        """
        return Informações CPTM da cidade de São Paulo
        """
        retorno = BeautifulSoup(self.getContent(url_direct.get('transp-cptm')))
        transp_metro = retorno.findAll('span', {'class': 'nome_linha'})
        linhas_cptm = []
        linhas_com_problemas = {}
        for x in transp_metro:
            linhas_cptm.append(x.string.lower())

        content = ''
        for key, x in enumerate(linhas_cptm):
            for div in retorno.find_all(class_=x):
                contador = 0
                for childdiv in div.find_all('span'):
                    if contador % 2:
                        if childdiv.string.lower().find('normal') == int(-1):
                            linhas_com_problemas[key] = {'situacao': childdiv.string, 'linha': x}
                    contador = contador + 1

        content = ''
        if len(linhas_com_problemas) > 0:
            for x in linhas_com_problemas.values():
                content += '<p>Linha:%s - Status: %s' % (x['linha'], x['situacao'])
        else:
            content += 'Circulação normal'
        return content

    @ram.cache(lambda *args: time() // (60 * 15))
    def getStatusMetro(self):
        """
        return Informações Metro da cidade de São Paulo
        """
        retorno = BeautifulSoup(self.getContent(url_direct.get('transp-metro')))
        transp_metro = retorno.find('ul', {'id': 'statusLinhaMetro'}).findAll('div')

        linhas_com_problemas = {}
        nome_da_linha = ''
        for key, value in enumerate(transp_metro):
            if key % 2:
                situacao = value.find('span').string
                situacao = situacao.lower()
                situacao_linha = situacao.strip(' \t\n\r')
                if situacao.find('normal') == int(-1):
                    linhas_com_problemas[key] = {'situacao': situacao_linha, 'linha': nome_da_linha}
            else:
                nome_da_linha = value.find('span').string
        content = ''
        if len(linhas_com_problemas) > 0:
            for x in linhas_com_problemas.values():
                content += '<p>Linha:%s - Status: %s' % (x['linha'], x['situacao'])
        else:
            content += 'Circulação normal'

        return content

    """
    ##########################################################################
                    Transito Zonas da cidade de São Paulo
    ##########################################################################
    """
    # @ram.cache(lambda *args: time() // (60 * 15))
    # def getTransito(self):
    #     """
    #     return: Trânsito em São Paulo agrupado por zonas da cidade
    #     """
    #     self.soup = BeautifulSoup(self.getContent(url_direct.get('transito-agora')))
    #     lista_zonas_sp = ('OesteLentidao', 'NorteLentidao',
    #                       'LesteLentidao', 'SulLentidao', 'lentidao')
    #     km_lentidao = []
    #     for zonas_sp in lista_zonas_sp:
    #         km_lentidao.append(self.soup.find('div', {"id": zonas_sp}).string)

    #     transito_html = '<div id="call-trans" class="dash" style="display: block;">' \
    #                     '<h3>Trânsito</h3>' \
    #                     '<button class="fechar-dash">X</button><div class="tran-total">' \
    #                     '<div class="ttotal"><span class="amarelo em14 bold"> %s </span>' % str(km_lentidao[4]) + ' km' + \
    #                     '<br><small class="bold em09">de lentidão</small></div>' \
    #                     '<div class="ttotal amarelo"><br>' \
    #                     '<hr class="pont"><div id="sp-mapa"><ul id="lentidao">' \
    #                     '<li id="kmOeste" class="amarelo"> %s ' % km_lentidao[0] + '</li>' \
    #                     '<li id="kmNorte" class="amarelo"> %s ' % km_lentidao[1] + '</li>' \
    #                     '<li id="kmLeste" class="amarelo"> %s ' % km_lentidao[2] + '</li>' \
    #                     '<li id="kmSul"   class="amarelo"> %s ' % km_lentidao[3] + '</li>'   \
    #                     '</ul></div> <div class="bloco-linha">' \
    #                     '<a href="http://www.cetsp.com.br/transito-agora/mapa-de-fluidez.aspx" class="azul-pq" target="_blank">Mapa de fluidez</a>' \
    #                     '<a href="http://www.cetsp.com.br/transito-agora/transito-nas-principais-vias.aspx" target="_blank" class="azul-pq">Lentidão por corredor</a>' \
    #                     '</div></div>'
    #     transito_html = '%s - %s - %s - %s - %s' % (str(km_lentidao[4]),km_lentidao[0],km_lentidao[1],km_lentidao[2],km_lentidao[3])

    #     return transito_html

    """
    ##########################################################################
                            Rodizio e Área de restrição
    ##########################################################################
    """
    # @ram.cache(lambda *args: time() // (60 * 15))
    # def getRodizio(self):
    #     """
    #     return: Informações rodízio de automóveis da cidade de São Paulo
    #     """
    #     url_rodizio = url_direct.get('dash-rodizio')
    #     placas_final_url_return = urllib.urlopen(url_rodizio)
    #     data_result = json.loads(placas_final_url_return.read())
    #     placa = data_result['Rotation']['desc']
    #     placa_horario_inicio = self.getPlacaHorarioInicio()
    #     placa_horario_final = self.getPlacaHorarioFinal()

    #     rodizio_html = '<div id="call-rodizio" class="dash" style="display: block;">' \
    #                    '<h3>Rodízio</h3> ' \
    #                    '<button class="fechar-dash">X</button>' \
    #                    '<div id="mapa-rodizio"></div><ul class="rod-3col"><li>' \
    #                    '<span class="em08 bold">Placas final:</span><br>' \
    #                    '<span class="amarelo em15">%s</span></li><li>' % placa + \
    #                    '<span class="em08 bold">Horário:</span><br>' \
    #                    '<small class="amarelo em1">%s</small><br>' % placa_horario_inicio + \
    #                    '<small class="amarelo em1">%s</small></li>' % placa_horario_final + \
    #                    '<li><span class="em08 bold">Penalidade:</span><br>' \
    #                    '<small class="amarelo em10">R$85,13</small>' \
    #                    '<small class="amarelo em08"> e 4pts na carteira</small></li></ul></div>'

    #     rodizio_html = ' %s - %s - %s ' % (placa,placa_horario_inicio,placa_horario_final)

    #     return rodizio_html

    @ram.cache(lambda *args: time() // (60 * 15))
    def getRestricaoPlacaFinal(self):
        """
        return: Restrição placa final
        """
        import ast
        restricao_placa_final = ast.literal_eval(self.soup.text).get('Rotation').get('desc')
        return restricao_placa_final

    @ram.cache(lambda *args: time() // (60 * 15))
    def getPlacaHorarioInicio(self):
        """
        return: Horário Início rodizio da cidade de São Paulo
        """
        placa_horario_inicio = '7h às 10h'
        return placa_horario_inicio

    @ram.cache(lambda *args: time() // (60 * 15))
    def getPlacaHorarioFinal(self):
        """
        return: Horário Fim rodizio da cidade de São Paulo
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
            status = ''
            for i in statuses:
                status += '<a href="https://twitter.com/' + screen_name + '/statuses/' + str(i.id) + '" target="_blank">' + str(i.text) + '<time>' + str(i.relative_created_at) + '</time></a>'
                ocorrencias.append(status)
            return ocorrencias
        except:
            return False
