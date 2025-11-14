from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Tarea, Comentario
from proyectos.models import Proyecto

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'proyecto', 'asignado_a', 'prioridad', 'estado', 'fecha_vencimiento']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la tarea'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción detallada de la tarea',
                'rows': 4
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'asignado_a': forms.Select(attrs={
                'class': 'form-select'
            }),
            'prioridad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'proyecto': 'Proyecto',
            'asignado_a': 'Asignado a',
            'prioridad': 'Prioridad',
            'estado': 'Estado',
            'fecha_vencimiento': 'Fecha de Vencimiento'
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        
        User = get_user_model()
        
        # Validar que user no sea None
        if user is None:
            return
        
        # Filtrar proyectos a los que el usuario tiene acceso
        if not user.is_superuser and getattr(user, 'rol', None) != 'admin':
            self.fields['proyecto'].queryset = Proyecto.objects.filter(
                Q(creador=user) | Q(miembros=user)
            ).distinct()
        else:
            # Admin ve todos los proyectos
            self.fields['proyecto'].queryset = Proyecto.objects.all()
        
        # Filtrar usuarios asignables - excluir al usuario actual
        if 'asignado_a' in self.fields:
            if user.is_superuser or getattr(user, 'rol', None) == 'admin':
                # Admin puede asignar a cualquier usuario excepto a sí mismo
                self.fields['asignado_a'].queryset = User.objects.exclude(id=user.id)
            else:
                # Usuario normal solo puede asignar a miembros de sus proyectos (excluyéndose a sí mismo)
                proyectos_acceso = self.fields['proyecto'].queryset
                usuarios_disponibles = set()
                for proyecto in proyectos_acceso:
                    usuarios_disponibles.add(proyecto.creador)
                    usuarios_disponibles.update(proyecto.miembros.all())
                # Excluir al usuario actual de la lista de asignables
                usuarios_disponibles = [u for u in usuarios_disponibles if u.id != user.id]
                self.fields['asignado_a'].queryset = User.objects.filter(
                    id__in=[u.id for u in usuarios_disponibles]
                ).distinct()
        
        # PERMISOS ESPECÍFICOS SEGÚN ROLES
        if self.instance and self.instance.pk:
            # ADMIN tiene permisos completos - no se restringe nada
            if user.is_superuser or user.rol == 'admin':
                return
                
            # USUARIO CREADOR de la tarea - permisos completos
            elif user == self.instance.creador:
                return  # Puede editar todo
                
            # USUARIO ASIGNADO a la tarea - solo puede cambiar estado
            elif user == self.instance.asignado_a:
                for field_name in self.fields:
                    if field_name != 'estado':
                        self.fields[field_name].disabled = True
                self.fields['estado'].help_text = 'Como usuario asignado, solo puedes cambiar el estado de la tarea'
                
            # USUARIO SIN PERMISOS ESPECÍFICOS - solo lectura
            else:
                for field_name in self.fields:
                    self.fields[field_name].disabled = True
                self.fields['estado'].help_text = 'No tienes permisos para editar esta tarea'

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu comentario aquí...',
                'rows': 3
            })
        }
        labels = {
            'contenido': 'Comentario'
        }