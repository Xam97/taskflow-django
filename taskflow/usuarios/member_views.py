from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from .models import UsuarioPersonalizado
from .forms import UsuarioUpdateForm

class ListaUsuariosView(UserPassesTestMixin, ListView):
    model = UsuarioPersonalizado
    template_name = 'usuarios/lista_usuarios.html'
    context_object_name = 'usuarios'
    paginate_by = 10
    
    def test_func(self):
        # Solo administradores y superusuarios pueden acceder
        return self.request.user.is_superuser or self.request.user.rol == 'admin'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta página.')
        return redirect('dashboard')
    
    def get_queryset(self):
        # Excluir al usuario actual y mostrar solo miembros normales por defecto
        queryset = UsuarioPersonalizado.objects.exclude(id=self.request.user.id)
        
        # Filtrar por rol si se especifica
        rol_filter = self.request.GET.get('rol')
        if rol_filter:
            if rol_filter == 'admin':
                queryset = queryset.filter(Q(rol='admin') | Q(is_superuser=True))
            else:
                queryset = queryset.filter(rol=rol_filter)
        
        return queryset.order_by('-date_joined')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_usuarios'] = UsuarioPersonalizado.objects.count()
        context['total_miembros'] = UsuarioPersonalizado.objects.filter(rol='miembro').count()
        context['total_admins'] = UsuarioPersonalizado.objects.filter(
            Q(rol='admin') | Q(is_superuser=True)
        ).count()
        return context

class ActualizarUsuarioView(UserPassesTestMixin, UpdateView):
    model = UsuarioPersonalizado
    form_class = UsuarioUpdateForm
    template_name = 'usuarios/actualizar_usuario.html'
    context_object_name = 'usuario'
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.rol == 'admin'
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para editar usuarios.')
        return redirect('lista_usuarios')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pasar el usuario actual al formulario
        return kwargs
    
    def get_success_url(self):
        messages.success(self.request, f'Usuario {self.object.username} actualizado exitosamente.')
        return reverse_lazy('lista_usuarios')
    
    def get_queryset(self):
        if not self.request.user.is_superuser:
            return UsuarioPersonalizado.objects.filter(is_superuser=False)
        return UsuarioPersonalizado.objects.all()

class EliminarUsuarioView(UserPassesTestMixin, DeleteView):
    model = UsuarioPersonalizado
    template_name = 'usuarios/eliminar_usuario.html'
    context_object_name = 'usuario'
    success_url = reverse_lazy('lista_usuarios')
    
    def test_func(self):
        # Solo superusuarios pueden eliminar usuarios
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, 'Solo los superusuarios pueden eliminar usuarios.')
        return redirect('lista_usuarios')
    
    def get_queryset(self):
        # Prevenir eliminación de superusuarios por otros superusuarios
        # y prevenir que usuarios se eliminen a sí mismos
        return UsuarioPersonalizado.objects.exclude(id=self.request.user.id)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Usuario {self.get_object().username} eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)