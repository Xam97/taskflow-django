from django.contrib import admin
from .models import Tarea, Comentario

class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 1

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'proyecto', 'asignado_a', 'estado', 'prioridad', 'fecha_vencimiento']
    list_filter = ['estado', 'prioridad', 'fecha_creacion', 'fecha_vencimiento']
    search_fields = ['titulo', 'descripcion']
    inlines = [ComentarioInline]
    date_hierarchy = 'fecha_creacion'

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'tarea', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['contenido', 'autor__username']