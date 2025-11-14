from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .admin_views import CrearAdministradorView, AdminDashboardView
from .member_views import ListaUsuariosView, ActualizarUsuarioView, EliminarUsuarioView

urlpatterns = [
    # Página de inicio
    path('', views.HomeView.as_view(), name='home'),
    
    # Autenticación pública
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
    
    # Dashboard después del login
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Administración (solo usuarios autorizados)
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('crear-admin/', CrearAdministradorView.as_view(), name='crear_administrador'),
    
    # Gestión de usuarios (solo administradores)
    path('usuarios/', ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('usuarios/<int:pk>/editar/', ActualizarUsuarioView.as_view(), name='actualizar_usuario'),
    path('usuarios/<int:pk>/eliminar/', EliminarUsuarioView.as_view(), name='eliminar_usuario'),
]