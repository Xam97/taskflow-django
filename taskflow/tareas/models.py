from django.db import models
from django.urls import reverse
from usuarios.models import UsuarioPersonalizado
from proyectos.models import Proyecto

class Tarea(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('bloqueada', 'Bloqueada'),
    ]
    
    PRIORIDADES = [
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta'),
        (4, 'Crítica'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    prioridad = models.IntegerField(choices=PRIORIDADES, default=2)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    fecha_completado = models.DateTimeField(blank=True, null=True)
    
    # Relaciones
    proyecto = models.ForeignKey(
        Proyecto, 
        on_delete=models.CASCADE
    )
    asignado_a = models.ForeignKey(
        UsuarioPersonalizado, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='tareas_asignadas'
    )
    creador = models.ForeignKey(
        UsuarioPersonalizado, 
        on_delete=models.CASCADE,
        related_name='tareas_creadas'
    )
    
    def __str__(self):
        return f"{self.titulo} - {self.proyecto.nombre}"
    
    def get_absolute_url(self):
        return reverse('detalle_tarea', kwargs={'pk': self.pk})
    
    def esta_vencida(self):
        from django.utils import timezone
        if self.fecha_vencimiento and self.estado != 'completada':
            return self.fecha_vencimiento < timezone.now().date()
        return False
    
    def progreso(self):
        if self.estado == 'completada':
            return 100
        elif self.estado == 'en_progreso':
            return 50
        else:
            return 0
    
    class Meta:
        ordering = ['prioridad', '-fecha_creacion']
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'

class Comentario(models.Model):
    tarea = models.ForeignKey(
        Tarea, 
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    autor = models.ForeignKey(
        UsuarioPersonalizado, 
        on_delete=models.CASCADE
    )
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comentario de {self.autor} en {self.tarea.titulo}"
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'