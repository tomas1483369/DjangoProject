from functools import wraps

from django.contrib.auth.decorators import user_passes_test


def group_required(group_names, login_url='usuarios:login'):
    if isinstance(group_names, str):
        group_names = [group_names]

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)

        def check(user):
            return (
                user.is_authenticated
                and user.groups.filter(name__in=group_names).exists()
            )

        return user_passes_test(check, login_url=login_url)(wrapper)

    return decorator


def admin_required(view_func):
    return group_required('Administrador')(view_func)


def employee_required(view_func):
    return group_required('Empleado')(view_func)
