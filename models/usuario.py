class Usuario:
    def __init__(self,nombre,apellido,documento,contraseña,direccion,categoria="LOW",cuenta_corriente=0,facturas_pagadas=None,facturas_a_pagar=None,historial_ordenes=None):
        self.nombre=nombre
        self.apellido=apellido
        self.documento=documento
        self.contraseña=contraseña
        self.direccion=direccion
        self.categoria=categoria
        self.cuenta_corriente=cuenta_corriente
        self.facturas_pagadas=facturas_pagadas if facturas_pagadas is not None else []
        self.facturas_a_pagar=facturas_a_pagar if facturas_a_pagar is not None else []
        self.historial_ordenes=historial_ordenes if historial_ordenes is not None else []

    def to_dict(self):
        return{
            "nombre":self.nombre,
            "apellido":self.apellido,
            "documento":self.documento,
            "contraseña":self.contraseña,
            "direccion":self.direccion,
            "categoria":self.categoria,
            "cuenta_corriente":self.cuenta_corriente,
            "facturas_pagadas":self.facturas_pagadas,
            "facturas_a_pagar":self.facturas_a_pagar,
            "historial_ordenes":self.historial_ordenes
        }
    