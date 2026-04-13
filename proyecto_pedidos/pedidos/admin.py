from django.contrib import admin

from .models import Pedido, DetallePedido

# registra pedido en panel admin
admin.site.register(Pedido)
# registra detalle de pedido en panel admin
admin.site.register(DetallePedido)