from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Tarea, Comentario
from proyectos.models import Proyecto
from datetime import date, timedelta

User = get_user_model()

class TareaModelTest(TestCase):
    """Tests para el modelo Tarea"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.proyecto = Proyecto.objects.create(
            nombre='Proyecto Test',
            descripcion='Descripción',
            creador=self.user,
            fecha_vencimiento=date.today() + timedelta(days=30)
        )
        self.tarea = Tarea.objects.create(
            titulo='Tarea Test',
            descripcion='Descripción de la tarea',
            proyecto=self.proyecto,
            creador=self.user,
            prioridad=2
        )
    
    def test_tarea_creada(self):
        """Test que verifica que una tarea se crea correctamente"""
        self.assertEqual(self.tarea.titulo, 'Tarea Test')
        self.assertEqual(self.tarea.proyecto, self.proyecto)
        self.assertEqual(self.tarea.estado, 'pendiente')
    
    def test_esta_vencida(self):
        """Test que verifica el método esta_vencida"""
        self.assertFalse(self.tarea.esta_vencida())
        self.tarea.fecha_vencimiento = date.today() - timedelta(days=1)
        self.tarea.save()
        self.assertTrue(self.tarea.esta_vencida())
    
    def test_progreso(self):
        """Test que verifica el método progreso"""
        self.assertEqual(self.tarea.progreso(), 0)
        self.tarea.estado = 'en_progreso'
        self.tarea.save()
        self.assertEqual(self.tarea.progreso(), 50)
        self.tarea.estado = 'completada'
        self.tarea.save()
        self.assertEqual(self.tarea.progreso(), 100)

class TareaViewsTest(TestCase):
    """Tests para las vistas de tareas"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.proyecto = Proyecto.objects.create(
            nombre='Proyecto Test',
            descripcion='Descripción',
            creador=self.user,
            fecha_vencimiento=date.today() + timedelta(days=30)
        )
        self.tarea = Tarea.objects.create(
            titulo='Tarea Test',
            descripcion='Descripción',
            proyecto=self.proyecto,
            creador=self.user
        )
    
    def test_lista_tareas_requiere_login(self):
        """Test que verifica que la lista requiere autenticación"""
        response = self.client.get(reverse('tareas:lista_tareas'))
        self.assertEqual(response.status_code, 302)
    
    def test_lista_tareas_con_login(self):
        """Test que verifica que la lista funciona con login"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tareas:lista_tareas'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.tarea, response.context['tareas'])
    
    def test_crear_tarea(self):
        """Test que verifica la creación de una tarea"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('tareas:crear_tarea'), {
            'titulo': 'Nueva Tarea',
            'descripcion': 'Descripción',
            'proyecto': self.proyecto.pk,
            'prioridad': 2,
            'estado': 'pendiente'
        })
        # Puede ser 200 (con errores) o 302 (éxito)
        self.assertIn(response.status_code, [200, 302])
        # Verificar que la tarea se creó
        self.assertTrue(Tarea.objects.filter(titulo='Nueva Tarea').exists())
