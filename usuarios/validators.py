from django.core.exceptions import ValidationError


def validar_nombre_usuario(value):
    if not isinstance(value, str) or not value.isalnum():
        raise ValidationError('El nombre de usuario solo puede contener letras y números.')
