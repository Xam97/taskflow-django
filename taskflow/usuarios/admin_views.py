from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .models import UsuarioPersonalizado
from .admin_forms import AdminCreationForm

class CrearAdministradorView(UserPassesTestMixin, CreateView):
    model = UsuarioPersonalizado
    form_class = AdminCreationForm
    template_name = 'usuarios/crear_administrador.html'
    success_url = reverse_lazy('lista_usuarios')
    
    def test_func(self):
        # Solo superusuarios y administradores pueden acceder
        return self.request.user.is_superuser or self.request.user.rol == 'admin'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.rol == 'admin':
            messages.success(self.request, f'✅ Administrador {self.object.username} creado correctamente')
        else:
            messages.success(self.request, f'✅ Miembro {self.object.username} creado correctamente')
        return response

class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'usuarios/admin_dashboard.html'
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.rol == 'admin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.contrib.auth import get_user_model
        from proyectos.models import Proyecto
        from tareas.models import Tarea
        
        User = get_user_model()
        
        context['total_usuarios'] = User.objects.count()
        context['total_proyectos'] = Proyecto.objects.count()
        context['total_tareas'] = Tarea.objects.count()
        context['usuarios_recientes'] = User.objects.order_by('-date_joined')[:5]
        
        return context