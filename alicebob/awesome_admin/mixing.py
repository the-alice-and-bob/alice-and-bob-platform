from django.utils.html import format_html


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


class TagListMixin:
    """
    Mixin para mostrar tags estilizados en modelos de Django Admin.
    """
    tag_field_name = 'tags'  # Nombre del campo ManyToMany con los tags, puede ser sobrescrito

    def tag_list(self, obj):
        """
        Renderiza la lista de tags en el modelo.
        """
        tags = getattr(obj, self.tag_field_name).all()
        rendered_tags = ' '.join([
            format_html(
                '<span class="inline-block text-white px-2 py-0.5 text-xs font-medium rounded-sm" '
                'style="background-color: {};">{}</span>',
                tag.color_code, tag.name
            )
            for tag in tags
        ])
        return format_html(f'<div class="flex flex-wrap gap-1 items-center">{rendered_tags}</div>')

    tag_list.short_description = 'Tags'


__all__ = ('SuperUserOnlyMixin', 'ManagersOnlyMixin', 'RRSSOnlyMixin', 'TagListMixin')
