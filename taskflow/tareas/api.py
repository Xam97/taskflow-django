from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Tarea
from proyectos.models import Proyecto
from .serializers import TareaSerializer

class TareaViewSet(viewsets.ModelViewSet):
    # Serializer que convierte entre modelos Python y JSON
    serializer_class = TareaSerializer
    # Permitir acceso público para pruebas (POST/PUT/DELETE) — usar sólo en dev
    permission_classes = [permissions.AllowAny]
    queryset = Tarea.objects.all()  
    
    def get_queryset(self):
        user = self.request.user

        if not getattr(user, 'is_authenticated', False):
            # Mostrar sólo tareas de proyectos activos a usuarios anónimos
            return Tarea.objects.filter(proyecto__estado='activo')

        if user.is_superuser or getattr(user, 'rol', None) == 'admin':
            return Tarea.objects.all()

        proyectos_usuario = Proyecto.objects.filter(
            Q(creador=user) | Q(miembros=user)
        )
        return Tarea.objects.filter(
            Q(proyecto__in=proyectos_usuario) | 
            Q(asignado_a=user) |
            Q(creador=user)
        ).distinct()