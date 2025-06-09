from utils.auth_utils import *
from utils.carrito_utils import *
from utils.factura_utils import *
from utils.producto_utils import *
from utils.RegistrarActividadCatalogo import *
from utils.RegistrarConexion import *
from ConexionRedis import get_redis_client
import threading


def main():

    redis_conn = get_redis_client()

    print("Bienvenido a la tienda de deportes")

    while True:
        print("**********************")
        print("1-Registrar usuario")
        print("2-Iniciar Sesion")
        print("3-Cerrar Sesion")
        seleccion=input("Elija una opcion: ")

        if seleccion=='1':
            documento=input("Documento: ")
            contraseña=input("Contraseña: ")
            nombre=input("Nombre: ")
            apellido=input("Apellido: ")
            direccion=input("Direccion: ")

            try:
                id_usuario=registrar_usuario(nombre,apellido,contraseña,documento,direccion)
                print("Usuario registrado correctamente")
            except ValueError as e:
                print(e)
        
        elif seleccion=='2':
            documento=input("Documento: ")
            contraseña=input("Contraseña: ")
            if login_usuario(documento,contraseña):
                print("Inicio de sesion exitoso")
               # hilo_ranking = threading.Thread(target=guardar_ranking_periodicamente, daemon=True)
               # hilo_ranking.start()
                if es_admin(documento):
                    while True:
                        print("*******************")
                        print("1-Crear producto")
                        print("2-Actualizar producto")
                        print("3-Agregar descuento")
                        print("4-Ver lista de cambios de catalogo")
                        print("5-Agregar dinero a cuenta corriente")
                        print("6 - Guardar ranking de productos")
                        print("7-Salir")
                        seleccion_admin=input("Elija una opcion: ")
                        if seleccion_admin=='1':
                            crear_producto()
                        elif seleccion_admin=='2':
                            actualizar_producto(documento)
                        elif seleccion_admin=='3':
                            id_producto=int(input("Ingrese el id del producto: "))
                            cantidad=int(input("Ingrese el numero del porcentaje del descuento: "))
                            cargar_descuento(id_producto,cantidad)
                        elif seleccion_admin=='4':
                            ver_lista_cambios()
                        elif seleccion_admin=='5':
                            documento_usuario=input("Ingrese el documento del usuario: ")
                            cantidad_dinero=int(input("Ingrese el dinero a agregar: "))
                            agregar_cuenta_corriente(documento_usuario,cantidad_dinero)
                        elif seleccion_admin == '6':
                            guardar_ranking_en_mongo(redis_conn, get_db())
                            print("✅ Ranking guardado en MongoDB.")
                        elif seleccion_admin=='7':
                            break
                        else:
                            print("Opcion incorrecta")

                else:
                        
                    registrar_conexion(documento)  # Registrar conexión
                    print("Elija opcion para seguir: ")
                    while True:
                        print("*******************")
                        print("1-Ver datos")
                        print("2-Catalogo")
                        print("3-Carrito")
                        print("4-Ver pedido")
                        print("5-Factura")
                        print("6-Salir")
                        seleccion_menu=input("Elija una opcion: ")
                        if seleccion_menu=='1':
                            ver_datos(documento)
                        elif seleccion_menu=='2':
                            print("*******************")
                            print("1-Ver todo el catálogo")
                            print("2-Ver un producto (y registrar vista)")
                            print("3-Ver productos mas visitados")
                            print("4-Añadir comentario")
                            seleccion_catalogo=input("Elija una opcion: ")

                            if seleccion_catalogo=='1':
                                ver_productos()
                            elif seleccion_catalogo=='2':
                               id_producto = int(input("Ingrese el ID del producto: "))
                               ver_producto_por_id(id_producto, redis_conn)
                            elif seleccion_catalogo=='3':
                                ver_top_productos()
                            elif seleccion_catalogo=='4':
                                id_producto=int(input("Ingrese el id: "))
                                comentario=input("Comentario: ")
                                agregar_comentario(id_producto,comentario)
                            else:
                                print("Opcion incorrecta")
                            

                        elif seleccion_menu=='3':
                            print("*******************")
                            print("1-Añadir Producto")
                            print("2-Cambiar cantidad producto")
                            print("3-Eliminar Producto")
                            print("4-Ver carrito")
                            print("5-Finalizar carrito y generar pedido")
                            print("6-Salir")
                            seleccion_input=input("Elija una opcion: ")
                            if seleccion_input=='1':
                                id_producto=int(input("Ingrese el id del producto: "))
                                cantidad=int(input("Ingrese la cantidad del producto: "))
                                agregar_producto_carrito(documento,id_producto,cantidad)
                            elif seleccion_input=='2':
                                id_producto=int(input("Ingrese el id del producto: "))
                                cantidad=int(input("Ingrese la cantidad del producto: "))
                                cambiar_cantidad_producto(documento,id_producto,cantidad)
                            elif seleccion_input=='3':
                                id_producto=int(input("Ingrese el id del producto: "))
                                eliminar_producto_carrito(documento,id_producto)
                            elif seleccion_input=='4':
                                contenido=obtener_contenido_carrito(documento)
                                print(contenido)
                            elif seleccion_input=='5':
                                convertir_carrito_pedido(documento)
                            elif seleccion_input=='6':
                                pass
                            else:
                                print("Opcion incorrecta")
                            
                        elif seleccion_menu=="4":
                            id_pedido=input("Ingrese el ID del pedido: ")
                            ver_pedido(id_pedido)

                        elif seleccion_menu=="5":
                            print("*******************")
                            print("1-Generar factura")
                            print("2-Ver factura")
                            print("3-Pagar factura")
                            seleccion_factura=input("Elija una opcion: ")

                            if seleccion_factura=='1':
                                id_pedido=input("Ingrese el ID del pedido: ")
                                convertir_pedido_factura(documento,id_pedido)

                            elif seleccion_factura=='2':
                                id_factura=input("Ingrese el ID del factura: ")
                                ver_factura(id_factura)

                            elif seleccion_factura=='3':
                                id_factura=input("Ingrese el ID del factura: ")
                                pagar_factura(documento,id_factura)
                                
                        elif seleccion_menu=="6":
                            break


            else:
                print("Documento o contraseña incorrectos")
        
        elif seleccion=='3':
            if not es_admin(documento):
                registrar_desconexion(documento)  
                categoria = categorizar_usuario(documento)
                print(f"El usuario {documento} es un usuario {categoria}", "\n")
            print("Saliendo del sistema...")
            print("Cierre de sesion exitosa!")
            break

        else:
            print("Opcion invalida")

if __name__ == "__main__":
    main()