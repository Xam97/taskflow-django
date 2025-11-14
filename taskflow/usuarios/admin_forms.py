from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioPersonalizado

class AdminCreationForm(UserCreationForm):
    """Formulario para crear nuevos usuarios (miembros o administradores)"""
    
    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'rol']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'rol': 'Tipo de Usuario'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Permitir crear tanto administradores como miembros
        self.fields['rol'].choices = [
            ('admin', 'Administrador'),
            ('miembro', 'Miembro')
        ]
        self.fields['rol'].help_text = 'Selecciona el tipo de usuario a crear'