from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from .managers import ProductoManager
from .validators import validar_codigo_producto


nombre_validator = RegexValidator(
    r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$',
    'El nombre solo puede contener letras y espacios.',
)


class Producto(models.Model):
    nombre = models.CharField(
        max_length=120,
        validators=[nombre_validator],
    )
    codigo = models.CharField(
        max_length=20,
        unique=True,
        validators=[validar_codigo_producto],
    )
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    cantidad = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    stock_minimo = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    objects = ProductoManager()

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
