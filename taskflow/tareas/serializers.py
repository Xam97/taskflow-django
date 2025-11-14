from rest_framework import serializers
from .models import Tarea

class TareaSerializer(serializers.ModelSerializer):
    proyecto_nombre = serializers.CharField(source='proyecto.nombre', read_only=True)
    asignado_username = serializers.CharField(source='asignado_a.username', read_only=True)
    
    class Meta:
        model = Tarea
        fields = ['id', 'titulo', 'descripcion', 'estado', 'prioridad', 
                 'proyecto', 'proyecto_nombre', 'asignado_a', 'asignado_username',
                 'fecha_vencimiento', 'fecha_creacion']
