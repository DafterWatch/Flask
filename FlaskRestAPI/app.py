from ast import parse
from distutils import core
from sqlite3 import Date
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
#from FlaskRestAPI.models import PagoModel
from models import PersonaModel, UsuarioModel, DiagnosticoModel, PagoModel, ServicioModel, RutinaUsuarioModel, RutinaModel, db
from flask import Flask
from flask_cors import CORS
from modelo import predecir
import json 
from datetime import datetime
from json import dumps

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
        persona = PersonaModel.query.filter_by(ci=str(data['ci'])).first()
        if persona:
            return {'resultado': 0},
        else:
            new_persona = PersonaModel(
                data['nombres'], data['paterno'], data['materno'], data['ci'], data['celular'])
            db.session.add(new_persona)
            db.session.commit()
            db.session.flush()
            return {'resultado': 1, 'datos': new_persona.json()}, 201


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
        # [6,180,77,8,1,0,0,0]]
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
        usuario = UsuarioModel.query.filter_by(fk_id_persona=id).first()
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


class DiagnosticoView(Resource):
    def get(self):
        diagnosticos = DiagnosticoModel.query.all()
        return {'Diagnosticos': list(x.json() for x in diagnosticos)}

    def post(self):
        data = request.get_json()
        print("data")
        print(data)
        print("data")
        new_diagnostico = DiagnosticoModel( 
            data['edad'], data['peso'], data['altura'], data['problemas_salud'], data['objetivo'], data['fk_id_persona'], data['grasa'], data['experiencia'], data['sexo'], data['tipocuerpo'], data['rutina'])
        db.session.add(new_diagnostico)
        db.session.commit()
        db.session.flush()
        return new_diagnostico.json(), 201


class SingleDiagnosticoView(Resource):
    def get(self, id):
        diagnostico = DiagnosticoModel.query.filter_by(
            fk_id_persona=id).first()
        if diagnostico:
            print("diagnostico")
            print(diagnostico.json())
            print("diagnostico")
            return diagnostico.json()
        return {'message': 'Diagnostico id_diagnostico not found'}, 404

    def delete(self, id):
        diagnostico = DiagnosticoModel.query.filter_by(
            id_diagnostico=id).first()
        if diagnostico:
            db.session.delete(diagnostico)
            db.session.commit()
            return {'message': 'Deleted'}
        else:
            return {'message': 'Diagnostico not found'}, 404

    def put(self, id):
        data = request.get_json()
        diagnostico = DiagnosticoModel.query.filter_by(
            id_diagnostico=id).first()
        if diagnostico:
            diagnostico.edad = data['edad']
            diagnostico.peso = data['peso']
            diagnostico.altura = data['altura']
            diagnostico.grasa = data['grasa']
            diagnostico.experiencia = data['experiencia']
            diagnostico.problemas_salud = data['problemas_salud']
            diagnostico.objetivo = data['objetivo']
            diagnostico.fk_id_persona = data['fk_id_persona']
            diagnostico.sexo = data['sexo']
            diagnostico.tipocuerpo = data['tipocuerpo']
        else:
            diagnostico = DiagnosticoModel(id_usuario=id, **data)

        db.session.add(diagnostico)
        db.session.commit()
        return diagnostico.json()


class PagoView(Resource):
    def get(self):
        pagos = PagoModel.query.all()
        return {'Pagos': list(x.json() for x in pagos)}

    def post(self):
        data = request.get_json()
        new_pago = PagoModel(
            data['fk_id_usuario'], data['fk_id_servicio'], data['monto_pagado'], data['fecha'], data['fk_id_usuario_empleado'], data['fecha_inicio_sus'], data['fecha_fin_sus'])
        db.session.add(new_pago)
        db.session.commit()
        db.session.flush()
        return new_pago.json(), 201


class SinglePagoView(Resource):
    def get(self, id):
        pago = PagoModel.query.filter_by(fk_id_usuario=id).first()
        if pago:
            return pago.json()
        return {'message': 'Pago id_pago not found'}, 404

    def delete(self, id):
        pago = PagoModel.query.filter_by(id_pago=id).first()
        if pago:
            db.session.delete(pago)
            db.session.commit()
            return {'message': 'Deleted'}
        else:
            return {'message': 'Pago not found'}, 404

    def put(self, id):
        data = request.get_json()
        pago = PagoModel.query.filter_by(id_pago=id).first()
        if pago:
            pago.fk_id_usuario = data['fk_id_usuario']
            pago.fk_id_servicio = data['fk_id_servicio']
            pago.monto_pagado = data['monto_pagado']
            pago.fecha = data['fecha']
            pago.fk_id_usuario_empleado = data['fk_id_usuario_empleado']
            pago.fecha_inicio_sus = data['fecha_inicio_sus']
            pago.fecha_fin_sus = data['fecha_fin_sus']
        else:
            pago = PagoModel(id_pago=id, **data)

        db.session.add(pago)
        db.session.commit()
        return pago.json()


class ServicioView(Resource):
    def get(self):
        servicios = ServicioModel.query.all()
        return {'Servicios': list(x.json() for x in servicios)}

    def post(self):
        data = request.get_json()
        new_servicio = ServicioModel(
            data['nombre'], data['precio'])
        db.session.add(new_servicio)
        db.session.commit()
        db.session.flush()
        return new_servicio.json(), 201

