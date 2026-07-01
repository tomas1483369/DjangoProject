def user_roles(request):
    user = request.user
    if not user.is_authenticated:
        return {}

    return {
        'is_admin': user.groups.filter(name='Administrador').exists(),
        'is_employee': user.groups.filter(name='Empleado').exists(),
    }
