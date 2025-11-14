from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Proyecto
from datetime import date, timedelta

User = get_user_model()

class ProyectoModelTest(TestCase):
    """Tests para el modelo Proyecto"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.proyecto = Proyecto.objects.create(
            nombre='Proyecto Test',
            descripcion='Descripción del proyecto test',
            creador=self.user,
            fecha_vencimiento=date.today() + timedelta(days=30)
        )
    
    def test_proyecto_creado(self):
        """Test que verifica que un proyecto se crea correctamente"""
        self.assertEqual(self.proyecto.nombre, 'Proyecto Test')
        self.assertEqual(self.proyecto.creador, self.user)
    
    def test_total_tareas(self):
        """Test que verifica el método total_tareas"""
        self.assertEqual(self.proyecto.total_tareas(), 0)
    
    def test_str_representation(self):
        """Test que verifica la representación en string"""
        self.assertEqual(str(self.proyecto), 'Proyecto Test')

class ProyectoViewsTest(TestCase):
    """Tests para las vistas de proyectos"""
    
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
    
    def test_lista_proyectos_requiere_login(self):
        """Test que verifica que la lista requiere autenticación"""
        response = self.client.get(reverse('proyectos:lista_proyectos'))
        self.assertEqual(response.status_code, 302)
    
    def test_lista_proyectos_con_login(self):
        """Test que verifica que la lista funciona con login"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('proyectos:lista_proyectos'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.proyecto, response.context['proyectos'])
    
    def test_crear_proyecto(self):
        """Test que verifica la creación de un proyecto"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('proyectos:crear_proyecto'), {
            'nombre': 'Nuevo Proyecto',
            'descripcion': 'Descripción del nuevo proyecto',
            'fecha_vencimiento': (date.today() + timedelta(days=30)).strftime('%Y-%m-%d')
        })
        self.assertEqual(response.status_code, 302)  # Redirect después de crear
        self.assertTrue(Proyecto.objects.filter(nombre='Nuevo Proyecto').exists())
    
    def test_detalle_proyecto(self):
        """Test que verifica la vista de detalle"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('proyectos:detalle_proyecto', kwargs={'pk': self.proyecto.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['proyecto'], self.proyecto)
