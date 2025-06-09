from ConexionMongo import get_db
from datetime import datetime, timezone, time
from ConexionRedis import get_redis_client

redis_con = get_redis_client

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

def registrar_vista_producto(redis_conn, producto_id):
    redis_conn.zincrby("vistas_productos", 1, f"producto:{producto_id}")

def guardar_ranking_en_mongo(redis_conn, mongo_db):
    top_productos = redis_conn.zrevrange("vistas_productos", 0, 9, withscores=True)

    registros = []
    for producto_key, score in top_productos:
        producto_id = producto_key.decode().split(":")[1]
        producto = mongo_db.productos.find_one({"id_producto": int(producto_id)})
        nombre = producto["nombre"] if producto else "Desconocido"
        registros.append({
            "producto_id": producto_id,
            "nombre": nombre,
            "vistas": int(score),
            "fecha": datetime.now(timezone.utc)
        })

    mongo_db.ranking_productos.insert_many(registros)

def guardar_ranking_periodicamente():
    while True:
        try:
            guardar_ranking_en_mongo(redis_con, get_db())
            print("[🕒] Ranking guardado automáticamente en MongoDB.")
        except Exception as e:
            print(f"[⚠️] Error al guardar ranking automáticamente: {e}")
        time.sleep(60)  # Espera 60 segundos