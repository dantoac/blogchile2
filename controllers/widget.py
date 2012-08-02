# -*- coding: utf-8 -*-

def hora():
    session.forget()
    from datetime import datetime
    ahora = datetime.strftime(request.now.now(), '%d %b %Y %H:%M')
    hora = CAT('Última Actualización: ',SPAN(ahora, _class = 'label label-success'))
    return hora


#@cache(request.env.path_info, time_expire=7200, cache_model=cache.disk)
def indicadoreseconomicos():
    #if not request.ajax: return ''
    session.forget()
    #if request.ajax:
    import urllib2
    import locale


    locale.setlocale(locale.LC_ALL, 'es_CL.UTF8')

    import re
    locale.setlocale(locale.LC_ALL, 'es_CL.UTF8')
    #uri = 'http://www.averigualo.cl/feed/indicadores.xml'
    uri = 'http://indicador.eof.cl/xml'

    try:
        #pag = urllib2.urlopen(uri).read()
        pag = cache.disk(str(request.now.date()),lambda: urllib2.urlopen(uri).read(), time_expire=28800)

        pag = pag.decode('iso8859-1').encode('utf-8')

        html = TAG(pag)
        try:

            eurocalculado = locale.atof(html.element('indicador',_nombre='Euro')[0])
        except Exception,e:
            eurocalculado = '-'

        try:
            #dolarcalculado = locale.atof(html.element('indicador',_nombre='Dólar Observado')[0])
            dolarcalculado = locale.atof(html.element('indicador',_nombre=re.compile('Observado'))[0])
        except Exception,e:
            dolarcalculado = '-'


        try:
            #utmcalculado = locale.atof(html.element('utm')[0])
            utmcalculado = html.element('indicador',_nombre='UTM (Agosto)')[0]
        except Exception,e:
            utmcalculado = '-'


        try:
            #ufcalculado = locale.atof(html.element('uf')[0])
            ufcalculado = html.element('indicador',_nombre='UF')[0]
        except Exception,e:
            ufcalculado = '-'

        html_indicadores = TABLE(THEAD(TR(TH('Dólar'),TH('Euro'),TH('UF'),TH('UTM'))))
        html_indicadores.append(TR(TD('%s' % str(dolarcalculado)[:6]),
                                   TD('%s' % str(eurocalculado)[:6]),
                                   TD('%s' % str(ufcalculado)[:8]),
                                   TD('%s' % str(utmcalculado))
                                   )
                                )


        #html_indicadores = XML(html_indicadores)

    except Exception,e:
        html_indicadores = DIV('error: No pude obtener los indicadores económicos. %s' % e, _class='error')
    return dict(indicadores=html_indicadores)
    #else:
    #    return dict(indicadores='X_x')


def obtienedatos(urllugar,ubicacion):
    #if not request.ajax: return ''
    session.forget()
    import urllib2
    import time
    import datetime
    import urllib 

    ubicacion = ubicacion.capitalize()

    #import unicodedata as ud

    

    #url = urllib.urlencode(urllugar)

    
    url = urllib.quote_plus(urllugar,safe='?&/=:')
    #response.flash = url
    resp = urllib2.urlopen(str(XML(url)))

    xmlstr = resp.read()
    #xmlstr = xmlstr.decode('utf-8','ignore')

    # eliminando el xml que no podemos parsear
    xmlstr = xmlstr.replace('<![CDATA[','')
    xmlstr = xmlstr.replace(']]>','')

    # web2pyando el xml :D
    html = TAG(xmlstr)

    # obteniendo los datos para hoy
    ahora_temp = XML(html.element('temp_c')[0])
    ahora_icono = html.element('weathericonurl')[0]
    lugar = html.element('query')[0]
    ahora_velocidad_viento = html.element('windspeedkmph')[0]
    ahora_humedad = html.element('humidity')[0]
    ahora_tempMax = html.element('tempmaxc')[0] 
    ahora_tempMin = html.element('tempminc')[0]
    ahora_fecha = html.element('date')[0]


    # empaquetando el bloque de los indicadores de temperatura en una variable
    temp_info = UL(LI('Actual: %s °C' % ahora_temp),LI('Máxima: %s °C ' % ahora_tempMax),LI('Mínima: %s °C' % ahora_tempMin),_class='temperaturas')

    # formando el mensaje completo
    infohoy = DIV(_id='ahora')
    infohoy.append(XML('%(lugar)s  %(icono)s  %(temp)s' % dict(
        temp=temp_info,
        lugar=H2(lugar,_class='lugar_nombre'),
        icono = IMG(_src=ahora_icono,_class='ahora_icono'),)
                       )
                   )

    
    # obteniendo el pronóstico
    #pronostico = TABLE(THEAD(TH('Próximos días:')), _id='proximosdias')
    pronostico = DIV(SPAN(ubicacion,_class='dia'),_class='pronostico')
    
    for t in html.elements('weather'):
        icono = IMG(_src=t.element('weathericonurl')[0],_class='icono')
        #lugar = t.element('query')[0]
        #velocidad_viento = t.element('windspeedkmph')[0]
        #humedad = t.element('humidity')[0]
        tempMax = t.element('tempmaxc')[0] 
        tempMin = t.element('tempminc')[0]
        fecha = t.element('date')[0]
        
        facs = time.strptime(fecha, '%Y-%m-%d')
        fecha_dt = datetime.date(facs[0],facs[1],facs[2])
        fecha_str = XML(fecha_dt.strftime('%A').capitalize()[:2])
        
        #pronostico.append(TR(TD('%s' % fecha_str),TD('Min.: %s°C' % tempMin),TD('Max.:%s°C' % tempMax),TD(XML('%s' % icono)),_class='pronostico_diario')) #dict(icono=icono,fecha=fecha_str,tempMax=tempMax,tempMin=tempMin)),_id=fecha,_class='pronostico_diario'))

        pronostico.append(SPAN(icono,B(fecha_str),': %(tempMin)s/%(tempMax)s°C ' % dict(tempMax=tempMax,tempMin=tempMin)))
                        

    

    #msg = DIV(infohoy,pronostico,_class='tiempo_local')
    msg = pronostico

    
    return msg