class SingleServicioView(Resource):
    def get(self, id):
        servicio = ServicioModel.query.filter_by(id_servicio=id).first()
        if servicio:
            return servicio.json()
        return {'message': 'Servicio id_servicio not found'}, 404

    def delete(self, id):
        servicio = ServicioModel.query.filter_by(id_servicio=id).first()
        if servicio:
            db.session.delete(servicio)
            db.session.commit()
            return {'message': 'Deleted'}
        else:
            return {'message': 'Servicio not found'}, 404

    def put(self, id):
        data = request.get_json()
        servicio = ServicioModel.query.filter_by(id_servicio=id).first()
        if servicio:
            servicio.nombre = data['nombre']
            servicio.precio = data['precio']
        else:
            servicio = ServicioModel(id_servicio=id, **data)

        db.session.add(servicio)
        db.session.commit()
        return servicio.json()


class LoginView(Resource):
    def post(self):
        data = request.get_json()
        usuario = UsuarioModel.query.filter_by(
            usuario=data['usuario'], contrasenia=data['contrasenia']).first()
        if usuario:
            return {'resultado': 1, 'datos': usuario.json()}
        return {'resultado': 0, 'datos': ''}

class ValidateAddView(Resource):
    def post(self):
        data = request.get_json()
        persona = PersonaModel.query.filter_by(ci=str(data['ci'])).first()
        if persona:
            return {'resultado': 0},
        else:
            usuario = UsuarioModel.query.filter_by(correo=str(data['correo'])).first()
            if usuario:
                return {'resultado': 0}
            else:
                return {'resultado': 1}, 201


class RutinaUsuarioView(Resource):
    def get(self):
        rutinausuario = RutinaUsuarioModel.query.all()
        return {'RutinaUsuarios': list(x.json() for x in rutinausuario)}

    def post(self):
        data = request.get_json()
        new_rutinausuario = RutinaUsuarioModel(
            data['fk_id_persona'], data['fk_id_rutina'], data['completa'])
        db.session.add(new_rutinausuario)
        db.session.commit()
        db.session.flush()
        return new_rutinausuario.json(), 201

class SingleRutinaUsuarioView(Resource):
    def get(self, id):
        rutinausuario = RutinaUsuarioModel.query.filter_by(id_rutina_usuario=id).first()
        if rutinausuario:
            return rutinausuario.json()
        return {'message': 'rutinausuario id_rutina_usuario not found'}, 404

    def delete(self, id):
        rutinausuario = RutinaUsuarioModel.query.filter_by(id_rutina_usuario=id).first()
        if rutinausuario:
            db.session.delete(rutinausuario)
            db.session.commit()
            return {'message': 'Deleted'}
        else:
            return {'message': 'rutinausuario not found'}, 404

    def put(self, id):
        data = request.get_json()
        rutinaservicio = RutinaUsuarioModel.query.filter_by(id_rutina_usuario=id).first()
        if rutinaservicio:
            rutinaservicio.fk_id_persona = data['fk_id_persona']
            rutinaservicio.fk_id_rutina = data['fk_id_rutina']
            rutinaservicio.completa = data['completa']
        else:
            rutinaservicio = RutinaUsuarioModel(id_rutina_usuario=id, **data)

        db.session.add(rutinaservicio)
        db.session.commit()
        return rutinaservicio.json()

class RutinaView(Resource):
    def get(self):
        rutina = RutinaModel.query.all()
        return {'Rutinas': list(x.json() for x in rutina)}

    def post(self):
        data = request.get_json()
        new_rutina = RutinaModel(
            data['imagen'], data['titulo'], data['repeticiones'], data['descripcion'], data['instrucciones'], data['video'], data['id_rutina_grupo'])
        db.session.add(new_rutina)
        db.session.commit()
        db.session.flush()
        return new_rutina.json(), 201

class SingleRutinaView(Resource):
    def get(self, id):
        rutina = RutinaModel.query.filter_by(id_rutina=id).first()
        if rutina:
            return rutina.json()
        return {'message': 'rutina id_rutina not found'}, 404

    def delete(self, id):
        rutina = RutinaModel.query.filter_by(id_rutina=id).first()
        if rutina:
            db.session.delete(rutina)
            db.session.commit()
            return {'message': 'Deleted'}
        else:
            return {'message': 'rutina not found'}, 404

    def put(self, id):
        data = request.get_json()
        rutina = RutinaModel.query.filter_by(id_rutina=id).first()
        if rutina:
            rutina.imagen = data['imagen']
            rutina.titulo = data['titulo']
            rutina.repeticiones = data['repeticiones']
            rutina.descripcion = data['descripcion']
            rutina.instrucciones = data['instrucciones']
            rutina.video = data['video']
            rutina.id_rutina_grupo = data['id_rutina_grupo']
        else:
            rutina = RutinaModel(id_rutina=id, **data)

        db.session.add(rutina)
        db.session.commit()
        return rutina.json()


api.add_resource(PersonaView, '/personas')
api.add_resource(SinglePersonaView, '/persona/<int:id>')
api.add_resource(ModeloView, '/modelo')
api.add_resource(UsuarioView, '/usuarios')
api.add_resource(SingleUsuarioView, '/usuario/<int:id>')
api.add_resource(DiagnosticoView, '/diagnosticos')
api.add_resource(SingleDiagnosticoView, '/diagnostico/<int:id>')
api.add_resource(PagoView, '/pagos')
api.add_resource(SinglePagoView, '/pago/<int:id>')
api.add_resource(ServicioView, '/servicios')
api.add_resource(SingleServicioView, '/servicio/<int:id>')
api.add_resource(RutinaUsuarioView, '/rutinausuarios')
api.add_resource(SingleRutinaUsuarioView, '/rutinausuario/<int:id>')
api.add_resource(RutinaView, '/rutinas')
api.add_resource(SingleRutinaView, '/rutina/<int:id>')
api.add_resource(LoginView, '/login')
api.add_resource(ValidateAddView, '/validateAdd')

app.debug = True
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
