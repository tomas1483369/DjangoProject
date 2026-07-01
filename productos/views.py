from django.contrib import messages
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from usuarios.decorators import admin_required

from .forms import ProductoForm
from .models import Producto


def is_superuser(user):
    return user.is_authenticated and user.is_superuser


def superuser_required(view_func):
    return user_passes_test(is_superuser, login_url='usuarios:login')(view_func)


@admin_required
def crear_producto(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto creado correctamente.')
        return redirect(reverse('productos:catalogo'))
    return render(request, 'producto_form.html', {'form': form, 'title': 'Crear producto'})


@admin_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto actualizado correctamente.')
        return redirect(reverse('productos:catalogo'))
    return render(request, 'producto_form.html', {'form': form, 'title': 'Editar producto'})


@admin_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.estado = False
    producto.save(update_fields=['estado'])
    messages.success(request, 'Producto eliminado del catálogo.')
    return redirect(reverse('productos:catalogo'))


def _get_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def carrito(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        product_id = str(request.POST.get('product_id', ''))
        cart = _get_cart(request)
        if action == 'remove' and product_id:
            cart.pop(product_id, None)
            _save_cart(request, cart)
            messages.success(request, 'Producto eliminado del carrito.')
        elif action == 'clear':
            request.session['cart'] = {}
            request.session.modified = True
            messages.success(request, 'Carrito vaciado correctamente.')
        return redirect(reverse('productos:carrito'))

    cart = _get_cart(request)
    product_ids = [int(pid) for pid in cart.keys() if pid.isdigit()]
    products = Producto.objects.filter(pk__in=product_ids)
    items = []
    total_amount = 0
    total_quantity = 0

    for product in products:
        quantity = cart.get(str(product.pk), 0)
        subtotal = product.precio * quantity
        total_amount += subtotal
        total_quantity += quantity
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'productos/carrito.html', {
        'items': items,
        'total_amount': total_amount,
        'total_quantity': total_quantity,
    })


def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk, estado=True)

    if request.method == 'POST':
        cantidad = request.POST.get('cantidad', '1')
        try:
            cantidad = int(cantidad)
        except ValueError:
            cantidad = 1

        if cantidad < 1:
            messages.error(request, 'Debe seleccionar una cantidad válida.')
        elif cantidad > producto.cantidad:
            messages.error(request, 'No hay suficiente stock disponible.')
        else:
            cart = _get_cart(request)
            product_key = str(producto.pk)
            cart[product_key] = min(cart.get(product_key, 0) + cantidad, producto.cantidad)
            _save_cart(request, cart)
            messages.success(request, f'{producto.nombre} agregado al carrito.')
            return redirect(reverse('productos:carrito'))

    return render(request, 'productos/producto_detalle.html', {'product': producto})


def catalogo(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', 'all')
    products = Producto.objects.activos().order_by('-fecha_creacion')
    if query:
        products = products.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query)
        )

    if status == 'available':
        products = products.filter(cantidad__gt=F('stock_minimo'))
    elif status == 'low_stock':
        products = products.filter(cantidad__lte=F('stock_minimo'), cantidad__gt=0)
    elif status == 'out_of_stock':
        products = products.filter(cantidad=0)

    return render(request, 'catalogo.html', {
        'products': products,
        'query': query,
        'status': status,
    })
