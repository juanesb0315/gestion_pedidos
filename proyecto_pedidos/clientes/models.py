from django.db import models


# modelo de cliente del sistema
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)

    class Meta:
        db_table = 'clientes'

    # nombre legible del cliente
    def __str__(self):
        return self.nombre