from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .models import Producto

from .forms import FormularioProducto


# lista paginada de productos
class ListadoProductosVista(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'productos_app/listar.html'
    context_object_name = 'inventario_productos'
    paginate_by = 10
    ordering = ['id']


@login_required
# crea un nuevo producto
def registrar_producto(request):
    if request.method == 'POST':
        formulario_producto = FormularioProducto(request.POST)
        if formulario_producto.is_valid():
            formulario_producto.save()
            messages.success(request, 'Producto creado correctamente')
            return redirect('listar_productos')
    else:
        formulario_producto = FormularioProducto()
    return render(request, 'productos_app/crear.html', {'formulario_producto': formulario_producto})


@login_required
# edita un producto existente
def actualizar_producto(request, pk):
    registro_producto = get_object_or_404(Producto, pk=pk)
    formulario_producto = FormularioProducto(request.POST or None, instance=registro_producto)
    if formulario_producto.is_valid():
        formulario_producto.save()
        messages.success(request, 'Producto actualizado correctamente')
        return redirect('listar_productos')
    return render(request, 'productos_app/editar.html', {'formulario_producto': formulario_producto})


@login_required
# elimina producto sin detalle asociado
def borrar_producto(request, pk):
    registro_producto = get_object_or_404(Producto, pk=pk)
    if registro_producto.detallepedido_set.exists():
        messages.error(request, 'No puedes eliminar un producto que ya forma parte de un pedido registrado')
        return redirect('listar_productos')
    registro_producto.delete()
    messages.success(request, 'Producto eliminado correctamente del sistema')
    return redirect('listar_productos')


@login_required
# muestra detalle de un producto
def ver_producto(request, pk):
    registro_producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos_app/detalle.html', {'registro_producto': registro_producto})
