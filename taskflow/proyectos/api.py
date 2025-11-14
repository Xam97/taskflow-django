from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Proyecto
from .serializers import ProyectoSerializer

class ProyectoViewSet(viewsets.ModelViewSet):
    serializer_class = ProyectoSerializer
    # Permitir acceso público para pruebas (POST/PUT/DELETE) — usar sólo en dev
    permission_classes = [permissions.AllowAny]
    queryset = Proyecto.objects.all()  
    
    def get_queryset(self):
        user = self.request.user
        # Usuarios anónimos no tienen atributos personalizados
        if not getattr(user, 'is_authenticated', False):
            # Mostrar sólo proyectos activos a usuarios anónimos
            return Proyecto.objects.filter(estado='activo')

        if user.is_superuser or getattr(user, 'rol', None) == 'admin':
            return Proyecto.objects.all()

        return Proyecto.objects.filter(
            Q(creador=user) | Q(miembros=user)
        ).distinct()