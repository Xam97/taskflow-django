# Script para crear datos de prueba 
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskflow.settings')
django.setup()

from django.contrib.auth import get_user_model
from proyectos.models import Proyecto
from tareas.models import Tarea
from datetime import date, timedelta

Usuario = get_user_model()

def crear_usuarios():
    print("👤 Creando usuarios de prueba...")
    
    # Crear o actualizar superusuario admin
    admin_user, created = Usuario.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@taskflow.com',
            'is_staff': True,
            'is_superuser': True,
            'rol': 'admin'
        }
    )
    if created:
        admin_user.set_password('task2024')
        admin_user.save()
        print("✅ Superusuario admin creado: admin / task2024")
    else:
        admin_user.set_password('task2024')
        admin_user.save()
        print("✅ Superusuario admin actualizado: admin / task2024")
    
    # Crear usuarios normales
    usuarios_data = [
        {'username': 'maria', 'first_name': 'María', 'last_name': 'García'},
        {'username': 'carlos', 'first_name': 'Carlos', 'last_name': 'López'},
        {'username': 'ana', 'first_name': 'Ana', 'last_name': 'Martínez'},
    ]

    for user_data in usuarios_data:
        user, created = Usuario.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': f"{user_data['username']}@taskflow.com",
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'rol': 'miembro'
            }
        )
        if created:
            user.set_password('test123')
            user.save()
            print(f"✅ Usuario {user_data['username']} creado: {user_data['username']} / test123")
        else:
            user.set_password('test123')
            user.save()
            print(f"✅ Usuario {user_data['username']} actualizado: {user_data['username']} / test123")
    
    return admin_user, *[Usuario.objects.get(username=data['username']) for data in usuarios_data]

def crear_proyectos_y_tareas():
    print("📁 Creando proyectos y tareas...")
    
    admin, maria, carlos, ana = crear_usuarios()
    
    # Crear proyectos
    proyectos_data = [
        {
            'nombre': 'Desarrollo Web TaskFlow',
            'descripcion': 'Desarrollo del sistema de gestión de proyectos TaskFlow con Django',
            'dias_vencimiento': 30,
            'creador': admin,
            'miembros': [maria, carlos, ana]
        },
        {
            'nombre': 'Marketing Digital Q4',
            'descripcion': 'Campaña de marketing para el último trimestre del año',
            'dias_vencimiento': 45,
            'creador': maria,
            'miembros': [carlos, ana]
        },
        {
            'nombre': 'Rediseño App Móvil',
            'descripcion': 'Mejoras de UI/UX para la aplicación móvil principal',
            'dias_vencimiento': 60,
            'creador': carlos,
            'miembros': [maria, admin, ana]
        }
    ]

    for proyecto_data in proyectos_data:
        proyecto, created = Proyecto.objects.get_or_create(
            nombre=proyecto_data['nombre'],
            defaults={
                'descripcion': proyecto_data['descripcion'],
                'fecha_vencimiento': date.today() + timedelta(days=proyecto_data['dias_vencimiento']),
                'creador': proyecto_data['creador']
            }
        )
        if created:
            # Agregar miembros
            for miembro in proyecto_data['miembros']:
                proyecto.miembros.add(miembro)
            print(f"✅ Proyecto '{proyecto_data['nombre']}' creado")
        else:
            print(f"⚠️  Proyecto '{proyecto_data['nombre']}' ya existe")

    # Crear tareas para el primer proyecto
    proyecto1 = Proyecto.objects.get(nombre='Desarrollo Web TaskFlow')
    tareas_data = [
        {
            'titulo': 'Diseñar modelos de base de datos',
            'descripcion': 'Crear los modelos User, Project, Task, Comment con Django ORM',
            'proyecto': proyecto1,
            'asignado_a': maria,
            'prioridad': 3,
            'dias_vencimiento': 5
        },
        {
            'titulo': 'Implementar autenticación',
            'descripcion': 'Sistema de login, registro y permisos con Django Auth',
            'proyecto': proyecto1,
            'asignado_a': carlos,
            'prioridad': 3,
            'dias_vencimiento': 7
        },
        {
            'titulo': 'Crear templates base',
            'descripcion': 'Diseñar templates con Bootstrap y sistema de herencia',
            'proyecto': proyecto1,
            'asignado_a': ana,
            'prioridad': 2,
            'dias_vencimiento': 10
        },
        {
            'titulo': 'Configurar despliegue',
            'descripcion': 'Preparar entorno de producción y documentación',
            'proyecto': proyecto1,
            'asignado_a': admin,
            'prioridad': 1,
            'dias_vencimiento': 15
        }
    ]

    for tarea_data in tareas_data:
        tarea, created = Tarea.objects.get_or_create(
            titulo=tarea_data['titulo'],
            proyecto=tarea_data['proyecto'],
            defaults={
                'descripcion': tarea_data['descripcion'],
                'asignado_a': tarea_data['asignado_a'],
                'creador': admin,
                'prioridad': tarea_data['prioridad'],
                'fecha_vencimiento': date.today() + timedelta(days=tarea_data['dias_vencimiento'])
            }
        )
        if created:
            print(f"✅ Tarea '{tarea_data['titulo']}' creada")
        else:
            print(f"⚠️  Tarea '{tarea_data['titulo']}' ya existe")

    print("\n🎉 ¡DATOS DE PRUEBA CREADOS EXITOSAMENTE!")
    print("👤 USUARIOS DISPONIBLES:")
    print("   - admin / task2024 (Superusuario)")
    print("   - maria / test123 (Miembro)")
    print("   - carlos / test123 (Miembro)")
    print("   - ana / test123 (Miembro)")
    print("📁 PROYECTOS: 3 proyectos con tareas")
    print("📋 TAREAS: 4 tareas en 'Desarrollo Web TaskFlow'")
    print("🚀 ¡Sistema listo para usar!")

if __name__ == '__main__':
    crear_proyectos_y_tareas()