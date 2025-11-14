from django.contrib import admin
from .models import Tarea, Comentario

# Definir una clase inline para editar comentarios dentro de la vista de Tarea
class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 1


# Registrar y configurar el modelo Tarea en el admin
@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'proyecto', 'asignado_a', 'estado', 'prioridad', 'fecha_vencimiento']
    list_filter = ['estado', 'prioridad', 'fecha_creacion', 'fecha_vencimiento']
    search_fields = ['titulo', 'descripcion']
    inlines = [ComentarioInline]
    date_hierarchy = 'fecha_creacion'


# Registrar y configurar el modelo Comentario en el admin
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'tarea', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['contenido', 'autor__username']