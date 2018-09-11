'''
CREACIÓN DE LA BASE DE DATOS DONDE SE ALMACENARÁN
LOS PROYECTOS REALIZADOS.
'''
from sqlalchemy import create_engine, schema, types
from sqlalchemy import MetaData, Column, Table, ForeignKey, UniqueConstraint

metadata = schema.MetaData()

tabla_proyectos = schema.Table('proyectos', metadata,
                               schema.Column('idProyecto', types.Integer,
                                             primary_key=True),
                               schema.Column('nombre', types.String(100)),
                               schema.Column('idSubred', types.String(100)),
                               schema.Column('etiqueta', types.String(100)),
                               schema.Column('ipSubred', types.String(100)),
                               schema.Column('hostSolicitados', types.String(100)),
                               schema.Column('hostDisponibles', types.String(100)),
                               schema.Column('bitsRed', types.String(100)),
                               schema.Column('mascara', types.String(100)),
                               schema.Column('primeraAsignable', types.String(100)),
                               schema.Column('ultimaAsignable', types.String(100)),
                               schema.Column('broadcast', types.String(100))
                               )

engine = create_engine('sqlite:///Proyectos.db', echo=False)
metadata.bind = engine

metadata.create_all(checkfirst=True)
