from ConexionMongo import get_db
from models.producto import Producto
from utils.RegistrarActividadCatalogo import *



def crear_producto():
    db=get_db()
    productos_coleccion=db.productos

    id_producto=int(input("id del producto: "))

    while productos_coleccion.find_one({"id_producto":id_producto}):
        print("El id ya existe ingrese otro")
        id_producto=int(input("id del producto: "))

    nombre=input("Nombre: ")
    descripcion=input("Descripcion: ")
    precio=int(input("Precio: "))
    stock=int(input("Stock: "))
    foto_url=input("Url de la foto: ")
    comentarios=[]
    video_url=input("Url del video: ")

    producto=Producto(id_producto,nombre,descripcion,precio,stock,foto_url,comentarios,video_url)
    productos_coleccion.insert_one(producto.to_dict())


def ver_productos():
    db = get_db()
    productos_coleccion = db.productos
    results = productos_coleccion.find()

    print("\n{:<5} {:<20}".format("ID", "Nombre"))
    print("-" * 30)

    for r in results:
        print("{:<5} {:<20}".format(
            r.get("id_producto", ""),
            r.get("nombre", "")
        ))
    print("-" * 30)

def ver_top_productos(limit=5):
    db = get_db()
    ranking_coleccion = db.ranking_productos
    productos_coleccion = db.productos
    results = productos_coleccion.find()

    top_productos = ranking_coleccion.find().sort("vistas", -1).limit(limit)

    print("{:<5} {:<30} {:<10}".format("ID", "Nombre", "Vistas"))
    print("-" * 50)

    for p in top_productos:
        print("{:<5} {:<30} {:<10}".format(
            p.get("id_producto", ""),
            p.get("nombre", ""),
            p.get("vistas", 0)
        ))

    print("-" * 50)

def cargar_descuento(id_producto,cantidad):
    db=get_db()
    productos_coleccion=db.productos
    producto=productos_coleccion.find_one({"id_producto":id_producto})

    if not producto:
        print("El producto no fue encontrado")

    else:
        filtro={"id_producto":id_producto}
        actualizacion={'$set': {'descuento':cantidad}}
        productos_coleccion.update_one(filtro,actualizacion)

def agregar_comentario(id_producto,comentario):
    db=get_db()
    productos_coleccion=db.productos
    producto=productos_coleccion.find_one({"id_producto":id_producto})
    
    if not producto:
        print("El producto no fue encontrado")

    else:
        filtro={"id_producto":id_producto}
        actualizacion={'$push': {'comentarios':comentario}}
        productos_coleccion.update_one(filtro,actualizacion)

def actualizar_producto(documento):
    db = get_db()
    productos_coleccion = db.productos

    print("1-Nombre")
    print("2-Descripcion")
    print("3-Precio")
    print("4-Stock")
    print("5-Descuento")
    print("6-Url Foto")
    print("7-Url video")
    seleccion=input("¿Que desea actualizar?: ")
    id_producto = int(input("Ingrese el id del producto a actualizar: "))

    producto_actual = productos_coleccion.find_one({"id_producto": id_producto})

    if not producto_actual:
        print("Producto no encontrado")

    else:
        if seleccion=='1':
            nombre = input(f"Nombre ({producto_actual['nombre']}): ") or producto_actual['nombre']
            tipo='nombre'
            valor_viejo=producto_actual['nombre']
            valor_nuevo=nombre

        if seleccion=='2':
            descripcion = input(f"Descripcion ({producto_actual['descripcion']}): ") or producto_actual['descripcion']
            tipo='descripcion'
            valor_viejo=producto_actual['descripcion']
            valor_nuevo=descripcion

        if seleccion=='3':
            precio = int(input(f"Precio ({producto_actual['precio']}): "))
            tipo='precio'
            valor_viejo=producto_actual['precio']
            valor_nuevo=precio

        if seleccion=='4':
            stock = int(input(f"Stock ({producto_actual['stock']}): "))
            tipo='stock'
            valor_viejo=producto_actual['stock']
            valor_nuevo=stock

        if seleccion=='5':
            descuento = int(input(f"Descuento ({producto_actual['descuento']}): "))
            tipo='descuento'
            valor_viejo=producto_actual['descuento']
            valor_nuevo=descuento

        if seleccion=='6':
            foto_url = input(f"Url de la foto ({producto_actual['foto_url']}): ") or producto_actual['foto_url']
            tipo='foto_url'
            valor_viejo=producto_actual['foto_url']
            valor_nuevo=foto_url

        if seleccion=='7':
            video_url = input(f"Url del video ({producto_actual['video_url']}): ") or producto_actual['video_url']
            tipo='video_url'
            valor_viejo=producto_actual['video_url']
            valor_nuevo=video_url

        filtro={"id_producto":id_producto}
        actualizacion={'$set': {tipo:valor_nuevo}}
        productos_coleccion.update_one(filtro,actualizacion)

        registrar_actividad(id_producto,tipo,valor_viejo,valor_nuevo,documento)

def ver_producto_por_id(id_producto, redis_conn):
    db = get_db()
    producto = db.productos.find_one({"id_producto": id_producto})

    if producto:
        print("\n--- Detalles del Producto ---")
        print(f"Nombre: {producto.get('nombre')}")
        print(f"Descripción: {producto.get('descripcion')}")
        print(f"Precio: ${producto.get('precio')}")
        print(f"Stock: {producto.get('stock')}")
        print(f"Descuento: {producto.get('descuento')}")

        registrar_vista_producto(redis_conn, id_producto)

    else:
        print("❌ Producto no encontrado.")

