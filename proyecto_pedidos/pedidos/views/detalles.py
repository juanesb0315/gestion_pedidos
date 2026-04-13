from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView

from proyecto_pedidos.pedidos.models import Pedido, DetallePedido
from proyecto_pedidos.productos.models import Producto
from proyecto_pedidos.pedidos.forms import DetallePedidoForm


# lista paginada de detalles de pedido
class DetallePedidoListView(LoginRequiredMixin, ListView):
    model = DetallePedido
    template_name = 'detalles/listar_detalles.html'
    context_object_name = 'detalles'
    paginate_by = 10
    ordering = ['id']


@login_required
# agrega un producto dentro de un pedido
def agregar_detalle(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        form = DetallePedidoForm(request.POST, pedido=pedido)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.pedido = pedido
            producto = detalle.producto
            cantidad = detalle.cantidad
            if cantidad > producto.stock:
                messages.error(request, f'No puedes agregar {cantidad}. Solo quedan {producto.stock} unidades en stock.')
                return redirect('detalle', pk=pedido.id)
            producto.stock -= cantidad
            producto.save()
            detalle.save()
            messages.success(request, 'Producto agregado al pedido')
            return redirect('detalle', pk=pedido.id)
    else:
        form = DetallePedidoForm(pedido=pedido)
    return render(request, 'detalles/agregar_detalle.html', {'form': form, 'pedido': pedido})

@login_required
# edita cantidad y ajusta stock
def editar_detalle(request, pk):
    detalle = get_object_or_404(DetallePedido, pk=pk)
    producto = detalle.producto
    cantidad_anterior = detalle.cantidad
    form = DetallePedidoForm(request.POST or None, instance=detalle, pedido=detalle.pedido)
    if form.is_valid():
        detalle_editado = form.save(commit=False)
        nueva_cantidad = detalle_editado.cantidad
        producto.stock += cantidad_anterior
        if nueva_cantidad > producto.stock:
            messages.error(request, f'Cantidad máxima disponible: {producto.stock}')
            return redirect('detalle', pk=detalle.pedido.id)
        producto.stock -= nueva_cantidad
        producto.save()
        detalle_editado.save()
        messages.success(request, 'Producto actualizado correctamente')
        return redirect('detalle', pk=detalle.pedido.id)
    return render(request, 'detalles/editar_detalle.html', {'form': form})

@login_required
# elimina detalle y devuelve stock
def eliminar_detalle(request, pk):
    detalle = get_object_or_404(DetallePedido, pk=pk)
    producto = detalle.producto
    cantidad_a_devolver = detalle.cantidad
    pedido_id = detalle.pedido.id
    producto.stock += cantidad_a_devolver
    producto.save()
    detalle.delete()
    messages.success(request, 'Producto eliminado correctamente')
    return redirect('detalle', pk=pedido_id)


@login_required
# muestra detalle individual de producto en pedido
def ver_detalle_producto(request, pk):
    detalle = get_object_or_404(DetallePedido, pk=pk)
    return render(request, 'detalles/detalle_producto.html', {'detalle': detalle})
