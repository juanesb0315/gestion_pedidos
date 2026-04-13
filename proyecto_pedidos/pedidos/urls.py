from django.urls import path
from . import views
from . import reportes

# rutas principales de pedidos detalles y reportes
urlpatterns = [
    # página raíz ajustada para forzar login si no hay sesión activa
    path('', views.home_view, name='home'),
    path('listar/', views.PedidoListView.as_view(), name='listar'),
    path('crear/', views.crear_pedido, name='crear'),
    path('editar/<int:pk>/', views.editar_pedido, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_pedido, name='eliminar'),
    path('detalle/<int:pk>/', views.detalle_pedido, name='detalle'),
    
    # LOGIN
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.register_view, name='register'),
    
    # Detalle
    path('detalles/', views.DetallePedidoListView.as_view(), name='listar_detalles'),
    path('detalle-producto/<int:pk>/', views.ver_detalle_producto, name='ver_detalle_producto'),
    path('pedido/<int:pedido_id>/agregar/', views.agregar_detalle, name='agregar_detalle'),
    path('detalle/editar/<int:pk>/', views.editar_detalle, name='editar_detalle'),
    path('detalle/eliminar/<int:pk>/', views.eliminar_detalle, name='eliminar_detalle'),
    
    # Reportes 
    path('exportar/detalles/pdf/', reportes.exportar_detalles_pdf),
    path('exportar/detalles/excel/', reportes.exportar_detalles_excel),
    path('exportar/pedidos/pdf/', reportes.exportar_pedidos_pdf),
    path('exportar/pedidos/excel/', reportes.exportar_pedidos_excel),
    path('exportar/clientes/pdf/', reportes.exportar_clientes_pdf),
    path('exportar/clientes/excel/', reportes.exportar_clientes_excel),
    path('exportar/productos/pdf/', reportes.exportar_productos_pdf),
    path('exportar/productos/excel/', reportes.exportar_productos_excel),
    path('exportar/todo/excel/', reportes.exportar_todo_excel),
]