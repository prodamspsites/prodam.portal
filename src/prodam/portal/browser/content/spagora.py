# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from bs4 import BeautifulSoup
from urllib2 import urlopen

url_direct = {'pref-sp': 'http://www.capital.sp.gov.br/portal/',
              'ex-publico': "http://www.cptm.sp.gov.br/Pages/Home.aspx",
              'ex-publico': "http://www.metro.sp.gov.br/Sistemas/direto-do-metro-via4/diretodoMetroHome.aspx",
              'ex-ar': "http://sistemasinter.cetesb.sp.gov.br/Ar/php/ar_resumo_hora.php",
              'dash-aero': "http://voos.infraero.gov.br/hstvoos/RelatorioPortal.aspx",
              'ex-clima': "http://www.cgesp.org/v3/previsao_prefeitura_xml.jsp",
              'ex-publico': "http://cetsp1.cetsp.com.br/monitransmapa/agora/",
              'dash-rodisio': "http://misc.prefeitura.sp.gov.br/pmspws/rotation/data.json",
              'dash-aero-situacao': "http://www.infraero.gov.br/situacaoaeroporto/",
              'ex-clima-media': "http://www.saisp.br/cgesp/temp_media_prefeitura_sp.jsp"}


def getContent(url=None):
    """
    return: content redirect to service
    """
    content = urlopen(url).read()
    return BeautifulSoup(content)


class FindTemperature(object):
    """
    return temperature media
    """
    soup = None

    def __init__(self):
        """
        :return: initialize find climate in ex-clima
        """
        self.soup = getContent(url_direct.get("ex-clima-media"))

    def getTempMedia(self):
        """
        return time median
        """
        temp_media = float(self.soup.media.text)
        temp = str(int(round(temp_media)))
        return temp


class FindClimate(object):
    """
    find climate and roles sites
    """
    prevision = {'NB': 'Nubrado',
                 'EN': 'Encoberto',
                 'PI': 'Pancadas Isoladas',
                 'PC': 'Pancadas Chuvas'}
    soup = None

    def __init__(self):
        """
        :return: initialize find climate in ex-clima
        """
        self.soup = getContent(url_direct.get("ex-clima"))

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

    def getWeather(self, type):
        """
        :return: weather condicion in day
        """
        return self.soup.dia.findAll(type)[0].text

    def getTempMaxima(self):
        """
        return time morning
        """
        temp_max = str(self.getWeather('temp-max')[:-2])
        return temp_max

    def getTempMinima(self):
        """
        return temperature minimo
        """
        temp_min = str(self.getWeather('temp-min')[:-2])
        return temp_min

    def getPrevManha(self):
        """
        return prevision time morning
        """
        return self.getPrevision('Manhã')

    def getPrevTarde(self):
        """
        return time afternoon
        """
        return self.getPrevision('Tarde')

    def getPrevNoite(self):
        """
        return time night
        """
        return self.getPrevision('Noite')

    def getPrevMadrugada(self):
        """
        return time dawn
        """
        return self.getPrevision('Madrugada')

    def getUmidadeArMax(self):
        """
        return unit ar max
        """
        return str(self.getWeather('umid-max')[:2]) + '%'

    def getUmidadeArMin(self):
        """
        return unit ar min
        """
        return str(self.getWeather('umid-min')[:2]) + '%'

    def getHoraNascerSol(self):
        """
        return hour sunrise
        """
        return str(self.getWeather('sunrise')[:-1])

    def getHoraPorSol(self):
        """
        return sunset time
        """
        return str(self.getWeather('sunset')[:-1])


class FindQualityAr(object):
    """
    find quality ar in and roles sites
    """
    soup = None

    def __init__(self):
        """
        initialize quality ar
        """
        self.soup = getContent(url_direct.get("ex-ar"))


class FindAeportSituationVoo(object):
    """
    find conditional aeport and roles sites
    """
    soup = None

    def __init__(self):
        """
        initialize conditional
        """
        self.soup = getContent(url_direct.get("dash-aero"))


class FindAeportSituation(object):
    """
    find conditional aeport and roles sites
    """
    soup = None
    list_aeport = {'sbsp': 'CGH - Congonhas',
                   'sbgr': 'GRU - Guarulhos',
                   'sbmt': 'MAE - Cpo. de Marte',
                   'sbkp': 'VCP - Viracopos'}

    def __init__(self):
        """
        initialize conditional
        """
        self.soup = getContent(url_direct.get("dash-aero-situacao"))

    def getSituation(self):
        """
        return situation retrict conditional aeport
        """
        list_situation = []
        for aeport in self.list_aeport.keys():
            list_situation.append({'aeport': self.list_aeport.get(aeport),
                                   'situation': self.soup.findAll('li', {'id': aeport})})

        return list_situation


