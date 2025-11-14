from rest_framework import serializers
from .models import UsuarioPersonalizado

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioPersonalizado
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 'is_active']
        read_only_fields = ['id']
