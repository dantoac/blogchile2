# -*- coding: utf-8 -*-

#T.force('es-es')
#import locale
#locale.setlocale(locale.LC_ALL, 'es_CL.UTF8')

def index():
    M = DBModel()
    M.feeds()

    pub = UL(_class = 'thumbnails')
    
    if request.args:
        cat_id = db(db.categoria.slug == request.args(0)).select(db.categoria.id)[0] or 1
    else:
        cat_id = 1

    data = db((db.feed.categoria == cat_id) &
              (db.feed.is_active == True)
              ).select(
        db.feed.title,
        db.feed.link
        )


    pub.append(cache.disk(str(request.args(0)), 
                         lambda: get_feeds(data),
                         time_expire = 300)
               )

    return dict(feeds=pub)

def get_feeds(data):
    #session.forget()
    import gluon.contrib.feedparser as feedparser
    pub = CAT()
    for f in data:
        try:
            #d = cache.ram(str('asdf'), lambda: feedparser.parse(f.link), time_expire=60)
            d = feedparser.parse(f.link)
            entradas = [
                DIV(A(entry.title[:50]+'...', _href=entry.link, 
					_class = "noticia_link"),' ',
                    DIV(prettydate(guess_updated(entry.updated)) or entry.updated,
                        _class = "noticia_meta"),
                    _class = "noticia_contenido") for entry in d.entries[:3]]

            pub.append(LI(DIV(
                        H5(A(str(f.title).capitalize(), 
                             _href=f.link, _style = "white-space:normal !important;"
                               )), CAT(entradas),_class="thumbnail well"),
                          _class = "span2"
                          ))

        except Exception as e:
            pub.append(SPAN("!", _class="badge"))
    return pub

def guess_updated(date):
    """
	Traduce parámetro fecha a formato ISO estándar o 
	retorna la fecha original si no pudiere.
    """
    from datetime import datetime
    
    try:
		#traduce desde 2012-07-22 22:12:32
        updated = datetime.strptime(
                str(date),'%Y-%m-%d %H:%M:%S')
    except:
        try:
			#traduce desde Dom, 22 Julio 2012 22:12:32
            updated = datetime.strptime(
                    str(date[:25]),'%a, %d %b %Y %H:%M:%S')
        except:
			try:
				#traduce desde 22 Julio 2012 22:12:32
				updated = datetime.strptime(str(date[:-4]),
					'%d %b %Y %H:%M:%S')
			except:
				#fallback al formato original
				updated = date #"(último publicado)"
 
    return updated
