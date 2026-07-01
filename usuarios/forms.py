import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UsuarioRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        label='Usuario',
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9]+$',
                'El usuario solo puede contener letras y números.',
            )
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': ' ',
                'autofocus': True,
                'autocomplete': 'username',
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        label='Correo electrónico',
        widget=forms.EmailInput(
            attrs={
                'class': 'input',
                'placeholder': ' ',
                'autocomplete': 'email',
            }
        ),
    )
    password1 = forms.CharField(
        label='Contraseña',
        strip=False,
        help_text='Mínimo 8 caracteres, al menos una letra y un número.',
        widget=forms.PasswordInput(
            attrs={
                'class': 'input',
                'placeholder': ' ',
                'autocomplete': 'new-password',
            }
        ),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input',
                'placeholder': ' ',
                'autocomplete': 'new-password',
            }
        ),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            if len(password1) < 8:
                raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
            if not re.search(r'[A-Za-z]', password1) or not re.search(r'\d', password1):
                raise forms.ValidationError('La contraseña debe incluir letras y números.')
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = True
        if commit:
            user.save()
        return user


class UsuarioUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        label='Usuario',
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': ' ',
                'autocomplete': 'username',
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        label='Correo electrónico',
        widget=forms.EmailInput(
            attrs={
                'class': 'input',
                'placeholder': ' ',
                'autocomplete': 'email',
            }
        ),
    )
    is_active = forms.BooleanField(
        required=False,
        label='Activo',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        ),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'is_active')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email
