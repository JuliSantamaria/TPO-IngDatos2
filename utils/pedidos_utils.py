from ConexionMongo import get_db
from models.factura import Factura
from utils.factura_utils import ver_factura


def ver_pedido(id_pedido):
    db=get_db()
    pedidos_coleccion=db.pedidos
    pedido=pedidos_coleccion.find_one({"id_pedido":id_pedido})

    if not pedido:
        print("El pedido no existe")

    else:
        nombre=pedido["nombre"]
        apellido=pedido["apellido"]

        print("************************")
        print(f"ID Pedido: {id_pedido}")
        print(f"Nombre del cliente: {nombre}")
        print(f"Apellido del cliente: {apellido}")

        pedidos_productos=pedido["productos"]

        for doc in pedidos_productos:
            print("--------------------------------")
            print(f"Id Producto: {doc['id_producto']} --- Cantidad: {doc['cantidad']}")

        print("************************")
    
def convertir_pedido_factura(documento,id_pedido):
    db=get_db()
    pedidos_coleccion=db.pedidos
    usuarios_coleccion=db.usuarios
    usuario=usuarios_coleccion.find_one({"documento":documento})
    num=len(usuario["historial_ordenes"])
    id_factura=f'factura:{documento}:{num}'
    id_pedido=id_pedido
    pedidos_coleccion=db.pedidos
    pedido=pedidos_coleccion.find_one({"id_pedido":id_pedido})
    productos_coleccion=db.productos

    if not pedido:
        print("El pedido no existe")

    else:
        nombre=usuario["nombre"]
        apellido=usuario["apellido"]
        direccion=usuario["direccion"]
        pedidos_productos=pedido["productos"]
        aplicacion_descuento=pedido["aplicacion_descuento"]
        importe=0
        importe_total=0
        factura=Factura(id_factura,id_pedido,nombre,apellido,direccion,importe,importe_total)

        for doc in pedidos_productos:
            id_producto=int(doc['id_producto'])
            cantidad=int(doc['cantidad'])
            producto=productos_coleccion.find_one({"id_producto":id_producto})
            precio=int(producto['precio'])

            if aplicacion_descuento==False:
                descuento=0
                descuento_aplicable=0

            else:
                descuento=int(producto['descuento'])
                descuento_aplicable=(precio*(descuento/100))

            precio_total=precio*cantidad
            precio_final=(precio-descuento_aplicable)*cantidad
            importe=importe+precio_final
            factura.agregar_producto(id_producto,cantidad,precio,descuento_aplicable*cantidad,precio_total,precio_final)
            factura.set_importe(importe)
            
        importe_total=int(importe+(importe*0.21))
        factura.set_importe_total(importe_total)
        facturas_coleccion=db.facturas
        facturas_coleccion.insert_one(factura.to_dict())
        filtro = {'documento':documento}
        factura_insert={'id_factura':id_factura}
        actualizacion={'$push': {'facturas_a_pagar':factura_insert}}
        usuarios_coleccion.update_one(filtro,actualizacion)
        ver_factura(id_factura)





        



