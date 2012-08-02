# -*- coding: utf-8 -*-

class DBModel:

    def __init__(self):
        pass


    def auth_user(self):
        auth.define_tables(username=False)

    def categoria(self):
        db.define_table('categoria',
                        Field('title', label = T('Nombre')),
                        Field('slug', compute = lambda r:IS_SLUG.urlify(r['title'])),
                        Field('description', 'text', label = T('Descripción'),
                              comment=T('(opcional)')),
                        auth.signature,
                        format = '%(title)s',
                        )
        
        # requerimientos Tabla Categoría:
        db.categoria.title.requires = IS_NOT_IN_DB(db, 'categoria.title', 
                                                   error_message = \
                                                       'ya hay una categoría con ese título')
        db.categoria.is_active.writable = False
        db.categoria.is_active.readable = False
        pass

    def feeds(self):
        db.define_table('feed',
                        Field('title', label = T('Nombre del Feed'), 
                              comment = T('*requerido (sugerencia: "misitio.tld")')),
                        Field('categoria', 'reference categoria', 
                              comment = T('*requerido')),                     
                        Field('source', label = T('URL al Sitio'), 
                              comment = T('Ejemplo: http://www.sitio.tld')),
                        Field('link', requires = IS_URL(), label = T('URL feed'),
                              comment = T('*requerido')),
                        auth.signature,
                        format = '%(title)s',
                        )
        # requerimientos tabla Feed:
        db.feed.is_active.writable = False
        db.feed.is_active.readable = False
        db.feed.link.requires = IS_NOT_IN_DB(db, 'feed.link', error_message =\
                                                 T('Esta URL ya está en los registros'))
        db.feed.title.requires = IS_NOT_IN_DB(db, 'feed.title',  error_message =\
                                                  T('Ya hay otro feed con este título'))
        db.feed.categoria.requires = IS_IN_DB(db, 'categoria.id', '%(title)s', 
                                              error_message = \
                                                  T('Debe caregorizar el feed para que pueda ser mostrado.'))
        pass





if request.controller == "appadmin":
    M = DBModel()
    #M.auth_user()
    M.categoria()
    M.feeds()

