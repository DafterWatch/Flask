from ast import parse
from distutils import core
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from models import PersonaModel, db
from flask import Flask
from flask_cors import CORS

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
        return {'Persona':list(x.json() for x in personas)}
    def post(self):
        data = request.get_json()
        new_persona = PersonaModel(data['nombres'],data['paterno'], data['materno'], data['ci'], data['celular'])
        db.session.add(new_persona)
        db.session.commit()
        db.session.flush()
        #print(db.id)
        return new_persona.json(),201

class SinglePersonaView(Resource):
    def get(self, id):
        persona = PersonaModel.query.filter_by(id_persona=id).first()
        if persona:
            return persona.json()
        return {'message':'Persona id_persona not found'},404
    def delete(self, id):
        persona = PersonaModel.query.filter_by(id_persona=id).first()
        if persona:
            db.session.delete(persona)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message':'Persona not found'},404
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
            persona = PersonaModel(id_persona=id,**data)

        db.session.add(persona)
        db.session.commit()
        return persona.json()
    
api.add_resource(PersonaView, '/personas')
api.add_resource(SinglePersonaView, '/persona/<int:id>')

app.debug = True
if __name__ == '__main__':
    app.run(host='localhost', port=5000)