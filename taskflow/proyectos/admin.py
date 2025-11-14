from django.contrib import admin
from .models import Proyecto

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'creador', 'estado', 'fecha_creacion', 'fecha_vencimiento']
    list_filter = ['estado', 'fecha_creacion', 'fecha_vencimiento']
    search_fields = ['nombre', 'descripcion']
    filter_horizontal = ['miembros']
    date_hierarchy = 'fecha_creacion'