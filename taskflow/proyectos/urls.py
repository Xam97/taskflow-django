from django.urls import path
from . import views
from .export_views import ExportarProyectosCSVView, ExportarProyectosPDFView

# Define el nombre de la aplicación para namespacing
# Permite referenciar URLs como 'proyectos:lista_proyectos'
app_name = 'proyectos'

# Lista de patrones URL de la aplicación
urlpatterns = [
    path('', views.ListaProyectosView.as_view(), name='lista_proyectos'),
    path('crear/', views.CrearProyectoView.as_view(), name='crear_proyecto'),
    path('<int:pk>/', views.DetalleProyectoView.as_view(), name='detalle_proyecto'),
    path('<int:pk>/editar/', views.ActualizarProyectoView.as_view(), name='actualizar_proyecto'),
    path('<int:pk>/eliminar/', views.EliminarProyectoView.as_view(), name='eliminar_proyecto'),
    # Exportación
    path('exportar/csv/', ExportarProyectosCSVView.as_view(), name='exportar_csv'),
    path('exportar/pdf/', ExportarProyectosPDFView.as_view(), name='exportar_pdf'),
]