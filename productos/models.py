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
    categoria = models.CharField(
        max_length=80,
        blank=True,
        default='General',
        verbose_name='Categoría',
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

    @property
    def is_out_of_stock(self):
        return self.cantidad == 0

    @property
    def is_low_stock(self):
        return self.cantidad > 0 and self.cantidad <= self.stock_minimo

    @property
    def stock_status(self):
        if self.is_out_of_stock:
            return 'out_of_stock'
        if self.is_low_stock:
            return 'low_stock'
        return 'available'

    @property
    def stock_badge(self):
        if self.is_out_of_stock:
            return 'Agotado'
        if self.is_low_stock:
            return 'Bajo stock'
        return 'Disponible'

    @property
    def stock_badge_class(self):
        if self.is_out_of_stock:
            return 'badge bg-danger'
        if self.is_low_stock:
            return 'badge bg-warning text-dark'
        return 'badge bg-success'
