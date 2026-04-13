from django import forms
from django.utils import timezone
# Importamos las tablas de model 
from .models import Pedido, DetallePedido

# PEDIDO 
# formulario para crear y editar pedidos
class PedidoForm(forms.ModelForm):
    # define campos del formulario de pedido
    class Meta:
        model = Pedido
        fields = ['cliente', 'fecha', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    # evita fechas futuras en pedidos
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if not fecha:
            raise forms.ValidationError('La fecha es obligatoria.')
        if fecha > timezone.localdate():
            raise forms.ValidationError('La fecha no puede ser futura.')
        return fecha


# DETALLES   
# formulario para agregar productos al pedido
class DetallePedidoForm(forms.ModelForm):
    # recibe pedido actual para validar duplicados
    def __init__(self, *args, pedido=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.pedido_actual = pedido

    # define campos del formulario de detalle
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    # valida cantidad positiva
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0.')
        return cantidad

    # valida duplicados y disponibilidad de stock
    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')

        pedido = self.pedido_actual
        if pedido is None and self.instance and self.instance.pk:
            pedido = self.instance.pedido

        if not producto or not cantidad:
            return cleaned_data

        if pedido:
            consulta = DetallePedido.objects.filter(pedido=pedido, producto=producto)
            if self.instance and self.instance.pk:
                consulta = consulta.exclude(pk=self.instance.pk)
            if consulta.exists():
                raise forms.ValidationError('Este producto ya existe en el pedido.')

        stock_disponible = producto.stock
        if self.instance and self.instance.pk and self.instance.producto_id == producto.id:
            stock_disponible += self.instance.cantidad

        if cantidad > stock_disponible:
            raise forms.ValidationError(
                f'No hay stock suficiente para {producto.nombre}. Disponible: {stock_disponible}.'
            )

        return cleaned_data