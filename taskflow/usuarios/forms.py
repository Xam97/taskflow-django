from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import UsuarioPersonalizado

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        label='Nombre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        label='Apellido',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })
    )
    
    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Prevenir registro de usuarios con nombres de admin
        restricted_usernames = ['admin', 'administrator', 'root', 'superuser']
        if username.lower() in restricted_usernames:
            raise ValidationError('Este nombre de usuario no está disponible.')
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.rol = 'miembro'  # Siempre registrar como miembro
        
        if commit:
            user.save()
        return user

class UsuarioUpdateForm(forms.ModelForm):
    """Formulario para que administradores actualicen usuarios"""
    
    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'first_name', 'last_name', 'rol', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_active': 'Usuario activo',
            'rol': 'Rol del usuario'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Si el usuario actual no es superusuario, no puede cambiar roles a admin
        if self.user and not self.user.is_superuser:
            # Administradores normales no pueden crear otros admins ni modificar superusuarios
            if self.instance.is_superuser:
                # No permitir editar superusuarios
                for field in self.fields:
                    self.fields[field].disabled = True
                self.fields['is_active'].disabled = False  # Pero pueden desactivarlos
            else:
                # Solo permitir cambiar entre miembro y admin para usuarios no superusuarios
                self.fields['rol'].choices = [
                    ('miembro', 'Miembro'),
                    ('admin', 'Administrador')
                ]