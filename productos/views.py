from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ProductoForm
from .models import Producto


def is_superuser(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_superuser, login_url='usuarios:login')
def crear_producto(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('productos:catalogo'))
    return render(request, 'producto_form.html', {'form': form, 'title': 'Crear producto'})


@user_passes_test(is_superuser, login_url='usuarios:login')
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('productos:catalogo'))
    return render(request, 'producto_form.html', {'form': form, 'title': 'Editar producto'})


@user_passes_test(is_superuser, login_url='usuarios:login')
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.estado = False
    producto.save(update_fields=['estado'])
    return redirect(reverse('productos:catalogo'))


def catalogo(request):
    products = Producto.objects.filter(estado=True).order_by('-fecha_creacion')
    return render(request, 'catalogo.html', {'products': products})
