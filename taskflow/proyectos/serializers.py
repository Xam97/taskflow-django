from rest_framework import serializers
from .models import Proyecto

class ProyectoSerializer(serializers.ModelSerializer):
    creador_username = serializers.CharField(source='creador.username', read_only=True)
    
    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'descripcion', 'estado', 'fecha_creacion', 
                 'fecha_vencimiento', 'creador', 'creador_username', 'miembros']
