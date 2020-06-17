from django.contrib import admin

# Register your models here.
from irctapp.models import Role, CustomUser, Group


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'nome_completo', 'role', 'created_at')

    def nome_completo(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name


admin.site.register(Role, RoleAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Group, GroupAdmin)
