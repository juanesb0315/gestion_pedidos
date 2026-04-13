from django.urls import path

from . import views

# rutas de clientes
urlpatterns = [
    path('clientes/', views.ListadoClientesVista.as_view(), name='listar_clientes'),
    path('clientes/ver/<int:pk>/', views.ver_cliente, name='ver_cliente'),
    path('clientes/crear/', views.registrar_cliente, name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.actualizar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.borrar_cliente, name='eliminar_cliente'),
]
