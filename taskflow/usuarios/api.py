from rest_framework import viewsets, permissions
from .models import UsuarioPersonalizado
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = UsuarioPersonalizado.objects.all()
    serializer_class = UsuarioSerializer
    # Permitir acceso público para pruebas (POST/PUT/DELETE) — usar sólo en dev
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        user = self.request.user
        # Si la API está pública, los listados públicos deben devolver usuarios
        # activos. Para operaciones que requieren más privacidad, cambie esto.
        if not getattr(user, 'is_authenticated', False):
            return UsuarioPersonalizado.objects.filter(is_active=True)

        if user.is_superuser:
            return UsuarioPersonalizado.objects.all()
        # Un usuario autenticado sólo ve su propio perfil
        return UsuarioPersonalizado.objects.filter(id=user.id)
