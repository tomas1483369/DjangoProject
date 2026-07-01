from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from productos.models import Producto

from .forms import UsuarioRegisterForm


@login_required(login_url='usuarios:login')
def dashboard(request):
    total_products = Producto.objects.activos().count()
    low_stock_products = Producto.objects.bajo_stock().count()
    out_of_stock_products = Producto.objects.agotados().count()
    featured_products = Producto.objects.activos().order_by('-fecha_creacion')[:3]
    return render(request, 'dashboard.html', {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'featured_products': featured_products,
    })


@login_required(login_url='usuarios:login')
def lista_usuarios(request):
    users = User.objects.filter(is_active=True).order_by('username')
    return render(request, 'usuarios/lista_usuarios.html', {'users': users})


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('productos:catalogo'))

    form = UsuarioRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cuenta creada. Inicia sesión para continuar.')
        return redirect(reverse('usuarios:login'))

    return render(request, 'registration/register.html', {'form': form})


def is_superuser(user):
    return user.is_authenticated and user.is_superuser


def superuser_required(view_func):
    return user_passes_test(is_superuser, login_url='usuarios:login')(view_func)
