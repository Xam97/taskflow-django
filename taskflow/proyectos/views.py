from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count, Q
from .models import Proyecto
from .forms import ProyectoForm


# VISTA PARA CREAR PROYECTOS
class CrearProyectoView(LoginRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/crear_proyecto.html'
    success_url = reverse_lazy('proyectos:lista_proyectos') # Redirección después de éxito
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.creador = self.request.user # Asigna el usuario actual como creador
        response = super().form_valid(form)
        messages.success(self.request, '✅ Proyecto creado correctamente')
        return response

class ListaProyectosView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyectos/lista_proyectos.html'
    context_object_name = 'proyectos'
    paginate_by = 6 # Divide resultados en páginas de 6 elementos

    
    def get_queryset(self):
        # Si es admin, ve TODOS los proyectos
        if self.request.user.is_superuser or self.request.user.rol == 'admin':
            queryset = Proyecto.objects.all()
        else:
            # Usuario normal ve solo proyectos donde es creador o miembro
            queryset = Proyecto.objects.filter(
                Q(creador=self.request.user) | Q(miembros=self.request.user)
            ).distinct()
        
        # BÚSQUEDA AVANZADA
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query) |
                Q(descripcion__icontains=search_query) |
                Q(creador__username__icontains=search_query) |
                Q(creador__email__icontains=search_query)
            )
        
        # FILTRO POR ESTADO
        estado_filter = self.request.GET.get('estado', '')
        if estado_filter:
            queryset = queryset.filter(estado=estado_filter)
        
        # Anotar con conteo de tareas
        queryset = queryset.annotate(
            total_tareas=Count('tarea'),
            tareas_completadas=Count('tarea', filter=Q(tarea__estado='completada'))
        ).order_by('-fecha_creacion')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['estado_filter'] = self.request.GET.get('estado', '')
        context['estados_disponibles'] = Proyecto.ESTADOS
        return context

class DetalleProyectoView(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'proyectos/detalle_proyecto.html'
    context_object_name = 'proyecto'
    
    def get_queryset(self):
        # Si es admin, puede ver TODOS los proyectos
        if self.request.user.is_superuser or self.request.user.rol == 'admin':
            return Proyecto.objects.all()
        # Usuario normal solo ve proyectos donde es creador o miembro
        return Proyecto.objects.filter(
            Q(creador=self.request.user) | Q(miembros=self.request.user)
        ).distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = self.object
        
        # Calcular estadísticas para el template
        context['total_tareas'] = proyecto.tarea_set.count()
        context['tareas_completadas'] = proyecto.tarea_set.filter(estado='completada').count()
        context['tareas_pendientes'] = proyecto.tarea_set.filter(estado='pendiente').count()
        context['tareas_en_progreso'] = proyecto.tarea_set.filter(estado='en_progreso').count()
        
        return context

class ActualizarProyectoView(LoginRequiredMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/actualizar_proyecto.html'
    context_object_name = 'proyecto'
    
    def get_success_url(self):
        messages.success(self.request, '✅ Proyecto actualizado correctamente')
        return reverse_lazy('proyectos:detalle_proyecto', kwargs={'pk': self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs
    
    def get_queryset(self):
        # Admin puede editar TODOS los proyectos
        if self.request.user.is_superuser or self.request.user.rol == 'admin':
            return Proyecto.objects.all()
        # Usuario normal solo edita sus proyectos
        return Proyecto.objects.filter(creador=self.request.user)

class EliminarProyectoView(LoginRequiredMixin, DeleteView):
    model = Proyecto
    template_name = 'proyectos/eliminar_proyecto.html'
    success_url = reverse_lazy('proyectos:lista_proyectos')
    context_object_name = 'proyecto'
    
    def get_queryset(self):
        # Admin puede eliminar TODOS los proyectos
        if self.request.user.is_superuser or self.request.user.rol == 'admin':
            return Proyecto.objects.all()
        # Usuario normal solo elimina sus proyectos
        return Proyecto.objects.filter(creador=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '✅ Proyecto eliminado correctamente')
        return super().delete(request, *args, **kwargs)