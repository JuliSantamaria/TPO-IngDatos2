from ConexionMongo import get_db

def registrar_actividad(id_producto,tipo, valor_anterior, valor_nuevo, operador):
    db=get_db()
    coleccion_actividad=db.cambios_catalogo
    
    log = {
        "id":id_producto,
        "tipo": tipo,
        "valor_anterior": valor_anterior,
        "valor_nuevo": valor_nuevo,
        "operador": operador
    }

    coleccion_actividad.insert_one(log)

def ver_lista_cambios():
    db=get_db()
    coleccion_actividad=db.cambios_catalogo
    coleccion=coleccion_actividad.find()

    print("Lista de cambios")

    for doc in coleccion:
        id=doc["id"]
        tipo=doc["tipo"]
        valor_anterior=doc["valor_anterior"]
        valor_nuevo=doc["valor_nuevo"]
        operador=doc["operador"]
        
        print(f'Id: {id} --- Tipo: {tipo} --- Valor anterior: {valor_anterior} --- Valor nuevo: {valor_nuevo} --- Operador: {operador}')
