import redis


# Función para obtener el cliente de Redis
def get_redis_client():
    return redis.Redis(
        host='localhost',port=6379,db=0
    )
