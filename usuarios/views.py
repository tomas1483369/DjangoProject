from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from productos.models import Producto
from .decorators import admin_required
from .forms import UsuarioRegisterForm, UsuarioUpdateForm
from .services import AuthService


@login_required(login_url='usuarios:login')
def dashboard(request):
    total_users = User.objects.count()
    total_products = Producto.objects.activos().count()
    low_stock_products = Producto.objects.bajo_stock().count()
    out_of_stock_products = Producto.objects.agotados().count()
    latest_products = Producto.objects.activos().order_by('-fecha_creacion')[:4]
    latest_users = User.objects.order_by('-date_joined')[:5]

    return render(request, 'dashboard.html', {
        'total_users': total_users,
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'latest_products': latest_products,
        'latest_users': latest_users,
    })


def is_superuser(user):
    return user.is_authenticated and user.is_superuser


def superuser_required(view_func):
    return user_passes_test(is_superuser, login_url='usuarios:login')(view_func)


@login_required(login_url='usuarios:login')
def lista_usuarios(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', 'all')
    users = User.objects.order_by('username')
    if query:
        users = users.filter(Q(username__icontains=query) | Q(email__icontains=query))
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)
    return render(request, 'usuarios/lista_usuarios.html', {
        'users': users,
        'query': query,
        'status': status,
    })


class UsuarioLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f'Bienvenido de nuevo, {self.request.user.username}!')
        return super().form_valid(form)


@admin_required
def crear_usuario(request):
    form = UsuarioRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Usuario creado correctamente.')
        return redirect(reverse('usuarios:lista_usuarios'))
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'title': 'Crear usuario'})


@admin_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    form = UsuarioUpdateForm(request.POST or None, instance=usuario)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Usuario actualizado correctamente.')
        return redirect(reverse('usuarios:lista_usuarios'))
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'title': 'Editar usuario'})


@admin_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if usuario != request.user:
        usuario.is_active = False
        usuario.save(update_fields=['is_active'])
        messages.success(request, 'Usuario desactivado correctamente.')
    else:
        messages.error(request, 'No puedes desactivar tu propia cuenta.')
    return redirect(reverse('usuarios:lista_usuarios'))


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('productos:catalogo'))

    form = UsuarioRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        AuthService.assign_default_role(user)
        messages.success(request, 'Cuenta creada. Inicia sesión para continuar.')
        return redirect(reverse('usuarios:login'))

    return render(request, 'registration/register.html', {'form': form})
