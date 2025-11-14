from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import UsuarioPersonalizado

@admin.register(UsuarioPersonalizado)
class UsuarioPersonalizadoAdmin(UserAdmin):
    list_display = ['username', 'email', 'rol', 'is_active', 'date_joined']
    list_filter = ['rol', 'is_active', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('rol', 'avatar', 'telefono')
        }),
    )
    
    def get_queryset(self, request):
        # Prevenir que usuarios no superusuarios vean superusuarios
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs
    
    def has_change_permission(self, request, obj=None):
        # Prevenir que usuarios normales modifiquen superusuarios
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        # Prevenir que usuarios normales eliminen superusuarios
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)