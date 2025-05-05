from ConexionMongo import get_db
from models.producto import Producto
from utils.RegistrarActividadCatalogo import registrar_actividad

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
    db=get_db()
    productos_coleccion=db.productos
    results=productos_coleccion.find()

    print("Id","Nombre","Precio","Stock","Descuento")

    for r in results:
        print(r["id_producto"],r["nombre"],r["precio"],r["stock"],r["descuento"])

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




