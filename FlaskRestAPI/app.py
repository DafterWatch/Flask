from ast import parse
from distutils import core
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from models import PersonaModel, UsuarioModel, db
from flask import Flask
from flask_cors import CORS
from modelo import predecir

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hmfdzpkjqx@localhost/GimnasioDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


class PersonaView(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('name',
    #     type=str,
    #     required=True,
    #     help = "Can't leave blank"
    # )
    # parser.add_argument('price',
    #     type=float,
    #     required=True,
    #     help="Can't leave blank"
    # )
    # parser.add_argument('brand',
    #     type=str,
    #     required=True,
    #     help="Can't leave blank"
    # )/
    def get(self):
        personas = PersonaModel.query.all()
        return {'Personas': list(x.json() for x in personas)}

    def post(self):
        data = request.get_json()
        new_persona = PersonaModel(
            data['nombres'], data['paterno'], data['materno'], data['ci'], data['celular'])
        db.session.add(new_persona)
        db.session.commit()
        db.session.flush()
        return new_persona.json(), 201


class SinglePersonaView(Resource):
    def get(self, id):
        persona = PersonaModel.query.filter_by(id_persona=id).first()
        if persona:
            return persona.json()
        return {'message': 'Persona id_persona not found'}, 404

    def delete(self, id):
        persona = PersonaModel.query.filter_by(id_persona=id).first()
        if persona:
            db.session.delete(persona)
            db.session.commit()
            return {'message': 'Deleted'}
        else:
            return {'message': 'Persona not found'}, 404

    def put(self, id):
        data = request.get_json()
        persona = PersonaModel.query.filter_by(id_persona=id).first()
        if persona:
            persona.nombres = data['nombres']
            persona.paterno = data['paterno']
            persona.materno = data['materno']
            persona.ci = data['ci']
            persona.celular = data['celular']
        else:
            persona = PersonaModel(id_persona=id, **data)

        db.session.add(persona)
        db.session.commit()
        return persona.json()


class ModeloView(Resource):
    def post(self):
        data = request.get_json()
        datos = ([data['grasa'], data['altura'], data['peso'], data['experiencia'],
                  data['sexo'], data['endomorfo'], data['mesomorfo'], data['objetivo']])
        prediccion = predecir(datos)
        return {"valor": str(prediccion[0])}, 201


class UsuarioView(Resource):
    def get(self):
        usuarios = UsuarioModel.query.all()
        return {'Usuarios': list(x.json() for x in usuarios)}

    def post(self):
        data = request.get_json()
        new_usuario = UsuarioModel(
            data['usuario'], data['contrasenia'], data['correo'], data['rol'], data['fk_id_persona'])
        db.session.add(new_usuario)
        db.session.commit()
        db.session.flush()
        return new_usuario.json(), 201


class SingleUsuarioView(Resource):
    def get(self, id):
        usuario = UsuarioModel.query.filter_by(id_usuario=id).first()
        if usuario:
            return usuario.json()
        return {'message': 'Usuario id_usuario not found'}, 404

    def delete(self, id):
        usuario = UsuarioModel.query.filter_by(id_usuario=id).first()
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return {'message': 'Deleted'}
        else:
            return {'message': 'Usuario not found'}, 404

    def put(self, id):
        data = request.get_json()
        usuario = UsuarioModel.query.filter_by(id_usuario=id).first()
        if usuario:
            usuario.usuario = data['usuario']
            usuario.contrasenia = data['contrasenia']
            usuario.correo = data['correo']
            usuario.rol = data['rol']
            usuario.fk_id_persona = data['fk_id_persona']
        else:
            usuario = UsuarioModel(id_usuario=id, **data)

        db.session.add(usuario)
        db.session.commit()
        return usuario.json()


api.add_resource(PersonaView, '/personas')
api.add_resource(SinglePersonaView, '/persona/<int:id>')
api.add_resource(ModeloView, '/modelo')
api.add_resource(UsuarioView, '/usuarios')
api.add_resource(SingleUsuarioView, '/usuario/<int:id>')

app.debug = True
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