@cache(request.env.path_info, time_expire=28800, cache_model=cache.disk)
def pronosticotiempo():
    #if not request.ajax: return ''
    key = '9e6119ed3a211314113107'

    lugares = ['arica','iquique','antofagasta','copiapó','la serena','valparaíso','viña del mar','santiago','rancagua','talca','chillán','concepción','temuco','valdivia','puerto montt','coyhaique','punta arenas','robinson crusoe','hanga roa']

    lugares.sort()
       
    tiempo = CAT()
    for lugar in lugares:
        try:

            url = XML('http://free.worldweatheronline.com/feed/weather.ashx?q=%(lugar)s,chile&format=xml&num_of_days=5&key=%(key)s' % dict(key=key,lugar=lugar))
                      
            try:
                #tiempo += obtienedatos(url,lugar)
                tiempo.append(obtienedatos(url,lugar))
            except:
                tiempo = '<div class="error">droides trabajando, disculpe la molestia]</div>'
        except Exception,e:
            tiempo = DIV('%s' % e, _class='error')
    return dict(message=tiempo)

def identishare():
    #if not request.ajax: return ''
    session.forget()
    identishare =  XML('''
<div id="identishare" style="vertical-align: bottom;"></div>
<script type="text/javascript" src="http://www.tildehash.com/identishare.php" defer="defer"></script>
<noscript>
<iframe height="61" width="61" scrolling="no" frameborder="0" src="http://www.tildehash.com/identishare.php?noscript" border="0" marginheight="0" marginwidth="0" allowtransparency="true"></iframe>
</noscript>
''')

    return dict(identishare=identishare)

def dent():
    dent = XML('''
<div class="identica" style="background-color: white;border: 1px solid #ddd;display:inline;">
<a href="javascript:(function(){var%20d=document,w=window,e=w.getSelection,k=d.getSelection,x=d.selection,s=(e?e():(k)?k():(x?x.createRange().text:0)),f='http://identi.ca/index.php?action=bookmarklet',l=d.location,e=encodeURIComponent,g=f+'&status_textarea='+l.href;function%20a(){if(!w.open(g,'t','toolbar=0,resizable=0,scrollbars=1,status=1,width=320,height=200')){l.href=g;}}a();})()"><img src="http://www.nuxified.org/images/identica.png" /></a>
</div>
''')
    return dict(dent=dent)

def identica_badge():
    #if not request.ajax: return ''
    session.forget()
    badge = XML('''
<script type="text/javascript" src="http://identi.ca/js/identica-badge.js">
    {
       "user":"blogchile",
       "server":"identi.ca",
       "headerText":"@identica",
       "width" : "170px"
    }
    </script>
''')
    return dict(badge = badge)

def twitterfollow():
    #if not request.ajax: return ''
    session.forget()
    twitterfollow = XML('<a href="https://twitter.com/blogchile" class="twitter-follow-button" data-width="300px" data-lang="es" data-align="right">@blogchile</a><script src="http://platform.twitter.com/widgets.js" type="text/javascript"></script>')
    return dict(twitterfollow=twitterfollow)

def twittearesto():
    if not request.ajax: return ''
    session.forget()
    twittearesto = XML('<a href="http://twitter.com/share" class="twitter-share-button" data-count="horizontal" data-via="blogchile" data-lang="es">Tweetear esto</a><script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>')
    return dict(twittearesto=twittearesto)
