from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
import re

from proyecto_pedidos.clientes.models import Cliente
from proyecto_pedidos.productos.models import Producto

from .models import Pedido, DetallePedido


# serializer de cliente para la api
class ClienteSerializer(serializers.ModelSerializer):
    # valida nombre de cliente
    def validate_nombre(self, value):
        nombre = value.strip()
        if len(nombre) < 3:
            raise serializers.ValidationError('El nombre debe tener al menos 3 caracteres.')
        if not re.fullmatch(r'[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+', nombre):
            raise serializers.ValidationError('El nombre solo puede contener letras y espacios.')
        return nombre

    # valida correo unico en clientes
    def validate_correo(self, value):
        correo = value.strip().lower()
        consulta = Cliente.objects.filter(correo__iexact=correo)
        if self.instance:
            consulta = consulta.exclude(pk=self.instance.pk)
        if consulta.exists():
            raise serializers.ValidationError('Ya existe un cliente con este correo.')
        return correo

    # valida direccion minima
    def validate_direccion(self, value):
        direccion = value.strip()
        if len(direccion) < 5:
            raise serializers.ValidationError('La direccion debe tener al menos 5 caracteres.')
        return direccion

    # valida telefono y normaliza formato
    def validate_telefono(self, value):
        telefono = value.strip()
        if not re.fullmatch(r'[\d\s\-\(\)\+]+', telefono):
            raise serializers.ValidationError('Telefono invalido. Usa solo numeros y signos permitidos.')
        normalizado = re.sub(r'[^\d+]', '', telefono)
        digitos = normalizado[1:] if normalizado.startswith('+') else normalizado
        if not digitos.isdigit() or len(digitos) < 7 or len(digitos) > 15:
            raise serializers.ValidationError('Telefono invalido. Debe tener entre 7 y 15 digitos.')
        return normalizado

    # campos expuestos de cliente
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'correo', 'direccion', 'telefono']


# serializer de producto para la api
class ProductoSerializer(serializers.ModelSerializer):
    # valida nombre unico de producto
    def validate_nombre(self, value):
        nombre = value.strip()
        consulta = Producto.objects.filter(nombre__iexact=nombre)
        if self.instance:
            consulta = consulta.exclude(pk=self.instance.pk)
        if consulta.exists():
            raise serializers.ValidationError('Ya existe un producto con este nombre.')
        return nombre

    # valida precio mayor a cero
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio debe ser mayor a 0.')
        return value

    # valida rango de stock
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('El stock no puede ser negativo.')
        if value > 1000000:
            raise serializers.ValidationError('El stock es demasiado alto.')
        return value

    # campos expuestos de producto
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock']


# serializer de pedido para la api
class PedidoSerializer(serializers.ModelSerializer):
    # valida fecha no futura
    def validate_fecha(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError('La fecha no puede ser futura.')
        return value

    # campos expuestos de pedido
    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'fecha', 'estado']


# serializer de detalle para la api
class DetallePedidoSerializer(serializers.ModelSerializer):
    # valida reglas de negocio del detalle
    def validate(self, attrs):
        pedido = attrs.get('pedido', self.instance.pedido if self.instance else None)
        producto = attrs.get('producto', self.instance.producto if self.instance else None)
        cantidad = attrs.get('cantidad', self.instance.cantidad if self.instance else None)

        if not pedido or not producto or not cantidad:
            return attrs

        if cantidad <= 0:
            raise serializers.ValidationError({'cantidad': 'La cantidad debe ser mayor a 0.'})

        consulta = DetallePedido.objects.filter(pedido=pedido, producto=producto)
        if self.instance:
            consulta = consulta.exclude(pk=self.instance.pk)
        if consulta.exists():
            raise serializers.ValidationError('Este producto ya existe en el pedido.')

        stock_disponible = producto.stock
        if self.instance and self.instance.producto_id == producto.id:
            stock_disponible += self.instance.cantidad

        if cantidad > stock_disponible:
            raise serializers.ValidationError(
                {'cantidad': f'Stock insuficiente. Disponible: {stock_disponible}.'}
            )

        return attrs

    @transaction.atomic
    # descuenta stock al crear detalle
    def create(self, validated_data):
        producto = validated_data['producto']
        cantidad = validated_data['cantidad']
        producto.stock -= cantidad
        producto.save(update_fields=['stock'])
        return super().create(validated_data)

    @transaction.atomic
    # ajusta stock al actualizar detalle
    def update(self, instance, validated_data):
        producto_nuevo = validated_data.get('producto', instance.producto)
        cantidad_nueva = validated_data.get('cantidad', instance.cantidad)
        producto_anterior = instance.producto
        cantidad_anterior = instance.cantidad

        if producto_anterior.id == producto_nuevo.id:
            diferencia = cantidad_nueva - cantidad_anterior
            producto_nuevo.stock -= diferencia
            producto_nuevo.save(update_fields=['stock'])
        else:
            producto_anterior.stock += cantidad_anterior
            producto_anterior.save(update_fields=['stock'])
            producto_nuevo.stock -= cantidad_nueva
            producto_nuevo.save(update_fields=['stock'])

        return super().update(instance, validated_data)

    # campos expuestos de detalle
    class Meta:
        model = DetallePedido
        fields = ['id', 'pedido', 'producto', 'cantidad', 'subtotal']
        read_only_fields = ['subtotal']
