from ConexionMongo import get_db
from ConexionRedis import get_redis_client
from models.pedido import Pedido
from utils.pedidos_utils import *
import time
from datetime import datetime,timedelta

def agregar_producto_carrito(documento,id_producto,cantidad):
    r=get_redis_client()
    producto_key=f"producto:{documento}:{id_producto}"
    carrito_id=f"cart:{documento}"

    longitud=r.llen(carrito_id)
    if longitud==0:
        timestamp = time.time()
        r.set(f"{carrito_id}:timestamp", timestamp)

    db=get_db()
    productos_coleccion=db.productos
    producto=productos_coleccion.find_one({"id_producto":id_producto})

    if not producto:
        return print("No se encontro el producto")
    else:
        if hay_repetidos(r,carrito_id,id_producto):
            print("Ya hay un producto agregado con ese id")
        else:
            hay_stock=validar_stock(id_producto,cantidad)

            if hay_stock:
                precio_producto=int(producto["precio"])
                precio=precio_producto*cantidad
                r.hmset(producto_key,{'id':id_producto,'cantidad':cantidad,'precio_producto':precio_producto,'precio':precio})
                r.lpush(carrito_id,producto_key)

                print("Producto agregado")

                contenido=obtener_contenido_carrito(documento)
                print("Contenido del carrito:", contenido)

            else:
                print("No hay stock del producto")

def eliminar_producto_carrito(documento,id_producto):
    r=get_redis_client()

    carrito_id=f"cart:{documento}"
    producto_key=f"producto:{documento}:{id_producto}"

    r.lrem(carrito_id,0,producto_key)
    r.delete(producto_key)

    print("Producto eliminado")

def obtener_contenido_carrito(documento):
    r=get_redis_client()

    carrito_key=f"cart:{documento}"
    productos_keys = r.lrange(carrito_key, 0, -1)
    contenido = []

    for producto_key in productos_keys:
        producto = r.hgetall(producto_key)
        producto_decoded = {k.decode('utf-8'): v.decode('utf-8') for k, v in producto.items()}
        contenido.append(producto_decoded)

    return contenido

def calcular_total_carrito(documento):
    carrito_id=f"cart:{documento}"
    contenido=obtener_contenido_carrito(carrito_id)
    total=0

    for producto in contenido:
        precio=producto['precio']
        total += precio

    return total

def cambiar_cantidad_producto(documento,id_producto,cantidad):
    r=get_redis_client()

    producto_key=f"producto:{documento}:{id_producto}"
    carrito_id=f"cart:{documento}"
    productos_keys = r.lrange(carrito_id, 0, -1)

    for key in productos_keys:
        producto = r.hgetall(key)

        if int(producto[b'id'].decode('utf-8')) == id_producto:
            hay_stock=validar_stock(id_producto,cantidad)

            if hay_stock:
                precio_producto=int(producto[b'precio'])
                precio=precio_producto*cantidad
                r.hmset(producto_key,{'id':id_producto,'cantidad':cantidad,'precio_producto':precio_producto,'precio':precio})

                print("Producto actualizado")

                contenido=obtener_contenido_carrito(documento)
                print("Contenido del carrito:", contenido)
                break

            else:
                print("No hay stock del producto")
        else:
            print("El producto no está en el carrito")


def convertir_carrito_pedido(documento):
    r=get_redis_client()
    db=get_db()
    usuarios_coleccion=db.usuarios

    carrito_id=f"cart:{documento}"

    longitud=r.llen(carrito_id)
    if longitud==0:
        print("No hay nada en el carrito")

    else:
        tiempo_transcurrido = calcular_tiempo_desde_creacion(r,carrito_id)
        aplicacion_descuento=True

        if tiempo_transcurrido > timedelta(hours=72):
            aplicacion_descuento=False

        keys_producto=r.lrange(carrito_id,0,-1)
        usuario=usuarios_coleccion.find_one({"documento":documento})
        num=len(usuario["historial_ordenes"])
        id_pedido=f'pedido:{documento}:{num}'

        nombre=usuario["nombre"]
        apellido=usuario["apellido"]
        pedido=Pedido(id_pedido,nombre,apellido,aplicacion_descuento)

        for key_producto in keys_producto:
            producto=r.hgetall(key_producto)
            id_producto=int(producto[b'id'].decode('utf-8'))
            cantidad=int(producto[b'cantidad'])
            pedido.agregar_producto(id_producto,cantidad)
            restar_stock(id_producto,cantidad)

        pedidos_coleccion=db.pedidos

        for key_productos in keys_producto:
                r.delete(key_productos)

        r.delete(carrito_id)
        filtro = {'documento':documento}
        pedido_insert={'id_pedido':id_pedido}
        actualizacion={'$push': {'historial_ordenes':pedido_insert}}
        usuarios_coleccion.update_one(filtro,actualizacion)
        pedidos_coleccion.insert_one(pedido.to_dict())

        print("Pedido generado!")
        ver_pedido(id_pedido)

def validar_stock(id_producto,cantidad):
    db=get_db()
    producto_coleccion=db.productos
    producto=producto_coleccion.find_one({"id_producto":id_producto})
    cantidad_producto=producto["stock"]

    if cantidad_producto<cantidad:
        stock=False
    else:
        stock=True
    return stock

def restar_stock(id_producto,cantidad):
    db=get_db()
    producto_coleccion=db.productos
    producto=producto_coleccion.find_one({"id_producto":id_producto})

    cantidad_producto=producto["stock"]
    nueva_cantidad=cantidad_producto-cantidad

    filtro={"id_producto":id_producto}
    actualizacion={'$set': {'stock':nueva_cantidad}}
    producto_coleccion.update_one(filtro,actualizacion)
    
def hay_repetidos(r,carrito_id,id_producto):
    repetidos=False
    productos_keys = r.lrange(carrito_id, 0, -1)

    for key in productos_keys:
        producto_carrito = r.hgetall(key)

        if int(producto_carrito[b'id'].decode('utf-8')) == id_producto:
            repetidos= True

    return repetidos

def obtener_tiempo_creacion_carrito(r,carrito_key):
    timestamp = r.get(f"{carrito_key}:timestamp")

    if timestamp:
        timestamp = float(timestamp)
        tiempo_creacion = datetime.fromtimestamp(timestamp)

        return tiempo_creacion
    
    return None

def calcular_tiempo_desde_creacion(r,carrito_key):
    tiempo_creacion = obtener_tiempo_creacion_carrito(r,carrito_key)

    if tiempo_creacion:
        tiempo_actual = datetime.now()
        tiempo_transcurrido = tiempo_actual - tiempo_creacion
        return tiempo_transcurrido
    
    return None


        

