from .auth import login_view, logout_view, register_view, home_view
from .pedidos import PedidoListView, crear_pedido, editar_pedido, eliminar_pedido, detalle_pedido
from .detalles import DetallePedidoListView, agregar_detalle, editar_detalle, eliminar_detalle, ver_detalle_producto

# exporta vistas usadas por urls de pedidos
__all__ = [
    'login_view', 'logout_view', 'register_view', 'home_view',
    'PedidoListView', 'crear_pedido', 'editar_pedido', 'eliminar_pedido', 'detalle_pedido',
    'DetallePedidoListView', 'agregar_detalle', 'editar_detalle', 'eliminar_detalle', 'ver_detalle_producto',
]
