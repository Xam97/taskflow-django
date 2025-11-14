from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import UsuarioPersonalizado

User = get_user_model()

class UsuarioModelTest(TestCase):
    """Tests para el modelo UsuarioPersonalizado"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            rol='miembro'
        )
    
    def test_usuario_creado(self):
        """Test que verifica que un usuario se crea correctamente"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.rol, 'miembro')
    
    def test_es_administrador(self):
        """Test que verifica el método es_administrador"""
        self.assertFalse(self.user.es_administrador())
        self.user.rol = 'admin'
        self.user.save()
        self.assertTrue(self.user.es_administrador())
    
    def test_str_representation(self):
        """Test que verifica la representación en string"""
        self.assertIn('testuser', str(self.user))

class UsuarioViewsTest(TestCase):
    """Tests para las vistas de usuarios"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_home_view(self):
        """Test que verifica que la vista home funciona"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_view(self):
        """Test que verifica que la vista de login funciona"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_registro_view(self):
        """Test que verifica que la vista de registro funciona"""
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)
    
    def test_registro_post(self):
        """Test que verifica el registro de un nuevo usuario"""
        response = self.client.post(reverse('registro'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect después de registro
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_dashboard_requiere_login(self):
        """Test que verifica que el dashboard requiere autenticación"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect a login
    
    def test_dashboard_con_login(self):
        """Test que verifica que el dashboard funciona con login"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
