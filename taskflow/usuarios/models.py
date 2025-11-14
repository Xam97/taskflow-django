from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class UsuarioPersonalizado(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('miembro', 'Miembro'),
    ]
    
    rol = models.CharField(
        max_length=20, 
        choices=ROLES, 
        default='miembro'
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        null=True, 
        blank=True,
        default='avatars/default.png'
    )
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"
    
    def es_administrador(self):
        return self.rol == 'admin'
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'