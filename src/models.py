from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    # def __repr__(self):
    #     return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

Base = declarative_base()

tabla_pivote1 = Table('personaje_favorito', db.Model.metadata,
    Column('usuario_id', ForeignKey('usuario.id'), primary_key=True),
    Column('personaje_id', ForeignKey('personaje.id'), primary_key=True))

tabla_pivote2 = Table('planeta_favorito', db.Model.metadata,
    Column('usuario_id', ForeignKey('usuario.id')),
    Column('planeta_id' , ForeignKey('planeta.id')))

class Usuario(db.Model):
    __tablename__ = 'usuario'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    contrasena = Column(String(100), nullable=False)
    personajes = relationship('Personaje', secondary=tabla_pivote1)
    planetas = relationship('Planeta' , secondary=tabla_pivote2)
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class Personaje(db.Model):
    __tablename__ = 'personaje'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    birth_year = Column(String(100), nullable=True)
    eye_color = Column(String(100), nullable=True)
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eyeColor": self.eye_color,
            # do not serialize the password, its a security breach
        }        

class Planeta(db.Model):
    __tablename__ = 'planeta'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name_planeta = Column(String(250), nullable=False)
    gravity = Column(String(100), nullable=True)
    climate = Column(String(100), nullable=True)
    def serialize(self):
        return {
            "id": self.id,
            "name_planeta": self.name_planeta,
            "gravity": self.gravity,
            "climate": self.climate,
            # do not serialize the password, its a security breach
        }
  

#     def to_dict(self):
#         return {}

## Draw from SQLAlchemy base
# render_er(Base, 'diagram.png')
