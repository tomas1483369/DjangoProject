from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ProductoForm
from .models import Producto
from .services import ProductoService


def catalogo(request):
    products = Producto.objects.filter(estado=True).order_by('-fecha_creacion')
    return render(request, 'catalogo.html', {'products': products})


def crear_producto(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('productos:catalogo'))
    return render(request, 'producto_form.html', {'form': form, 'title': 'Crear producto'})


def editar_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('productos:catalogo'))
    return render(request, 'producto_form.html', {'form': form, 'title': 'Editar producto'})


def eliminar_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    producto.estado = False
    producto.save(update_fields=['estado'])
    return redirect(reverse('productos:catalogo'))
