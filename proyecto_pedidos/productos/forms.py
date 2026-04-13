from django import forms

from .models import Producto


# formulario para validar datos de producto
class FormularioProducto(forms.ModelForm):
    # configuracion del modelo y campos del formulario
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    # valida nombre unico del producto
    def clean_nombre(self):
        nombre_limpio = self.cleaned_data.get('nombre', '').strip()
        if not nombre_limpio:
            raise forms.ValidationError('El nombre es obligatorio.')
        if len(nombre_limpio) < 2:
            raise forms.ValidationError('El nombre debe tener al menos 2 caracteres.')
        if not nombre_limpio[0].isalpha():
            raise forms.ValidationError('El nombre debe comenzar con una letra.')

        consulta = Producto.objects.filter(nombre__iexact=nombre_limpio)
        if self.instance and self.instance.pk:
            consulta = consulta.exclude(pk=self.instance.pk)
        if consulta.exists():
            raise forms.ValidationError('Ya existe un producto con este nombre.')
        return nombre_limpio

    # valida precio mayor a cero
    def clean_precio(self):
        precio_limpio = self.cleaned_data.get('precio')
        if precio_limpio is None:
            raise forms.ValidationError('El precio es obligatorio.')
        if precio_limpio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0.')
        return precio_limpio

    # valida stock en rango permitido
    def clean_stock(self):
        stock_limpio = self.cleaned_data.get('stock')
        if stock_limpio is None:
            raise forms.ValidationError('El stock es obligatorio.')
        if stock_limpio < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        if stock_limpio > 1000000:
            raise forms.ValidationError('El stock es demasiado alto.')
        return stock_limpio
