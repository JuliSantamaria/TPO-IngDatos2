class Producto:
    def __init__(self,id_producto,nombre,descripcion,precio,stock,foto_url=None,comentarios=None,video_url=None,descuento=0):
        self.id_producto=id_producto
        self.nombre=nombre
        self.descripcion=descripcion
        self.precio=precio
        self.stock=stock
        self.descuento=descuento
        self.foto_url=foto_url
        self.comentarios=comentarios if comentarios is not None else []
        self.video_url=video_url
    
    def to_dict(self):
        return{
            "id_producto":self.id_producto,
            "nombre":self.nombre,
            "descripcion":self.descripcion,
            "precio":self.precio,
            "stock":self.stock,
            "descuento":self.descuento,
            "foto_url":self.foto_url,
            "comentarios":self.comentarios,
            "video_url":self.video_url
        }
    
