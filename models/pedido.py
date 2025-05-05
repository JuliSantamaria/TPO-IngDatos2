class Pedido:
    def __init__(self,id_pedido,nombre,apellido,aplicacion_descuento,productos=None):
        self.id_pedido=id_pedido
        self.nombre=nombre
        self.apellido=apellido
        self.aplicacion_descuento=aplicacion_descuento
        self.productos=productos or []
        
    def agregar_producto(self,id_producto,cantidad):
        self.productos.append({
            "id_producto": id_producto,
            "cantidad": cantidad
        })

    def to_dict(self):
        return{
            "id_pedido":self.id_pedido,
            "nombre":self.nombre,
            "apellido":self.apellido,
            "aplicacion_descuento":self.aplicacion_descuento,
            "productos":self.productos
        }
    