from importlib.resources import Resource
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class PersonaModel(db.Model):
    __tablename__ = 'persona'
    id_persona = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100))
    paterno = db.Column(db.String(50))
    materno = db.Column(db.String(50))
    ci = db.Column(db.String(15))    
    celular = db.Column(db.Integer())

    def __init__(self, nombres, paterno, materno, ci, celular):
        self.nombres = nombres
        self.paterno = paterno
        self.materno = materno
        self.ci = ci
        self.celular = celular

    def json(self):
        return {"nombres":self.nombres, "paterno":self.paterno, "materno":self.materno, "ci":self.ci, "celular":self.celular}