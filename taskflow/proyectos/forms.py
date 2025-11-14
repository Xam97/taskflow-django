from django import forms
from django.db.models import Q
from .models import Proyecto

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_vencimiento', 'miembros']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proyecto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del proyecto',
                'rows': 4
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'miembros': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '6'
            })
        }
        labels = {
            'nombre': 'Nombre del Proyecto',
            'descripcion': 'Descripción',
            'fecha_vencimiento': 'Fecha de Vencimiento',
            'miembros': 'Miembros del Equipo'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        
        # Validar que user no sea None
        if self.user is None:
            return
        
        # Filtrar miembros para excluir al usuario actual (creador)
        if 'miembros' in self.fields:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            self.fields['miembros'].queryset = User.objects.exclude(id=self.user.id)
            self.fields['miembros'].help_text = 'Selecciona los miembros del equipo (no incluye al creador)'
        
        # Si no es el creador del proyecto, no puede editar fecha de vencimiento ni miembros
        if self.instance and self.instance.pk and self.instance.creador != self.user:
            if not self.user.is_superuser and self.user.rol != 'admin':
                self.fields['fecha_vencimiento'].disabled = True
                self.fields['miembros'].disabled = True
                self.fields['fecha_vencimiento'].help_text = 'Solo el creador del proyecto puede modificar la fecha de vencimiento'
                self.fields['miembros'].help_text = 'Solo el creador del proyecto puede gestionar los miembros'