from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from proyecto_pedidos.clientes.models import Cliente
from proyecto_pedidos.productos.models import Producto

from .models import Pedido, DetallePedido
from .serializers import (
    ClienteSerializer,
    ProductoSerializer,
    PedidoSerializer,
    DetallePedidoSerializer,
)
from .views.auth import create_jwt_token


@api_view(['POST'])
@permission_classes([AllowAny])
# endpoint para generar token jwt en api
def obtener_token_api(request):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '').strip()

    if not username or not password:
        return Response(
            {'detail': 'Debe enviar username y password.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request, username=username, password=password)
    if not user:
        return Response(
            {'detail': 'Credenciales invalidas.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = create_jwt_token(user)
    return Response({'token': token})


# viewset api de clientes
class ClienteApiViewSet(ModelViewSet):
    queryset = Cliente.objects.all().order_by('id')
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# viewset api de productos
class ProductoApiViewSet(ModelViewSet):
    queryset = Producto.objects.all().order_by('id')
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# viewset api de pedidos
class PedidoApiViewSet(ModelViewSet):
    queryset = Pedido.objects.all().order_by('id')
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# viewset api de detalles de pedido
class DetallePedidoApiViewSet(ModelViewSet):
    queryset = DetallePedido.objects.all().order_by('id')
    serializer_class = DetallePedidoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @transaction.atomic
    # devuelve stock al borrar un detalle
    def perform_destroy(self, instance):
        producto = instance.producto
        producto.stock += instance.cantidad
        producto.save(update_fields=['stock'])
        instance.delete()
