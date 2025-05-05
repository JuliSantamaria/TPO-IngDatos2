class Factura:
    def __init__(self,id_factura,id_pedido,nombre,apellido,direccion,importe,importe_total,productos=None,pago="No pagada"):
        self.id_factura=id_factura
        self.id_pedido=id_pedido
        self.nombre=nombre
        self.apellido=apellido
        self.direccion=direccion
        self.importe=importe
        self.importe_total=importe_total
        self.productos=productos or []
        self.pago=pago or []

    def agregar_producto(self,id_producto,cantidad,precio,descuento,precio_total,precio_final):
        self.productos.append({
            "id_producto": id_producto,
            "cantidad": cantidad,
            "precio":precio,
            "precio_total":precio_total,
            "descuento":descuento,
            "precio_final":precio_final
        })
    
    def agregar_pago(self,forma,monto,fecha,hora,operador):
        self.pago.append({
            "forma_de_pago":forma,
            "operador_interviniente":operador,
            "fecha":fecha,
            "hora":hora,
            "monto":monto
        })
        
    
    def set_importe(self,importe):
        self.importe=importe
    
    def set_importe_total(self,importe_total):
        self.importe_total=importe_total

    def to_dict(self):
        return{
            'id_factura':self.id_factura,
            'id_pedido':self.id_pedido,
            'nombre':self.nombre,
            'apellido':self.apellido,
            'direccion':self.direccion,
            'importe':self.importe,
            'importe_total':self.importe_total,
            'productos':self.productos,
            'pago':self.pago
        }