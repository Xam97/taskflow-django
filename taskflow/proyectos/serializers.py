from rest_framework import serializers
from .models import Proyecto

class ProyectoSerializer(serializers.ModelSerializer):
    creador_username = serializers.CharField(source='creador.username', read_only=True)
     # Obtiene el username del creador usando relación ForeignKey
    class Meta:
        # Especifica el modelo que será serializado
        model = Proyecto
        # Lista de campos que serán incluidos en la serialización
        fields = ['id', 'nombre', 'descripcion', 'estado', 'fecha_creacion', 
                 'fecha_vencimiento', 'creador', 'creador_username', 'miembros']
