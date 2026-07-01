import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


username_validator = RegexValidator(
    r'^[A-Za-z0-9]+$',
    'El usuario solo puede contener letras y números.',
)

password_validator = RegexValidator(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$',
    'La contraseña debe tener mínimo 8 caracteres e incluir mayúscula, minúscula, número y carácter especial.',
)

product_name_validator = RegexValidator(
    r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$',
    'El nombre solo puede contener letras y espacios.',
)

product_code_validator = RegexValidator(
    r'^PROD-\d{4}$',
    'El código del producto debe tener el formato PROD-0001.',
)


def validar_codigo_producto(value):
    pattern = re.compile(r'^PROD-\d{4}$')
    if not pattern.match(str(value)):
        raise ValidationError('El código del producto debe tener el formato PROD-0001.')
