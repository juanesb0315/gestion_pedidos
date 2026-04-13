from django.db import models
from proyecto_pedidos.clientes.models import Cliente
from proyecto_pedidos.productos.models import Producto

# Pedidos
# modelo principal de pedido
class Pedido(models.Model):
    ESTADOS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='pendiente')

    class Meta:
        db_table = 'pedidos'
        
    # nombre legible del pedido
    def __str__(self):
        return f"Pedido {self.id} - {self.cliente}"
    
# Detalles 
# modelo de productos dentro del pedido
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=True)

    class Meta:
        db_table = 'detalles_pedido'
        
    # calcula subtotal antes de guardar
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.producto.precio
        super().save(*args, **kwargs)

    # nombre legible del detalle
    def __str__(self):
        return f"{self.producto} x {self.cantidad}"