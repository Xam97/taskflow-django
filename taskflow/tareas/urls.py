from django.urls import path
from . import views
from .export_views import ExportarTareasCSVView, ExportarTareasPDFView

app_name = 'tareas'

urlpatterns = [
    path('', views.ListaTareasView.as_view(), name='lista_tareas'),
    path('crear/', views.CrearTareaView.as_view(), name='crear_tarea'),
    path('<int:pk>/', views.DetalleTareaView.as_view(), name='detalle_tarea'),
    path('<int:pk>/editar/', views.ActualizarTareaView.as_view(), name='actualizar_tarea'),
    path('<int:pk>/eliminar/', views.EliminarTareaView.as_view(), name='eliminar_tarea'),
    path('<int:tarea_pk>/comentario/crear/', views.CrearComentarioView.as_view(), name='crear_comentario'),
    path('<int:pk>/completar/', views.CambiarEstadoTareaView.as_view(), name='completar_tarea'),
    # Exportación
    path('exportar/csv/', ExportarTareasCSVView.as_view(), name='exportar_csv'),
    path('exportar/pdf/', ExportarTareasPDFView.as_view(), name='exportar_pdf'),
]