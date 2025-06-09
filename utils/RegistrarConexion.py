import datetime
from ConexionRedis import get_redis_client

redis_client = get_redis_client()

def registrar_conexion(documento):
    fecha_hora_inicio = datetime.datetime.now().timestamp()
    fecha_actual = datetime.date.today().strftime('%Y-%m-%d')

    redis_client.hset(f"usuario:{documento}:conexion", "inicio", fecha_hora_inicio)
    redis_client.pfadd(f"usuario:{documento}:dias_unicos", fecha_actual)

def registrar_desconexion(documento):
    fecha_hora_fin = datetime.datetime.now().timestamp()
    inicio = redis_client.hget(f"usuario:{documento}:conexion", "inicio")

    if inicio:  
        tiempo_conexion = fecha_hora_fin - float(inicio)
        fecha_actual = datetime.date.today().strftime('%Y-%m-%d')
        redis_client.lpush(f"usuario:{documento}:conexiones:{fecha_actual}", tiempo_conexion)
        redis_client.hdel(f"usuario:{documento}:conexion", "inicio")

def calcular_tiempo_total_conexion(documento, fecha):
    total_tiempo = 0
    conexiones = redis_client.lrange(f"usuario:{documento}:conexiones:{fecha}", 0, -1)

    for conexion in conexiones:
        total_tiempo += float(conexion)

    return total_tiempo

def categorizar_usuario(documento):
    fecha_actual = datetime.date.today()
    tiempo_total_semana = 0

    for i in range(7):
        fecha = (fecha_actual - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        tiempo_conexion = calcular_tiempo_total_conexion(documento, fecha)

        if tiempo_conexion > 0:
            tiempo_total_semana += tiempo_conexion
    
    dias_conexion = redis_client.pfcount(f"usuario:{documento}:dias_unicos")
    
    if dias_conexion == 0:
        return "LOW"

    tiempo_promedio_diario = (tiempo_total_semana / dias_conexion) / 60

    if tiempo_promedio_diario > 240:
        return "TOP"
    elif tiempo_promedio_diario > 120:
        return "MEDIUM"
    else:
        return "LOW"