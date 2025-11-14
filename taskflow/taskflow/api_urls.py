from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importar los ViewSets
from usuarios.api import UsuarioViewSet
from proyectos.api import ProyectoViewSet
from tareas.api import TareaViewSet

# Crear el router
router = DefaultRouter()

# Registrar los ViewSets
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'proyectos', ProyectoViewSet, basename='proyecto')
router.register(r'tareas', TareaViewSet, basename='tarea')

# Las URLs del router incluyen automáticamente una vista raíz
urlpatterns = [
    path('', include(router.urls)),
]
