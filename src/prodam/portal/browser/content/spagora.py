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

    def showDetails(self):
        try:
            requested = self.request.form['id']
            text = ''
            if requested == "ex-clima":
                text = self.getWeatherSp()
            if requested == "ex-ar":
                text = self.getAirQuality()
            if requested == "ex-aero":
                text = self.getAirportFlights()
            if requested == "ex-publico":
                text = self.getMeansOfTransportation()
            if requested == "ex-transito":
                text = self.getTraffic()
            if requested == "ex-rodizio":
                text = self.getCarRotation()
        except:
            text = False
        return text

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
        response = None
        while True:
            try:
                handle = self._opener.open(req)
                if handle.info().get('Content-Encoding') == 'gzip':
                    data = handle.read()
                    buf = StringIO(data)
                    f = GzipFile(fileobj=buf)
                    response = f.read()
                else:
                    response = handle.read()
                break
            except HTTPError, e:
                retries = retries + 1
                print "%d Tentativas na url: %s, erro: %s" % (retries, url, e.getcode())
                if retries > self.max_retries:
                    break

        if response:
            return response
        else:
            return False

    """
    ##########################################################################
                           Página inicial - São Paulo Agora (capa)
    ##########################################################################
    """
    @ram.cache(lambda *args: time() // (60 * 15))
    def getCapa(self):
        content = ""

        try:
            self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima-media")))
            temp_media = self.getTempMedia()
            hour = localtime(time()).tm_hour
            self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima")))
            dia = self.soup.findAll('dia')
            potencial = dia[0].parent.find('ct', {'periodo': self.getPeriod(hour)})

            content += """
                       <li class="ex-clima ver-mais">
                       <div class="dash-border">
                       <strong class="titulo-dash">Tempo</strong>
                       <div class="tempo-g nb"></div>
                       <div class="t-media"><span>Média</span><span id="CGE-media" class="amarelo bold">%(temp_media)s°</span></div>
                       <div class="tempestade">
                       <span>Potencial <div class="raio"></div></span>
                       <span id="status-temp" class="amarelo">%(potencial)s</span>
                       </div>
                       </div>
                       <div class="ex-hover"><a href="#verMais"></a><div></div></div>
                       </li>
                       """ % {'temp_media': temp_media, 'potencial': str(potencial['pt'])}

        except:
            content += self.getContentExcept(class_li='ex-ar', text_div='Tempo')

        try:
            self.soup = BeautifulSoup(self.getContent(url_direct.get('qualidade-oxigenio')))
            qualidade_ar = self.getDescQualidade()

            content += """
                       <li class="ex-ar ver-mais">
                       <div class="dash-border">
                       <strong class="titulo-dash">Qualidade do Ar</strong>
                       <div class="dash-img o2quali"></div>
                       <b class="bullet-verde em2">%(qualidade_ar)s</b>
                       </div>
                       <div class="ex-hover"><a href="#verMais"></a><div></div></div>
                       </li>
                       """ % {'qualidade_ar': qualidade_ar}
        except:
            content += self.getContentExcept(class_li='ex-ar', text_div='Qualidade do Ar')

        content += """
                   <li class="ex-aero ver-mais">
                   <div class="dash-border">
                   <strong class="titulo-dash">Aeroportos</strong>
                   <div class="dash-img"></div>
                   <span id="aero-status">Consulte situação</span>
                   </div>
                   <div class="ex-hover"><a href="#verMais"></a><div></div></div>
                   </li>
                   """

        content += """
                   <li class="ex-publico ver-mais">
                   <div class="dash-border">
                   <strong class="titulo-dash">Transporte Público</strong>
                   <div class="dash-img"></div>
                   Busca de itinerários
                   </div>
                   <div class="ex-hover"><a href="#verMais"></a><div></div></div>
                   </li>
                   """
        try:
            self.soup = BeautifulSoup(self.getContent(url_direct.get('transito-agora')))

            total_km_lentidao = self.soup.find('div', {"id": 'lentidao'}).string

            if total_km_lentidao <= 45:
                status_transito_sp = 'livre'
            elif total_km_lentidao >= 45 and total_km_lentidao <= 90:
                status_transito_sp = 'moderado'
            elif total_km_lentidao > 90:
                status_transito_sp = 'ruim'

            content += """
                       <li class="ex-transito ver-mais">
                       <div class="dash-border">
                       <strong class="titulo-dash">Trânsito</strong>
                       <div class="dash-img semaforo"></div>
                       <div class="tran-total">
                       <div class="ttotal"><span class="amarelo em14 bold">%(total_km_lentidao)skm</span><br>
                       <small class="bold em09">de lentidão</small></div>
                       <span class="kmStatus verde"><i class="ball-status verde"></i>%(status_transito_sp)s</span>
                       </div></div>
                       <div class="ex-hover"><a href="#verMais"></a><div></div></div>
                       </li>
                       """ % {'total_km_lentidao': total_km_lentidao, 'status_transito_sp': status_transito_sp}
        except:
            content += self.getContentExcept(class_li='ex-transito', text_div='Trânsito')

        url_rodizio = url_direct.get('dash-rodizio')
        placas_final_url_return = urllib.urlopen(url_rodizio)
        data_result = json.loads(placas_final_url_return.read())
        placa = data_result['Rotation']['desc']

        content += """
                   <li class="ex-rodizio ver-mais">
                   <div class="dash-border">
                   <strong class="titulo-dash">Rodízio</strong>
                   <div class="dash-img"></div>
                   <ul class="rod-3col">
                   <li><span class="em08 bold"><small>Placas final:</small></span><br><span class="azul-pq em15">%(placa)s</span></li>
                   </ul></div>
                   <div class="ex-hover"><a href="#verMais"></a><div></div></div>
                   </li>
                   """ % {'placa': placa}

        return content

    """
    ##########################################################################
                           Helpers
    ##########################################################################
    """
    @ram.cache(lambda *args: time() // (60 * 15))
    def getTempMedia(self):
        """
        return temperature median in moment
        """
        temp_media = float(self.soup.media.text)
        temperature = str(int(round(temp_media)))
        return temperature

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
        content = """
                   <div id="call-publi" class="dash" style="display: block;">
                   %(text_div)s
                   <button class="fechar-dash">X</button>
                   <p class="sp-erro">Não foi possível carregar informações</p>
                   </div>
                   """ % {'text_div': text_div}
        return content

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

    @ram.cache(lambda *args: time() // (60 * 15))
    def getTempMaxima(self):
        """
        return time morning
        """
        self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima")))
        dia = self.soup.findAll('dia')
        temp_max = dia[0].parent.find('temp-max')
        return temp_max.string

    @ram.cache(lambda *args: time() // (60 * 15))
    def getTempMinima(self):
        """
        return temperature minimo
        """
        self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima")))
        dia = self.soup.findAll('dia')
        temp_min = dia[0].parent.find('temp-min')
        return temp_min.string

    @ram.cache(lambda *args: time() // (60 * 15))
    def getUmidadeArMax(self):
        """
        return unit ar max
        """
        self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima")))
        dia = self.soup.findAll('dia')
        umid_max = dia[0].parent.find('umid-max')
        return umid_max.string

    @ram.cache(lambda *args: time() // (60 * 15))
    def getUmidadeArMin(self):
        """
        return unit ar min
        """
        self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima")))
        dia = self.soup.findAll('dia')
        umid_min = dia[0].parent.find('umid-min')
        return umid_min.string

    @ram.cache(lambda *args: time() // (60 * 15))
    def getHoraNascerSol(self):
        """
        return hour sunrise
        """
        self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima")))
        dia = self.soup.findAll('dia')
        sunrise = dia[0].parent.find('sunrise')
        return sunrise.string

    @ram.cache(lambda *args: time() // (60 * 15))
    def getHoraPorSol(self):
        """
        return sunset time
        """
        self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima")))
        dia = self.soup.findAll('dia')
        sunset = dia[0].parent.find('sunset')
        return sunset.string

    """
    ##########################################################################
                           Qualidade do ar
    ##########################################################################
    """
    @ram.cache(lambda *args: time() // (60 * 15))
    def getAirQuality(self):
        try:
            qualidade_ar = self.getQualidadeAr()
            content = qualidade_ar
        except:
            content = self.getContentExcept(class_li='ex-ar', text_div='Qualidade do Ar')
        return content

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

    """
    ##########################################################################
                           Clima
    ##########################################################################
    """
    @ram.cache(lambda *args: time() // (60 * 15))
    def getWeatherSp(self):
        try:
            self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima-media")))
            temp_media = self.getTempMedia()

            self.soup = BeautifulSoup(self.getContent(url_direct.get("ex-clima")))
            dia = self.soup.findAll('dia')

            prev_manha = dia[0].parent.find('ct', {'periodo': 'Manhã'})
            prev_tarde = dia[0].parent.find('ct', {'periodo': 'Tarde'})
            prev_noite = dia[0].parent.find('ct', {'periodo': 'Noite'})
            prev_madrugada = dia[0].parent.find('ct', {'periodo': 'Madrugada'})
            umidade_ar_max = self.getUmidadeArMax()
            umidade_ar_min = self.getUmidadeArMin()
            hora_nascer_sol = self.getHoraNascerSol()
            hora_por_sol = self.getHoraPorSol()
            temp_maxima = self.getTempMaxima()
            temp_minima = self.getTempMinima()
            content = """
                      <div id="call-clima" class="dash" style="display: block;">
                      <h3>Tempo <em class="fonte">Fonte: CGE</em></h3>
                      <button class="fechar-dash">X</button>
                      <div id="temp-bloco">
                      <div id="t-agora" class="tempo-g nb"></div>
                      <div id="t-media"><small class="em08">Temperatura Media</small><br><span id="temp-media" class="amarelo em18">%(media)s°</span></div>
                      <div id="minXmax">
                      <div id="new-max"><span class="tmax"></span>%(max)s</div>
                      <div id="new-min"><span class="tmin"></span>%(min)s</div>
                      </div>
                      </div>
                      <ul id="dia-todo">
                      <li>
                      <strong class="azul-pq em08">Manha</strong>
                      <div class="tempo-p pn-pq"></div>
                      <div class="raio"></div>
                      <span class="em07 bold amarelo">%(manha)s</span>
                      </li>
                      <li>
                      <strong class="azul-pq em08">Tarde</strong>
                      <div class="tempo-p pi-pq"></div>
                      <div class="raio"></div>
                      <span class="em07 bold amarelo">%(tarde)s</span>
                      </li>
                      <li>
                      <strong class="azul-pq em08">Noite</strong>
                      <div class="tempo-p pi-pq-noite"></div>
                      <div class="raio"></div>
                      <span class="em07 bold amarelo">%(noite)s</span>
                      </li>
                      <li>
                      <strong class="azul-pq em08">Madrugada</strong>
                      <div class="tempo-p nb-pq-noite"></div>
                      <div class="raio"></div>
                      <span class="em07 bold amarelo">%(madrugada)s</span>
                      </li>
                      </ul>
                      <div id="tempor-outras">
                      <div class="a-40 bold">
                      <small class="em07"><span id="div" class="gotas"></span>Umidade relativa do ar</small>
                      <div class="a-half em13"><span class="tmax"></span> %(umax)s</div>
                      <div class="a-half em13"><span class="tmin"></span> %(umin)s</div>
                      </div>
                      <div class="sol-box">
                      <div id="sol"></div>
                      <div class="a-half"><small class="amarelo em14">%(hrin)s</small> <small class="em07">Nascer do sol</small></div>
                      <div class="a-half"><small class="amarelo em14">%(hrmax)s</small> <small class="em07">Por do sol</small></div>
                      </div></div></div>
                      """ % {'media': temp_media, 'max': temp_maxima[:-1], 'min': temp_minima[:-1], 'manha': prev_manha['pt'], 'tarde': prev_tarde['pt'], 'noite': prev_noite['pt'], 'madrugada': prev_madrugada['pt'], 'umax': umidade_ar_max, 'umin': umidade_ar_min, 'hrin': hora_nascer_sol[:-1], 'hrmax': hora_por_sol[:-1]}
        except:
            content = self.getContentExcept(class_li='ex-clima', text_div='Tempo')
        return content

    """
    ##########################################################################
                           Situação dos Aeroportos
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
    def getAirportFlights(self):
        try:
            soup = BeautifulSoup(self.getContent(url_direct.get('dash-aero-situacao')))
            retorno = {}
            for aeroporto in self.list_aeport:
                aeroporto_congonhas = soup.find(id=aeroporto)
                situacao_aeroporto = self.situation_aeport[aeroporto_congonhas['class'][0]]
                retorno[aeroporto] = {'aeroporto': self.list_aeport[aeroporto]['local'], 'status': situacao_aeroporto}

            content = """
                      <div id="call-aero" class="dash" style="display: block;">
                      <h3>Aeroportos <em class="em08 fonte">Fonte: Infraero e GRU</em></h3>
                      <button class="fechar-dash">X</button>
                      <ul id="aero-lista">
                      """
            print self.AeroportoVooSatus()
            html = ""
            for aeroport in retorno:
                if 'sbsp' == str(aeroport):
                    content += """
                               <li class="%(class)s"><strong class="aeronome">%(aeroporto)s</strong><small>
                               <span class="verde"><b class="ball-status verde"></b>%(status)s</span></li>
                               <br>
                               <span class="txt-right">Vôos atrasados:</span>
                               <span class="txt-left azul-pq">7</span></small>
                               <small><span class="txt-right">Vôos cancelados:</span>
                               <span class="txt-left azul-pq">2</span></small></li>
                               """ % {'aeroporto': retorno[aeroport]['aeroporto'], 'status': retorno[aeroport]['status'], 'html': html, 'class': aeroport['codigo'].lower()}
                else:
                    content += """
                               <li class="%(class)s"><strong class="aeronome">%(aeroporto)s</strong><small>
                               <span class="verde"><b class="ball-status verde"></b>%(status)s</span></li>
                               """ % {'aeroporto': retorno[aeroport]['aeroporto'], 'status': retorno[aeroport]['status'], 'html': html, 'class': aeroport['codigo'].lower()}

            content += "</ul></div>"
        except:
            content = self.getContentExcept(class_li='ex-aeroportos', text_div='Aeroportos')
        return content

    @ram.cache(lambda *args: time() // (60 * 15))
    def AeroportoVooSatus(self):
        soup = BeautifulSoup(self.getContent(url_direct.get('dash-aero')))
        content = ''
        situacao = soup.find('td', text='Sao Paulo - Congonhas-SP')
        if situacao:
            voos = situacao.parent.findAll('span')
            content += '<p>cancelado: %s e atrasado %s</p>' % (voos[8].text, voos[0].text)
        else:
            content += '<p>Consulte situação</p>'
        return content

    """
    ##########################################################################
                           Rodizio SP
    ##########################################################################
    """
    @ram.cache(lambda *args: time() // (60 * 15))
    def getCarRotation(self):
        try:
            url_rodizio = url_direct.get('dash-rodizio')
            placas_final_url_return = urllib.urlopen(url_rodizio)
            data_result = json.loads(placas_final_url_return.read())
            placa = data_result['Rotation']['desc']
            content = """
                      <div id="call-rodizio" class="dash" style="display: block;">
                      <h3>Rodízio</h3>
                      <button class="fechar-dash">X</button>
                      <div id="mapa-rodizio"></div>
                      <ul class="rod-3col">
                      <li><span class="em08 bold">Placas final:</span><br><span class="amarelo em15">%(placa)s</span></li>
                      <li><span class="em08 bold">Horário:</span><br><small class="amarelo em1">7h às 10h</small><br><small class="amarelo em1">17h às 20h</small></li>
                      <li><span class="em08 bold">Penalidade:</span><br><small class="amarelo em10">R$85,13</small><small class="amarelo em08"> e 4pts na carteira</small></li>
                      </ul>
                      </div>
                      """ % {'placa': placa}
        except:
            content = self.getContentExcept(class_li='ex-rodizio', text_div='Rodízio')
        return content

    """
    ##########################################################################
                           Trânsito SP
    ##########################################################################
    """
    @ram.cache(lambda *args: time() // (60 * 15))
    def getTraffic(self):
        try:
            self.soup = BeautifulSoup(self.getContent(url_direct.get('transito-agora')))
            lista_zonas_sp = ('OesteLentidao', 'NorteLentidao',
                              'LesteLentidao', 'SulLentidao', 'lentidao')
            km_lentidao = []
            for zonas_sp in lista_zonas_sp:
                km_lentidao.append(self.soup.find('div', {"id": zonas_sp}).string)

            content = """
                      <div id="call-trans" class="dash" style="display: block;">
                      <h3>Trânsito</h3>
                      <button class="fechar-dash">X</button>
                      <div class="tran-total">
                      <div class="ttotal"><span class="amarelo em14 bold">%(lentidao)s km</span><br><small class="bold em09">de lentidão</small></div>
                      <div class="ttotal amarelo"><br><span class="amarelo bolinha"></span>regular</div>
                      </div>
                      <hr class="pont">
                      <div id="sp-mapa">
                      <ul id="lentidao">
                      <li id="kmOeste" class="amarelo">%(oeste)s</li>
                      <li id="kmNorte" class="amarelo">%(norte)s</li>
                      <li id="kmLeste" class="amarelo">%(leste)s</li>
                      <li id="kmSul" class="amarelo">%(sul)s</li>
                      </ul>
                      </div>
                      <div class="bloco-linha"><a href="http://www.cetsp.com.br/transito-agora/mapa-de-fluidez.aspx" class="azul-pq" target="_blank">Mapa de fluidez</a> <a href="http://www.cetsp.com.br/transito-agora/transito-nas-principais-vias.aspx" target="_blank" class="azul-pq">Lentidão por corredor</a></div></div>
                      """ % {'oeste': km_lentidao[0][:5], 'norte': km_lentidao[1][:5], 'leste': km_lentidao[2][:5], 'sul': km_lentidao[3][:5], 'lentidao': km_lentidao[4]}
        except:
            content = self.getContentExcept(class_li='ex-transito', text_div='Transito')
        return content

    """
    ##########################################################################
                           Transporte Público
    ##########################################################################
    """
    @ram.cache(lambda *args: time() // (60 * 15))
    def getMeansOfTransportation(self):
        try:
            status_metro_sp = self.getStatusMetro()
            status_trens_sp = self.getStatusCptm()
            content = """
                      <div id="call-publi" class="dash" style="display: block;">
                      <h3>Transporte Público</h3> <button class="fechar-dash">X</button>
                      <ul>
                      <li>
                      <div class="status"><i class="verde"></i></div>
                      <div class="mini Mbus"></div>
                      <span id="spT-twitter">Não saia de casa sem antes consultar qual o melhor trajetos.
                      Acesse: <a href="http://www.sptrans.co" target="_blank">Mais</a></span>
                      </li>
                      <li>
                      <div class="status"><i class="amarelo"></i></div>
                      <div class="mini Mmetro"></div>
                      <span id="t-metro">%(metro)s</span>
                      </li>
                      <li>
                      <div class="status"><i class="vermelho"></i></div>
                      <div class="mini Mcptm"></div>
                      <span id="t-cptm">%(trem)s</span>
                      </li>
                      </ul>
                      <a href="http://www.sptrans.com.br/itinerarios/" target="_blank" class="link-amarelo">Consultar itinerários</a>
                      </div>
                       """ % {'metro': status_metro_sp, 'trem': status_trens_sp}
        except:
            content = self.getContentExcept(class_li='ex-transito', text_div='Transito')
        return content

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
                content += '<p>Linha: %s - %s </p>' % (x['linha'], x['situacao'])
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
                content += '<p>Linha:%s - Status: %s </p>' % (x['linha'], x['situacao'])
        else:
            content += 'Circulação normal'

        return content

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
