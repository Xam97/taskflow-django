from django.db import models
from django.urls import reverse
from usuarios.models import UsuarioPersonalizado

class Proyecto(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('pausado', 'Pausado'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_vencimiento = models.DateField()
    
    # Relaciones
    creador = models.ForeignKey(
        UsuarioPersonalizado, 
        on_delete=models.CASCADE,
        related_name='proyectos_creados'
    )
    miembros = models.ManyToManyField(
        UsuarioPersonalizado, 
        related_name='proyectos_colaboracion',
        blank=True
    )
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('detalle_proyecto', kwargs={'pk': self.pk})
    
    def tareas_pendientes(self):
        return self.tarea_set.filter(estado='pendiente').count()
    
    def tareas_completadas(self):
        return self.tarea_set.filter(estado='completada').count()
    
    def total_tareas(self):
        return self.tarea_set.count()
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'