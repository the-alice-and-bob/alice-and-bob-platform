class UserGroups:
    RRSS = 'rrss'
    MANAGER = 'manager'
    PLATFORM_ADMIN = 'platform_admin'


class SuperUserOnlyMixin:
    """
    Mixin para restringir el acceso en el Django Admin a usuarios con permisos específicos.
    """

    def has_module_permission(self, request):
        """
        Controla si el usuario tiene acceso al módulo (app) en el Django Admin.
        """
        return request.user.is_superuser or request.user.groups.filter(name=UserGroups.PLATFORM_ADMIN).exists()

    def has_view_permission(self, request, obj=None):
        """
        Controla si el usuario puede ver los objetos en este modelo.
        """
        return request.user.is_superuser or request.user.groups.filter(name=UserGroups.PLATFORM_ADMIN).exists()

    def has_add_permission(self, request):
        """
        Controla si el usuario puede añadir objetos en este modelo.
        """
        return request.user.is_superuser or request.user.groups.filter(name=UserGroups.PLATFORM_ADMIN).exists()

    def has_change_permission(self, request, obj=None):
        """
        Controla si el usuario puede cambiar objetos en este modelo.
        """
        return request.user.is_superuser or request.user.groups.filter(name=UserGroups.PLATFORM_ADMIN).exists()

    def has_delete_permission(self, request, obj=None):
        """
        Controla si el usuario puede eliminar objetos en este modelo.
        """
        return request.user.is_superuser or request.user.groups.filter(name=UserGroups.PLATFORM_ADMIN).exists()


class ManagersOnlyMixin:
    """
    Mixin para restringir el acceso en el Django Admin a usuarios con permisos específicos.
    """

    def has_module_permission(self, request):
        """
        Controla si el usuario tiene acceso al módulo (app) en el Django Admin.
        """
        return request.user.is_superuser or request.user.groups.filter(name_in=[UserGroups.MANAGER, UserGroups.PLATFORM_ADMIN]).exists()

    def has_view_permission(self, request, obj=None):
        """
        Controla si el usuario puede ver los objetos en este modelo.
        """
        return request.user.is_superuser or request.user.groups.filter(name_in=[UserGroups.MANAGER, UserGroups.PLATFORM_ADMIN]).exists()

    def has_add_permission(self, request):
        """
        Controla si el usuario puede añadir objetos en este modelo.
        """
        return request.user.is_superuser or request.user.groups.filter(name_in=[UserGroups.MANAGER, UserGroups.PLATFORM_ADMIN]).exists()

    def has_change_permission(self, request, obj=None):
        """
        Controla si el usuario puede cambiar objetos en este modelo.
        """
        return request.user.is_superuser or request.user.groups.filter(name_in=[UserGroups.MANAGER, UserGroups.PLATFORM_ADMIN]).exists()

    def has_delete_permission(self, request, obj=None):
        """
        Controla si el usuario puede eliminar objetos en este modelo.
        """
        return request.user.is_superuser or request.user.groups.filter(name_in=[UserGroups.MANAGER, UserGroups.PLATFORM_ADMIN]).exists()


class RRSSOnlyMixin:
    """
    Mixin para restringir el acceso en el Django Admin a usuarios con permisos específicos.
    """

    def has_module_permission(self, request):
        """
        Controla si el usuario tiene acceso al módulo (app) en el Django Admin.
        """
        # groups: rrss and managers
        return request.user.is_superuser or request.user.groups.filter(
            name__in=[UserGroups.RRSS, UserGroups.MANAGER, UserGroups.PLATFORM_ADMIN]
        ).exists()

    def has_view_permission(self, request, obj=None):
        """
        Controla si el usuario puede ver los objetos en este modelo.
        """
        return request.user.is_superuser or request.user.groups.filter(
            name__in=[UserGroups.RRSS, UserGroups.MANAGER, UserGroups.PLATFORM_ADMIN]
        ).exists()

    def has_add_permission(self, request):
        """
        Controla si el usuario puede añadir objetos en este modelo.
        """
        return request.user.is_superuser or request.user.groups.filter(
            name__in=[UserGroups.RRSS, UserGroups.MANAGER, UserGroups.PLATFORM_ADMIN]
        ).exists()

    def has_change_permission(self, request, obj=None):
        """
        Controla si el usuario puede cambiar objetos en este modelo.
        """
        return request.user.is_superuser or request.user.groups.filter(
            name__in=[UserGroups.RRSS, UserGroups.MANAGER, UserGroups.PLATFORM_ADMIN]
        ).exists()

    def has_delete_permission(self, request, obj=None):
        """
        Controla si el usuario puede eliminar objetos en este modelo.
        """
        return request.user.is_superuser or request.user.groups.filter(
            name__in=[UserGroups.RRSS, UserGroups.MANAGER, UserGroups.PLATFORM_ADMIN]
        ).exists()


__all__ = ('SuperUserOnlyMixin', 'ManagersOnlyMixin', 'RRSSOnlyMixin')
