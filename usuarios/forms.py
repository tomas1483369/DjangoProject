import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

from .validators import password_validator, username_validator


class UsuarioRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        label='Usuario',
        validators=[username_validator],
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': ' ',
                'autofocus': True,
                'autocomplete': 'username',
                'pattern': '^[A-Za-z0-9]+$',
                'title': 'Solo letras y números.',
                'inputmode': 'latin',
                'required': 'required',
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        label='Correo electrónico',
        validators=[EmailValidator('Ingrese un correo electrónico válido.')],
        widget=forms.EmailInput(
            attrs={
                'class': 'input',
                'placeholder': ' ',
                'autocomplete': 'email',
                'required': 'required',
            }
        ),
    )
    password1 = forms.CharField(
        label='Contraseña',
        strip=False,
        help_text='Mínimo 8 caracteres, incluyendo mayúscula, minúscula, número y carácter especial.',
        validators=[password_validator],
        widget=forms.PasswordInput(
            attrs={
                'class': 'input',
                'placeholder': ' ',
                'autocomplete': 'new-password',
                'pattern': '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*\\W).{8,}$',
                'title': 'Contraseña con 8+ caracteres, mayúscula, minúscula, número y carácter especial.',
                'required': 'required',
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
                'required': 'required',
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
            if not re.search(r'[A-Z]', password1):
                raise forms.ValidationError('La contraseña debe contener al menos una letra mayúscula.')
            if not re.search(r'[a-z]', password1):
                raise forms.ValidationError('La contraseña debe contener al menos una letra minúscula.')
            if not re.search(r'\d', password1):
                raise forms.ValidationError('La contraseña debe contener al menos un número.')
            if not re.search(r'\W', password1):
                raise forms.ValidationError('La contraseña debe contener al menos un carácter especial.')
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
        validators=[username_validator],
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': ' ',
                'autocomplete': 'username',
                'pattern': '^[A-Za-z0-9]+$',
                'title': 'Solo letras y números.',
                'inputmode': 'latin',
                'required': 'required',
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        label='Correo electrónico',
        validators=[EmailValidator('Ingrese un correo electrónico válido.')],
        widget=forms.EmailInput(
            attrs={
                'class': 'input',
                'placeholder': ' ',
                'autocomplete': 'email',
                'required': 'required',
                'inputmode': 'email',
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
