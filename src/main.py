"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Usuario, Personaje, Planeta, tabla_pivote1, tabla_pivote2
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/usuario', methods=['GET'])
def handle_usuario():
    obtenerUsuarios = Usuario.query.all()
    lista = []
    for user in obtenerUsuarios:
        lista.append(user.serialize())
    return jsonify(lista), 200    

    # print(request.method)   # obtener metodo: GET POST, DELETE, PATCH, PUT
    # print(request.get_json())   # obtener JSON enviado por cliente
    # lista = []
    # for usuario in usuarios:
    #     lista.append(usuario.serialize())

    # return jsonify(lista), 200
  

@app.route('/personajes', methods=['GET'])
def obtenerPersonajes():
    personajes = Personaje.query.all()
    listado = []   
    for pers in personajes:
        listado.append(pers.serialize())
    return jsonify(listado), 200

@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def obtenerPersonajes_id(personaje_id):
    
    # personaje = Personaje(name='yasna', birth_year="1988", eye_color='brown')
    # db.session.add(personaje)
    # db.session.commit()
    personajes = Personaje.query.filter_by(id=personaje_id)[0]
    print('_'*80)
    print(Personaje.query.filter_by(id=personaje_id)[0])
    print('_'*80)
    return jsonify(personajes.serialize()), 200   

@app.route('/planetas', methods=['GET'])
def obtenerPlanetas():
    planetas = Planeta.query.all()
    lista2 = []
    for planets in planetas:
        lista2.append(planets.serialize())
    return jsonify(lista2), 200   
    
@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def obtenerPlaneta_id(planeta_id):
    
    # personaje = Personaje(name='yasna', birth_year="1988", eye_color='brown')
    # db.session.add(personaje)
    # db.session.commit()
    planetas = Planeta.query.filter_by(id=planeta_id).first()
    return jsonify(planetas.serialize()), 200                 

@app.route('/usuario/favoritos/<int:usuario_id>', methods=['GET'])
def usuarioFavoritos(usuario_id):
    print('-'*80)
    # El siguiente código se hace porque no se tienen usuarios, entonces se crean a la mala, esta forma se usa para agregar registros en la base de datos, instanciando la clase, agregandola en la BD y luego guardándola en la base de datos: 
    # usuario = Usuario(name='Yas3',contrasena='ajdkslf')
    # db.session.add(usuario)
    # db.session.commit()
    # print(Usuario.query.filter_by(id=2).first().personaje)
    # print('UsuarioPersonajes:', Usuario.query.filter_by(id=2).first().personaje)
    usuarioPersonajes = Usuario.query.filter_by(id=usuario_id).first().personajes
    print(usuarioPersonajes)
    # usuario = Usuario.query.filter_by(id=2).first()
    # personaje_favorito = Personaje.query.filter_by(id=1).first()
    # usuario.personaje.append(personaje_favorito)
    # db.session.add(usuario)
    # db.session.commit()
  
    print('-'*80)
    # print('UsuarioPlanetas:', Usuario.query.filter_by(id=3).first().planeta)
    usuarioPlanetas = Usuario.query.filter_by(id=usuario_id).first().planetas
    # usuario = Usuario.query.filter_by(id=usuario_id).first()
    # planeta_favorito = Planeta.query.filter_by(id=2).first()
    # usuario.planeta.append(planeta_favorito)
    # db.session.add(usuario)
    # db.session.commit()

    print('-'*90)
    lista = []
    for personaje_favorito in usuarioPersonajes : 
        lista.append(personaje_favorito.serialize())
    for planeta_favorito in usuarioPlanetas :
        lista.append(planeta_favorito.serialize())    
    return jsonify(lista), 200

@app.route('/favoritos/planetas/<int:planeta_id>' , methods= ['POST'])
def favoritos_planetas_create(planeta_id):
    planeta = Planeta.query.get(planeta_id)
    usuario = Usuario.query.get(1)
    usuario.planetas.append(planeta)
    db.session.commit()
    return jsonify({"succses": "Ya se agregó su planeta favorito satisfactoriamente"}), 201

@app.route('/favoritos/personajes/<int:personaje_id>' , methods= ['POST'])    
def favoritos_personajes_create(personaje_id):
    personaje = Personaje.query.get(personaje_id)
    usuario = Usuario.query.get(1)
    usuario.personajes.append(personaje)
    db.session.commit()
    return jsonify({"succes": "Ya se agregó su personaje favorito satisfactoriamente"}), 201

@app.route('/favoritos/planetas/<int:planeta_id>' , methods=['DELETE'])   
def favoritos_planetas_delete(planeta_id):
    planeta = Planeta.query.get(planeta_id)
    usuario = Usuario.query.get(1)
    usuario.planetas.remove(planeta)
    db.session.commit()
    return jsonify({"succes": "Ya se elimino el planeta favorito satisfactoriamente"}), 200

@app.route('/favoritos/personajes/<int:personaje_id>' , methods = ['DELETE'])  
def favoritos_personajes_delete(personaje_id):
    personaje = Personaje.query.get(personaje_id)
    usuario = Usuario.query.get(1)
    usuario.personajes.remove(personaje)
    db.session.commit()
    return jsonify({"succes": "Ya se elimino el personaje favorito satisfactoriamente"}), 200  


   
    # favoritosPersonajes= tabla_pivote1.query.all()
    # favoritosPlanetas= tabla_pivote2.query.all()
    # print(favoritosPersonajes)
    # print(favoritosPlanetas)
    # lista2 = [favoritosPersonajes + favoritosPlanetas]
    # for favoritos in lista2:
    #     lista2.append(favoritos.serialize())
    # return jsonify(lista2), 200   


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