class SpAgora(BrowserView):

    def __init__(self):
        pass

    def getClima(self):
        """
        return: content clima and details

        """
        temp_media = FindTemperature().getTempMedia()
        clima = FindClimate()
        temp_maxima = clima.getTempMaxima()
        temp_minima = clima.getTempMinima()
        prev_manha = clima.getPrevManha()
        prev_tarde = clima.getPrevTarde()
        prev_noite = clima.getPrevNoite()
        prev_madrugada = clima.getPrevMadrugada()
        umidade_ar_max = clima.getUmidadeArMax()
        umidade_ar_min = clima.getUmidadeArMin()
        hora_nascer_sol = clima.getHoraNascerSol()
        hora_por_sol = clima.getHoraPorSol()

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

    def getQualidadeAr(self):
        """
        return: content qualidade do ar
        """
        # import ipdb; ipdb.set_trace()
        # quality_ar = FindQualityAr()
        quality_ar_html = None
        # quality_ar_html =   '<div id="call-ar" class="dash" style="display: block;">' \
        #                         '<h3>' \
        #                             'Qualidade do Ar ' \
        #                             '<em class="fonte">Fonte: CETESB</em>' \
        #                         '</h3> ' \
        #                         '<button class="fechar-dash">X</button>' \
        #                         '<div class="O2"></div>' \
        #                         '<div id="o2mapa">' \
        #                             '<div class="kineticjs-content" role="presentation" style="position: relative; display: inline-block; width: 300px; height: 160px;">' \
        #                                 '<canvas width="300" height="160" style="padding: 0px; margin: 0px; border: 0px; position: absolute; top: 0px; left: 0px; ' \
        #                                 'width: 300px; height: 160px; background: transparent;"></canvas>' \
        #                             '</div>' \
        #                         '</div>' \
        #                         '<ol id="dica">' \
        #                             '<li>' \
        #                                 '<i></i> ' \
        #                                     'Pessoas com doenças respiratórias podem apresentar sintomas como tosse seca e cansaço' \
        #                             '</li>' \
        #                             '<li>' \
        #                                 '<i></i>' \
        #                                     'Pessoas com doenças cardíacas ou pulmonares, procurem reduzir esforço pesado ao ar livre.' \
        #                             '</li>' \
        #                             '<li>' \
        #                                 '<i></i>' \
        #                                     'Reduzir o esforço físico pesado ao ar livre, principalmente pessoas com doenças cardíacas ou pulmonares, idosos e crianças.' \
        #                                 '</li>' \
        #                             '<li>' \
        #                                 '<i></i>' \
        #                                     'População em geral pode apresentar sintomas como ardor nos olhos, nariz e garganta, tosse seca e cansaço.' \
        #                             '</li>' \
        #                         '</ol>' \
        #                     '</div>'
        return quality_ar_html

    def getAereo(self):
        """
        return: content aeroporto
        """
        # situation = FindAeportSituation()
        # situation_voo = FindAeportSituationVoo()
        aeport_html = '<div id="call-aero" class="dash" style="display: block;">' \
                      '<h3>' \
                      'Aeroportos '\
                      '<em class="em08 fonte">Fonte: Infraero e GRU</em>' \
                      '</h3>' \
                      '<button class="fechar-dash">X</button>' \
                      '<ul id="aero-lista"><li class="cgh">' \
                      '<strong class="aeronome">'\
                      '<abbr>CGH</abbr> - Congonhas</strong>' \
                      '<small><span class="undefined"><b class="ball-status undefined">' \
                      '</b>Aberto</span><br><span class="txt-right">Vôos atrasados:</span>   <span class="txt-left azul-pq">0</span></small><small><span class="txt-right">Vôos cancelados:</span> <span class="txt-left azul-pq">2</span></small></li><li class="gru"><strong class="aeronome"><abbr>GRU</abbr> - Guarulhos</strong><small><span class="verde"><b class="ball-status verde"></b>Aberto</span><br><a href="http://www.gru.com.br/pt-br" class="link-aero" target="_blank">Clique e consulte</a> </small></li><li class="mae"><small><strong class="aeronome"><abbr>MAE</abbr> - Cpo. de Marte</strong><small><span class="undefined"><b class="ball-status undefined"></b>Aberto</span><br><a href="http://www.infraero.gov.br/index.php/aeroportos/sao-paulo/aeroporto-campo-de-marte.html" class="link-aero" target="_blank">Clique e consulte</a></small></small></li><li class="vcp"><small><small><strong class="aeronome"><abbr>VCP</abbr>- Viracopos</strong><small><span class="verde"><b class="ball-status verde"></b>Aberto</span><br><a href="http://www.viracopos.com/passageiros/voos/" class="link-aero" target="_blank">Clique e consulte</a></small></small></small></li></ul></div>'
        return aeport_html

    def getTransportePublico(self):
        """
        return content transporte puclico
        """
        _publico = self.getContent("ex-publico")
        return _publico

    def getTransito(self):
        """
        return: content transtito
        """
        _transito = self.getContent("ex-transito")
        return _transito

    def getRodisio(self):
        """
        return: content rodozio
        """
        _rodizio = self.getContent("ex-rodizio")
        return _rodizio
