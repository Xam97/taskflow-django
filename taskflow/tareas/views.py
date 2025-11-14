from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Tarea, Comentario
from .forms import TareaForm, ComentarioForm
from proyectos.models import Proyecto
class ListaTareasView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = 'tareas/lista_tareas.html'
    context_object_name = 'tareas'
    paginate_by = 10
    
    def get_queryset(self):
        #obtener parametros de filtro de la URL
        estado_filter = self.request.GET.get('estado')
        search_query = self.request.GET.get('q', '')
        prioridad_filter = self.request.GET.get('prioridad', '')
        
        # Si es admin, ve TODAS las tareas
        if self.request.user.is_superuser or self.request.user.rol == 'admin':
            queryset = Tarea.objects.all()
        else:
            # Usuario normal ve solo tareas de sus proyectos o asignadas a él
            proyectos_usuario = Proyecto.objects.filter(
                Q(creador=self.request.user) | Q(miembros=self.request.user)
            )
            queryset = Tarea.objects.filter(
                Q(proyecto__in=proyectos_usuario) | 
                Q(asignado_a=self.request.user) |
                Q(creador=self.request.user)
            ).distinct()
        
        # BÚSQUEDA AVANZADA
        if search_query:
            queryset = queryset.filter(
                Q(titulo__icontains=search_query) |
                Q(descripcion__icontains=search_query) |
                Q(proyecto__nombre__icontains=search_query) |
                Q(asignado_a__username__icontains=search_query) |
                Q(creador__username__icontains=search_query)
            )
        
        # FILTRO POR ESTADO
        if estado_filter:
            queryset = queryset.filter(estado=estado_filter)
        
        # FILTRO POR PRIORIDAD
        if prioridad_filter:
            queryset = queryset.filter(prioridad=prioridad_filter)
        
        return queryset.select_related('proyecto', 'asignado_a', 'creador').order_by('-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Pasar valores actuales de filtros al template
        context['estado_filter'] = self.request.GET.get('estado', '')
        context['prioridad_filter'] = self.request.GET.get('prioridad', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['estados_disponibles'] = Tarea.ESTADOS
        context['prioridades_disponibles'] = Tarea.PRIORIDADES
        return context

class DetalleTareaView(LoginRequiredMixin, DetailView):
    model = Tarea
    template_name = 'tareas/detalle_tarea.html'
    context_object_name = 'tarea'
    
    def get_queryset(self):
        # Si es admin, puede ver TODAS las tareas
        if self.request.user.is_superuser or self.request.user.rol == 'admin':
            return Tarea.objects.all()
        # Usuario normal solo ve tareas de sus proyectos
        proyectos_usuario = Proyecto.objects.filter(
            Q(creador=self.request.user) | Q(miembros=self.request.user)
        )
        return Tarea.objects.filter(proyecto__in=proyectos_usuario)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentarios'] = self.object.comentarios.all().order_by('-fecha_creacion')
        context['form_comentario'] = ComentarioForm()
        return context

class CrearTareaView(LoginRequiredMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tareas/crear_tarea.html'
    
    def get_success_url(self):
        messages.success(self.request, '✅ Tarea creada correctamente')
        return reverse_lazy('tareas:detalle_tarea', kwargs={'pk': self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        proyecto_id = self.request.GET.get('proyecto')
        if proyecto_id:
            try:
                proyecto = Proyecto.objects.get(id=proyecto_id)
                initial['proyecto'] = proyecto
            except Proyecto.DoesNotExist:
                pass
        return initial
    
    def form_valid(self, form):
        form.instance.creador = self.request.user
        return super().form_valid(form)

class ActualizarTareaView(LoginRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tareas/actualizar_tarea.html'
    context_object_name = 'tarea'
    
    def get_success_url(self):
        messages.success(self.request, '✅ Tarea actualizada correctamente')
        return reverse_lazy('tareas:detalle_tarea', kwargs={'pk': self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_queryset(self):
        # Admin puede editar TODAS las tareas
        if self.request.user.is_superuser or self.request.user.rol == 'admin':
            return Tarea.objects.all()
        
        # Usuario normal solo edita tareas donde es creador o asignado
        proyectos_usuario = Proyecto.objects.filter(
            Q(creador=self.request.user) | Q(miembros=self.request.user)
        )
        return Tarea.objects.filter(
            Q(proyecto__in=proyectos_usuario) & 
            (Q(creador=self.request.user) | Q(asignado_a=self.request.user))
        )
class EliminarTareaView(LoginRequiredMixin, DeleteView):
    model = Tarea
    template_name = 'tareas/eliminar_tarea.html'
    success_url = reverse_lazy('tareas:lista_tareas')
    context_object_name = 'tarea'
    
    def get_queryset(self):
        # Admin puede eliminar TODAS las tareas
        if self.request.user.is_superuser or self.request.user.rol == 'admin':
            return Tarea.objects.all()
        # Usuario normal solo elimina tareas que creó
        return Tarea.objects.filter(creador=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '✅ Tarea eliminada correctamente')
        return super().delete(request, *args, **kwargs)
    
class CambiarEstadoTareaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        tarea = get_object_or_404(Tarea, pk=pk)
        
        # Verificar permisos
        if not (request.user.is_superuser or 
                request.user.rol == 'admin' or 
                tarea.creador == request.user or 
                tarea.asignado_a == request.user):
            messages.error(request, '❌ No tienes permisos para cambiar el estado de esta tarea')
            return redirect('tareas:detalle_tarea', pk=pk)
        
        # Cambiar estado a completada
        tarea.estado = 'completada'
        tarea.fecha_completado = timezone.now()
        tarea.save()
        
        messages.success(request, '✅ Tarea marcada como completada correctamente')
        return redirect('tareas:detalle_tarea', pk=pk)

class CrearComentarioView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'tareas/crear_comentario.html'
    
    def get_success_url(self):
        messages.success(self.request, '✅ Comentario agregado correctamente')
        return reverse_lazy('tareas:detalle_tarea', kwargs={'pk': self.kwargs['tarea_pk']})
    
    def form_valid(self, form):
        tarea = get_object_or_404(Tarea, pk=self.kwargs['tarea_pk'])
        form.instance.tarea = tarea
        form.instance.autor = self.request.user
        return super().form_valid(form)