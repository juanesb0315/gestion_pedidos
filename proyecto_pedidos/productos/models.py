from django.db import models


# modelo de producto del inventario
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField()

    class Meta:
        db_table = 'productos'

    # nombre legible del producto
    def __str__(self):
        return self.nombre