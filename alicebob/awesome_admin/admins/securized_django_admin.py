from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from awesome_admin.mixing import SuperUserOnlyMixin

admin.site.unregister(Group)
admin.site.unregister(User)


# Personaliza la clase administrativa para Group
# class CustomGroupAdmin(GroupAdmin, ModelAdmin, SuperUserOnlyMixin):
@admin.register(Group)
class CustomGroupAdmin(SuperUserOnlyMixin, GroupAdmin, ModelAdmin):
    """
    Admin para el modelo Group con restricciones de permisos.
    """
    # add action: change password


# Personaliza la clase administrativa para User
@admin.register(User)
class CustomUserAdmin(SuperUserOnlyMixin, UserAdmin, ModelAdmin):
    """
    Admin para el modelo User con restricciones de permisos.
    """
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
