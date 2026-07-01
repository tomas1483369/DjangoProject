from django.core.exceptions import ValidationError


def validar_codigo_producto(value):
    if not isinstance(value, str) or not value.startswith('PROD-'):
        raise ValidationError('El código del producto debe tener el formato PROD-0001.')
