from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count, Q
from .models import UsuarioPersonalizado
from .forms import RegistroForm
from proyectos.models import Proyecto
from tareas.models import Tarea

# Vista de Login personalizada
class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        # Mensaje de error genérico para mayor seguridad
        response = super().form_invalid(form)
        # No revelar información específica sobre qué falló
        return response

# Vista de Registro
class RegistroView(CreateView):
    model = UsuarioPersonalizado
    form_class = RegistroForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        form.instance.rol = 'miembro'
        return super().form_valid(form)

# Vista de Dashboard (página principal después del login)
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Si es admin, cuenta TODOS los proyectos
        if user.is_superuser or user.rol == 'admin':
            proyectos_count = Proyecto.objects.count()
            tareas_completadas = Tarea.objects.filter(estado='completada').count()
            tareas_pendientes = Tarea.objects.filter(estado='pendiente').count()
            proyectos_recientes = Proyecto.objects.all().order_by('-fecha_creacion')[:3]
            tareas_recientes = Tarea.objects.all().order_by('-fecha_creacion')[:6]
            miembros_count = UsuarioPersonalizado.objects.count()
            usuarios_activos = UsuarioPersonalizado.objects.filter(is_active=True).count()
            usuarios_recientes = UsuarioPersonalizado.objects.order_by('-date_joined')[:5]
            total_admins = UsuarioPersonalizado.objects.filter(
                Q(rol='admin') | Q(is_superuser=True)
            ).count()
        else:
            # Usuario normal cuenta solo sus proyectos
            proyectos_usuario = Proyecto.objects.filter(
                Q(creador=user) | Q(miembros=user)
            ).distinct()
            
            proyectos_count = proyectos_usuario.count()
            tareas_completadas = Tarea.objects.filter(
                Q(asignado_a=user) | Q(creador=user) | Q(proyecto__in=proyectos_usuario),
                estado='completada'
            ).count()
            tareas_pendientes = Tarea.objects.filter(
                Q(asignado_a=user) | Q(creador=user) | Q(proyecto__in=proyectos_usuario),
                estado='pendiente'
            ).count()
            proyectos_recientes = proyectos_usuario.order_by('-fecha_creacion')[:3]
            tareas_recientes = Tarea.objects.filter(
                Q(asignado_a=user) | Q(creador=user) | Q(proyecto__in=proyectos_usuario)
            ).order_by('-fecha_creacion')[:6]
            miembros_count = UsuarioPersonalizado.objects.filter(rol='miembro').count()
            usuarios_activos = UsuarioPersonalizado.objects.filter(is_active=True).count()
            usuarios_recientes = UsuarioPersonalizado.objects.order_by('-date_joined')[:5]
            total_admins = UsuarioPersonalizado.objects.filter(
                Q(rol='admin') | Q(is_superuser=True)
            ).count()
        
        context['proyectos_count'] = proyectos_count
        context['tareas_pendientes'] = tareas_pendientes
        context['tareas_completadas'] = tareas_completadas
        context['miembros_count'] = miembros_count
        context['usuarios_activos'] = usuarios_activos
        context['proyectos_recientes'] = proyectos_recientes
        context['tareas_recientes'] = tareas_recientes
        context['usuarios_recientes'] = usuarios_recientes
        context['total_admins'] = total_admins
        
        return context

# Vista de Página de Inicio
class HomeView(TemplateView):
    template_name = 'usuarios/home.html'