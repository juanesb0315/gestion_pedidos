from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .models import Cliente

from .forms import FormularioCliente


# lista paginada de clientes
class ListadoClientesVista(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes_app/listar.html'
    context_object_name = 'registros_clientes'
    paginate_by = 10
    ordering = ['id']


@login_required
# crea un nuevo cliente
def registrar_cliente(request):
    if request.method == 'POST':
        formulario_cliente = FormularioCliente(request.POST)
        if formulario_cliente.is_valid():
            formulario_cliente.save()
            messages.success(request, 'Cliente creado correctamente')
            return redirect('listar_clientes')
    else:
        formulario_cliente = FormularioCliente()
    return render(request, 'clientes_app/crear.html', {'formulario_cliente': formulario_cliente})


@login_required
# edita un cliente existente
def actualizar_cliente(request, pk):
    registro_cliente = get_object_or_404(Cliente, pk=pk)
    formulario_cliente = FormularioCliente(request.POST or None, instance=registro_cliente)
    if formulario_cliente.is_valid():
        formulario_cliente.save()
        messages.success(request, 'Cliente actualizado correctamente')
        return redirect('listar_clientes')
    return render(request, 'clientes_app/editar.html', {'formulario_cliente': formulario_cliente})


@login_required
# elimina cliente sin pedidos asociados
def borrar_cliente(request, pk):
    registro_cliente = get_object_or_404(Cliente, pk=pk)
    if registro_cliente.pedido_set.exists():
        messages.error(request, 'No puedes eliminar este cliente porque tiene pedidos asociados')
        return redirect('listar_clientes')
    registro_cliente.delete()
    messages.success(request, 'Cliente eliminado correctamente')
    return redirect('listar_clientes')


@login_required
# muestra detalle de un cliente
def ver_cliente(request, pk):
    registro_cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'clientes_app/detalle.html', {'registro_cliente': registro_cliente})
