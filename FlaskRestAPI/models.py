from importlib.resources import Resource
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class PersonaModel(db.Model):
    __tablename__ = 'persona'
    id_persona = db.Column(db.Integer, primary_key=True, autoincrement=True)
    primernombre = db.Column(db.String(100))
    segundonombre = db.Column(db.String(100))
    paterno = db.Column(db.String(50))
    materno = db.Column(db.String(50))
    ci = db.Column(db.String(15))
    celular = db.Column(db.Integer())

    def __init__(self, primernombre,segundonombre, paterno, materno, ci, celular):
        self.primernombre = primernombre
        self.segundonombre = segundonombre
        self.paterno = paterno
        self.materno = materno
        self.ci = ci
        self.celular = celular

    def json(self):
        return {"id_persona": self.id_persona, "primernombre": self.primernombre, "segundonombre": self.segundonombre,"paterno": self.paterno, "materno": self.materno, "ci": self.ci, "celular": self.celular}


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
    edad = db.Column(db.String(100))
    peso = db.Column(db.Integer())
    altura = db.Column(db.Integer())
    problemas_salud = db.Column(db.String(100))
    objetivo = db.Column(db.String(150))
    fk_id_persona = db.Column(db.Integer())
    grasa = db.Column(db.Integer())
    experiencia = db.Column(db.Integer())
    sexo = db.Column(db.Integer())
    tipocuerpo = db.Column(db.String(50))
    rutina = db.Column(db.Integer())

    def __init__(self, edad, peso, altura, problemas_salud, objetivo, fk_id_persona, grasa, experiencia, sexo, tipocuerpo, rutina):
        self.edad = edad
        self.peso = peso
        self.altura = altura
        self.problemas_salud = problemas_salud
        self.objetivo = objetivo
        self.fk_id_persona = fk_id_persona
        self.grasa = grasa
        self.experiencia = experiencia
        self.sexo = sexo
        self.tipocuerpo = tipocuerpo
        self.rutina = rutina

    def json(self):
        return {"id_diagnostico": self.id_diagnostico, "edad": self.edad, "peso": self.peso, "altura": self.altura, "problemas_salud": self.problemas_salud, "objetivo": self.objetivo, "fk_id_persona": self.fk_id_persona, "grasa": self.grasa, "experiencia": self.experiencia, "sexo": self.sexo, "tipocuerpo": self.tipocuerpo, "rutina": self.rutina}


class PagoModel(db.Model):
    __tablename__ = 'pagos'
    id_pago = db.Column(db.Integer, primary_key=True)
    fk_id_usuario = db.Column(db.Integer)
    fk_id_servicio = db.Column(db.Integer)
    monto_pagado = db.Column(db.Integer)
    fecha = db.Column(db.String(100))
    fk_id_usuario_empleado = db.Column(db.Integer)
    fecha_inicio_sus = db.Column(db.String(100))
    fecha_fin_sus = db.Column(db.String(100))

    def __init__(self, fk_id_usuario, fk_id_servicio, monto_pagado, fecha, fk_id_usuario_empleado, fecha_inicio_sus, fecha_fin_sus):
        self.fk_id_usuario = fk_id_usuario
        self.fk_id_servicio = fk_id_servicio
        self.monto_pagado = monto_pagado
        self.fecha = fecha
        self.fk_id_usuario_empleado = fk_id_usuario_empleado
        self.fecha_inicio_sus = fecha_inicio_sus
        self.fecha_fin_sus = fecha_fin_sus

    def json(self):
        return {"id_pago":self.id_pago, "fk_id_usuario": self.fk_id_usuario, "fk_id_servicio": self.fk_id_servicio, "monto_pagado": self.monto_pagado, "fecha": self.fecha, "fecha_inicio_sus": self.fecha_inicio_sus, "fecha_fin_sus": self.fecha_fin_sus}

class ServicioModel(db.Model):
    __tablename__ = 'servicio'
    id_servicio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Integer)

    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def json(self):
        return {"id_servicio": self.id_servicio, "nombre": self.nombre, "precio": self.precio}

class RutinaUsuarioModel(db.Model):
    __tablename__ = 'rutinasusuarios'
    id_rutina_usuario = db.Column(db.Integer, primary_key=True)
    fk_id_persona = db.Column(db.String(100))
    fk_id_rutina = db.Column(db.Integer)
    completa = db.Column(db.Boolean)

    def __init__(self, fk_id_persona, fk_id_rutina, completa):
        self.fk_id_persona = fk_id_persona
        self.fk_id_rutina = fk_id_rutina
        self.completa = completa

    def json(self):
        return {"id_rutina_usuario": self.id_rutina_usuario, "fk_id_persona": self.fk_id_persona, "fk_id_rutina": self.fk_id_rutina, "completa": self.completa}

class RutinaModel(db.Model):
    __tablename__ = 'rutinas'
    id_rutina = db.Column(db.Integer, primary_key=True)
    imagen = db.Column(db.String(1000))
    titulo = db.Column(db.String(200))
    repeticiones = db.Column(db.String(200))
    descripcion = db.Column(db.String(500))
    instrucciones = db.Column(db.String(500))
    video = db.Column(db.String(1000))
    id_rutina_grupo = db.Column(db.Integer)

    def __init__(self, imagen, titulo, repeticiones, descripcion, instrucciones, video, id_rutina_grupo):
        self.imagen = imagen
        self.titulo = titulo
        self.repeticiones = repeticiones
        self.descripcion = descripcion
        self.instrucciones = instrucciones
        self.video = video
        self.id_rutina_grupo = id_rutina_grupo

    def json(self):
        return {"id_rutina": self.id_rutina, "imagen": self.imagen, "titulo": self.titulo, "repeticiones": self.repeticiones, "descripcion": self.descripcion, "instrucciones": self.instrucciones, "video": self.video, "id_rutina_grupo": self.id_rutina_grupo}

class NoticiasModel(db.Model):
    __tablename__ = 'noticias'
    id_noticia = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    descripcion = db.Column(db.String(1000))
    imagen = db.Column(db.String(1000))
    fecha = db.Column(db.String(20))

    def __init__(self, titulo, descripcion, imagen, fecha):
        self.titulo = titulo
        self.descripcion = descripcion
        self.imagen = imagen
        self.fecha = fecha

    def json(self):
        return {"id_noticia": self.id_noticia, "titulo": self.titulo, "descripcion": self.descripcion, "imagen": self.imagen, "fecha": self.fecha}