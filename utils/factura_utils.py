
from datetime import datetime

from ConexionMongo import get_db


def ver_factura(id_factura):
    db=get_db()
    facturas_coleccion=db.facturas
    factura=facturas_coleccion.find_one({"id_factura":id_factura})

    if not factura:
        print("La factura no existe")

    else:
        nombre=factura["nombre"]
        apellido=factura["apellido"]
        direccion=factura["direccion"]
        importe=factura["importe"]
        imoprte_total=factura["importe_total"]

        print("************************")
        print(f"ID Factura: {id_factura}")
        print(f"Nombre del cliente: {nombre}")
        print(f"Apellido del cliente: {apellido}")
        print(f"Direccion: {direccion}")

        factura_productos=factura["productos"]
        impuestos=True

        while impuestos:
            print("1-Monotributista")
            print("2-Excento")
            print("3-Consumidor final")
            print("4-Responsable inscripto")
            seleccion=input("Ingrese su condicion: ")

            if seleccion=='4':
                impuestos=False

            elif seleccion=='1' or seleccion=='2' or seleccion=='3':
                impuestos=False

            else:
                print("Opcion no valida")

        for doc in factura_productos:
            print("--------------------------------")
            print(f"Id Producto: {doc['id_producto']} --- Cantidad: {doc['cantidad']} --- Precio: {doc['precio']} --- Precio total: {doc['precio_total']} --- Descuento: {doc['descuento']}--- Precio final: {doc['precio_final']}")
        
        if seleccion=='4':
            print("************************")
            print(f"Importe: {importe}")
            print(f"Importe total (con iva): {imoprte_total}")
            print("************************")

        else:
            print("************************")
            print(f"Importe total (con iva): {imoprte_total}")
            print("************************")

def pagar_factura(documento,id_factura):
    db=get_db()
    facturas_coleccion=db.facturas
    factura=facturas_coleccion.find_one({"id_factura":id_factura})

    if not factura:
        print("La factura no existe")

    else:
        importe=int(factura["importe_total"])
        usuarios_coleccion=db.usuarios
        usuario=usuarios_coleccion.find_one({"documento":documento})
        cuenta_corriente=int(usuario["cuenta_corriente"])
        pago=False
        cuenta_insuficiente=False
        seleccion=0
        now = datetime.now()
        hora_actual = now.time()
        hora=hora_actual.strftime("%H:%M:%S")
        fecha_actual = now.date()
        fecha=fecha_actual.strftime("%Y-%m-%d")

        while pago!=True:
            print("Seleccione la forma de pago:")
            print("1-Efectivo")
            print("2-Tarjeta")
            print("3-Cuenta corriente")
            print("4-En punto de retiro")
            seleccion=input("Ingrese la opcion: ")

            if seleccion=='1':
                print("Pago en efectivo registrado")
                pago=True
                forma="Efectivo"

            elif seleccion=='2':
                print("Pago con tarjeta registrado")
                pago=True
                filtro = {'id_factura':id_factura}
                forma="Tarjeta"

            elif seleccion=='3':
                if importe>cuenta_corriente:
                    cuenta_insuficiente=True
                    break

                else:
                    print("Pago con cuenta corriente registado")
                    valor_nuevo=cuenta_corriente-importe
                    filtro_usuario = {'documento':documento}
                    actualizacion_usuario = {'$set': {'cuenta_corriente':valor_nuevo}}
                    usuarios_coleccion.update_one(filtro_usuario,actualizacion_usuario)
                    forma="Cuenta corriente"
                    pago=True

            elif seleccion=='4':
                print("Pago en punto de retiro registrado")
                pago=True
                forma="En punto de retiro"

            else:
                print("Opcion incorrecta, intente de nuevo")

        if cuenta_insuficiente:
            print("Dinero en cuenta corriente insuficiente")

        else:
            operador=input("Ingrese el operador interviniente, si no hay presione 0: ")

            if operador=="0":
                operador="-"

            pago_data={
                "forma_de_pago":forma,
                "operador_interviniente":operador,
                "fecha":fecha,
                "hora":hora,
                "monto":importe
            }

            filtro = {'id_factura':id_factura}
            actualizacion = {'$set': {'pago':pago_data}}
            facturas_coleccion.update_one(filtro,actualizacion)

            filtro_factura = {'documento':documento}
            factura_insert={'id_factura':id_factura}
            actualizacion={'$push': {'facturas_pagadas':factura_insert}}
            eliminar = {'$pull': {'facturas_a_pagar': factura_insert}}
            usuarios_coleccion.update_one(filtro_factura,actualizacion)
            usuarios_coleccion.update_one(filtro_factura,eliminar)