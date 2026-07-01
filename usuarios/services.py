from django.contrib.auth.models import Group, Permission
from django.db import OperationalError, ProgrammingError


class AuthService:
    @staticmethod
    def create_default_roles():
        try:
            Permission.objects.exists()
        except (OperationalError, ProgrammingError):
            return

        administrator_perms = [
            'add_user',
            'change_user',
            'delete_user',
            'view_user',
            'view_producto',
            'add_producto',
            'change_producto',
            'delete_producto',
        ]

        employee_perms = [
            'view_producto',
        ]

        admin_group, _ = Group.objects.get_or_create(name='Administrador')
        empleado_group, _ = Group.objects.get_or_create(name='Empleado')

        admin_permissions = Permission.objects.filter(codename__in=administrator_perms)
        empleado_permissions = Permission.objects.filter(codename__in=employee_perms)

        admin_group.permissions.set(admin_permissions)
        empleado_group.permissions.set(empleado_permissions)

    @staticmethod
    def assign_default_role(user):
        try:
            empleado_group = Group.objects.get(name='Empleado')
        except Group.DoesNotExist:
            return

        user.groups.add(empleado_group)
        user.save(update_fields=['last_login'])
