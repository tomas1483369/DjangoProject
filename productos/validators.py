import re

from django.core.exceptions import ValidationError

PRODUCT_CODE_PATTERN = re.compile(r'^PROD-\d{4}$')


def validar_codigo_producto(value):
    if not PRODUCT_CODE_PATTERN.match(str(value)):
        raise ValidationError('El código del producto debe tener el formato PROD-0001.')
