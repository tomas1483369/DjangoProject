from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class UsuarioPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = 'usuarios:login'
    raise_exception = False


class AdminPermissionMixin(UsuarioPermissionMixin):
    permission_required = (
        'auth.add_user',
        'auth.change_user',
        'auth.delete_user',
    )


class ProductoPermissionMixin(UsuarioPermissionMixin):
    permission_required = (
        'productos.add_producto',
        'productos.change_producto',
        'productos.delete_producto',
    )
