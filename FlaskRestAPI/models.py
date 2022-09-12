from importlib.resources import Resource
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class PersonaModel(db.Model):
    __tablename__ = 'persona'
    id_persona = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
        return {"id_persona": self.id_persona, "nombres": self.nombres, "paterno": self.paterno, "materno": self.materno, "ci": self.ci, "celular": self.celular}


class UsuarioModel(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasenia = db.Column(db.String(50))
    correo = db.Column(db.String(100))
    rol = db.Column(db.String(50))
    fk_id_persona = db.Column(db.Integer())

    def __init__(self, usuario, contrasenia, correo, rol, fk_id_persona):
        self.usuario = usuario
        self.contrasenia = contrasenia
        self.correo = correo
        self.rol = rol
        self.fk_id_persona = fk_id_persona

    def json(self):
        return {"id_usuario": self.id_usuario, "usuario": self.usuario, "contrasenia": self.contrasenia, "correo": self.correo, "rol": self.rol, "fk_id_persona": self.fk_id_persona}


class DiagnosticoModel(db.Model):
    __tablename__ = 'diagnostico'
    id_diagnostico = db.Column(db.Integer, primary_key=True)
    edad = db.Column(db.Integer())
    peso = db.Column(db.Integer())
    altura = db.Column(db.Integer())
    problemas_salud = db.Column(db.String(100))
    objetivo = db.Column(db.String(150))
    fk_id_persona = db.Column(db.Integer())

    def __init__(self, edad, peso, altura, problemas_salud, objetivo, fk_id_persona):
        self.edad = edad
        self.peso = peso
        self.altura = altura
        self.problemas_salud = problemas_salud
        self.objetivo = objetivo
        self.fk_id_persona = fk_id_persona

    def json(self):
        return {"id_diagnostico": self.id_diagnostico, "edad": self.edad, "peso": self.peso, "altura": self.altura, "problemas_salud": self.problemas_salud, "objetivo": self.objetivo, "fk_id_persona": self.fk_id_persona}
