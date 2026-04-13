from django.urls import path

from . import views

# rutas de productos
urlpatterns = [
    path('productos/', views.ListadoProductosVista.as_view(), name='listar_productos'),
    path('productos/ver/<int:pk>/', views.ver_producto, name='ver_producto'),
    path('productos/crear/', views.registrar_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.actualizar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.borrar_producto, name='eliminar_producto'),
]
