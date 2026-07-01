from django import forms
from django.core.validators import RegexValidator

from .models import Producto


class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre',
        max_length=120,
        validators=[
            RegexValidator(
                r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$',
                'El nombre solo puede contener letras y espacios.',
            )
        ],
    )

    codigo = forms.CharField(
        label='Código',
        max_length=20,
        validators=[
            RegexValidator(
                r'^PROD-\d{4}$',
                'El código debe tener formato PROD-0001.',
            )
        ],
    )

    class Meta:
        model = Producto
        fields = [
            'nombre',
            'codigo',
            'imagen',
            'descripcion',
            'precio',
            'cantidad',
            'stock_minimo',
            'estado',
        ]
        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control bg-secondary text-white border-secondary'}
            ),
            'codigo': forms.TextInput(
                attrs={'class': 'form-control bg-secondary text-white border-secondary'}
            ),
            'imagen': forms.FileInput(
                attrs={'class': 'form-control bg-secondary text-white border-secondary'}
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control bg-secondary text-white border-secondary',
                    'rows': 4,
                }
            ),
            'precio': forms.NumberInput(
                attrs={'class': 'form-control bg-secondary text-white border-secondary', 'step': '0.01'}
            ),
            'cantidad': forms.NumberInput(
                attrs={'class': 'form-control bg-secondary text-white border-secondary'}
            ),
            'stock_minimo': forms.NumberInput(
                attrs={'class': 'form-control bg-secondary text-white border-secondary'}
            ),
            'estado': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            content_type = imagen.content_type
            if content_type not in ('image/jpeg', 'image/png'):
                raise forms.ValidationError('La imagen debe ser JPEG o PNG.')
            if imagen.size > 2 * 1024 * 1024:
                raise forms.ValidationError('La imagen no puede superar los 2 MB.')
        return imagen

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError('El precio debe ser un valor positivo.')
        return precio

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is None or cantidad < 0:
            raise forms.ValidationError('La cantidad debe ser un número entero positivo.')
        return cantidad

    def clean_stock_minimo(self):
        stock_minimo = self.cleaned_data.get('stock_minimo')
        if stock_minimo is None or stock_minimo < 0:
            raise forms.ValidationError('El stock mínimo debe ser un número entero positivo.')
        return stock_minimo
