# TaskFlow - Sistema de Gestión de Proyectos

Sistema web desarrollado con Django para la gestión de proyectos y tareas en equipo.

## 📋 Características

- ✅ Gestión completa de proyectos y tareas
- ✅ Sistema de autenticación y autorización
- ✅ Roles de usuario (Administrador y Miembro)
- ✅ Dashboard personalizado
- ✅ CRUD completo de proyectos y tareas
- ✅ Sistema de comentarios en tareas
- ✅ Panel de administración personalizado
- ✅ Interfaz responsive
- ✅ Búsqueda y filtrado avanzado
- ✅ Exportación a CSV/PDF
- ✅ API REST completa

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

### Pasos de Instalación

1. **Clonar el repositorio** (si aplica):
   ```bash
   git clone <url-del-repositorio>
   cd Taskflow-Django
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**:
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

4. **Instalar dependencias**:
   ```bash
   cd taskflow
   pip install -r ../requirements.txt
   ```

5. **Configurar variables de entorno**:
   ```bash
   # Copiar el archivo .env.example a .env
   cp ../.env.example .env
   
   # Editar .env y configurar SECRET_KEY (generar una nueva clave secreta)
   ```

6. **Aplicar migraciones**:
   ```bash
   python manage.py migrate
   ```

7. **Crear superusuario**:
   ```bash
   python manage.py createsuperuser
   ```

8. **Cargar datos de prueba** (opcional):
   ```bash
   python manage_data.py
   ```

9. **Ejecutar servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

10. **Acceder a la aplicación**:
    - Abrir navegador en: `http://127.0.0.1:8000/`
    - Panel de administración: `http://127.0.0.1:8000/admin/`

## 👥 Usuarios de Prueba

### Superusuario (creado manualmente)
- Username: `admin`
- Password: `task2024`

### Usuarios de prueba (generados con manage_data.py)
- **Miembros:**
  - Username: `maria`
  - Password: `test123`
  - Username: `carlos`
  - Password: `test123`
  - Username: `ana`
  - Password: `test123`

## 📁 Estructura del Proyecto

```
Taskflow-Django/
├── taskflow/              # Directorio principal del proyecto
│   ├── manage.py
│   ├── db.sqlite3
│   ├── taskflow/          # Configuración del proyecto
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── usuarios/          # App de usuarios
│   ├── proyectos/         # App de proyectos
│   ├── tareas/            # App de tareas
│   ├── templates/         # Templates HTML
│   ├── static/            # Archivos estáticos (CSS, JS)
│   └── media/             # Archivos subidos por usuarios
├── requirements.txt       # Dependencias del proyecto
├── .env.example          # Ejemplo de variables de entorno
└── README.md            # Este archivo
```

## 🔧 Configuración

### Variables de Entorno

Crear archivo `.env` en el directorio `taskflow/` con:

```env
SECRET_KEY=tu-clave-secreta-aqui-generar-una-nueva
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Generar SECRET_KEY

```python manage.py shell
from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())
```

## 🧪 Ejecutar Tests

```bash
python manage.py test
```

Para ver el coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
start htmlcov/index.html
```

## 📦 Dependencias Principales

- Django 5.2.7
- Pillow 12.0.0 (para manejo de imágenes)
- python-dotenv 1.2.1 (para variables de entorno)
- reportlab 4.0.7 (para exportación PDF)

Ver `requirements.txt` para lista completa.

## 🎯 Funcionalidades Principales

### Para Administradores
- Gestión completa de usuarios
- Acceso a todos los proyectos y tareas
- Panel de administración avanzado
- Exportación de datos

### Para Miembros
- Crear y gestionar proyectos propios
- Asignar tareas a miembros del equipo
- Comentar en tareas
- Ver dashboard personalizado

## 🔒 Seguridad

- ✅ Autenticación requerida para todas las vistas
- ✅ Validación de permisos por rol
- ✅ Protección CSRF
- ✅ Validación de formularios
- ✅ Passwords hasheados
- ⚠️ **IMPORTANTE**: Cambiar SECRET_KEY en producción
- ⚠️ **IMPORTANTE**: Configurar DEBUG=False en producción

## 📝 API REST

La API REST está disponible en `/api/`. Ver documentación en `/api/docs/`.


## 📄 Licencia

Este proyecto es parte de un proyecto académico.

## 👨‍💻 Autores

- Fabian Gimenez
- Sofia Morel
- Camila Rodas
- Alan Rojas

## 📞 Contacto

Para consultas sobre el proyecto, contactar al instructor del curso.

---

**Versión:** 1.0.0  
**Última actualización:** 2025

