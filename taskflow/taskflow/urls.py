from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('taskflow.api_urls')),  # API REST
    path('api-auth/', include('rest_framework.urls')),  # Autenticación API
    path('', include('usuarios.urls')),
    path('proyectos/', include('proyectos.urls')),
    path('tareas/', include('tareas.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)