from django import forms
import re

from .models import Cliente


# formulario para validar datos de cliente
class FormularioCliente(forms.ModelForm):
    # configuracion del modelo y campos del formulario
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # valida nombre del cliente
    def clean_nombre(self):
        nombre_limpio = self.cleaned_data.get('nombre', '').strip()
        if not nombre_limpio:
            raise forms.ValidationError('El nombre es obligatorio.')
        if len(nombre_limpio) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
        if not nombre_limpio[0].isalpha():
            raise forms.ValidationError('El nombre debe comenzar con una letra.')
        if not re.fullmatch(r'[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+', nombre_limpio):
            raise forms.ValidationError('El nombre solo puede contener letras y espacios.')
        return nombre_limpio

    # valida correo unico del cliente
    def clean_correo(self):
        correo_limpio = self.cleaned_data.get('correo', '').strip().lower()
        if not correo_limpio:
            raise forms.ValidationError('El correo es obligatorio.')

        consulta = Cliente.objects.filter(correo__iexact=correo_limpio)
        if self.instance and self.instance.pk:
            consulta = consulta.exclude(pk=self.instance.pk)
        if consulta.exists():
            raise forms.ValidationError('Ya existe un cliente con este correo.')
        return correo_limpio

    # valida direccion minima
    def clean_direccion(self):
        direccion_limpia = self.cleaned_data.get('direccion', '').strip()
        if not direccion_limpia:
            raise forms.ValidationError('La direccion es obligatoria.')
        if len(direccion_limpia) < 5:
            raise forms.ValidationError('La direccion debe tener al menos 5 caracteres.')
        return direccion_limpia

    # valida telefono con formato flexible
    def clean_telefono(self):
        telefono_limpio = self.cleaned_data.get('telefono', '').strip()
        if not telefono_limpio:
            raise forms.ValidationError('El telefono es obligatorio.')

        # Permite formatos comunes: +57 300-123-4567, (300) 123 4567, etc.
        if not re.fullmatch(r'[\d\s\-\(\)\+]+', telefono_limpio):
            raise forms.ValidationError('Telefono invalido. Usa solo numeros y signos como +, -, espacios o parentesis.')

        telefono_normalizado = re.sub(r'[^\d+]', '', telefono_limpio)
        if telefono_normalizado.startswith('+'):
            solo_digitos = telefono_normalizado[1:]
        else:
            solo_digitos = telefono_normalizado

        if not solo_digitos.isdigit() or len(solo_digitos) < 7:
            raise forms.ValidationError('Telefono invalido. Debe tener al menos 7 digitos.')

        if len(solo_digitos) > 15:
            raise forms.ValidationError('Telefono invalido. Maximo 15 digitos.')

        return telefono_normalizado
