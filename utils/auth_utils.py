from ConexionMongo import get_db
from models.usuario import *


def registrar_usuario(nombre,apellido,contraseña,documento,direccion):
    db=get_db()
    usuarios_coleccion=db.usuarios

    if usuarios_coleccion.find_one({"documento":documento}):
        raise ValueError("El usuario ya existe")
    else:
        usuario=Usuario(nombre,apellido,documento,contraseña,direccion)
        usuarios_coleccion.insert_one(usuario.to_dict())

def login_usuario(documento,contraseña):
    db=get_db()
    usuarios_coleccion=db.usuarios

    usuario=usuarios_coleccion.find_one({"documento":documento})
    if not usuario:
        return False
    
    if usuario["contraseña"]==contraseña:
        return True
    
    return False

def es_admin(documento):
    db=get_db()
    usuarios_coleccion=db.usuarios
    usuario=usuarios_coleccion.find_one({"documento":documento})
    categoria_admin=usuario["categoria"]

    if categoria_admin=='Admin':
        return True
    else:
        return False
    
def ver_datos(documento):
    db=get_db()
    usuarios_coleccion=db.usuarios
    usuario=usuarios_coleccion.find_one({"documento":documento})

    nombre=usuario["nombre"]
    apellido=usuario["apellido"]
    direccion=usuario["direccion"]
    categoria=usuario["categoria"]
    cuenta_corriente=usuario["cuenta_corriente"]

    print(f"Nombre: {nombre} --- Apellido: {apellido} --- Direccion: {direccion} --- Categoria: {categoria} --- Cuenta Corriente: {cuenta_corriente}")

def agregar_cuenta_corriente(documento,cantidad):
    db=get_db()
    usuarios_coleccion=db.usuarios
    usuario=usuarios_coleccion.find_one({"documento":documento})
    
    if not usuario:
        print("No se encontro el usuario")
    else:
        filtro={"documento":documento}
        actualizacion={'$set': {'cuenta_corriente':cantidad}}
        usuarios_coleccion.update_one(filtro,actualizacion)