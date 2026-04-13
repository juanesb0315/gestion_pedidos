from rest_framework.routers import DefaultRouter
from django.urls import path

from .api_views import (
    ClienteApiViewSet,
    ProductoApiViewSet,
    PedidoApiViewSet,
    DetallePedidoApiViewSet,
    obtener_token_api,
)

# router con slash opcional para clientes api
router = DefaultRouter(trailing_slash='/?')
router.register('clientes', ClienteApiViewSet, basename='api-clientes')
router.register('productos', ProductoApiViewSet, basename='api-productos')
router.register('pedidos', PedidoApiViewSet, basename='api-pedidos')
router.register('detalles', DetallePedidoApiViewSet, basename='api-detalles')

# rutas de token y recursos api
urlpatterns = [
    path('token/', obtener_token_api, name='api-token'),
]
urlpatterns += router.urls
