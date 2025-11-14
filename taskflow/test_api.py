#!/usr/bin/env python
"""Script para probar que la API esté configurada correctamente"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskflow.settings')
django.setup()

from django.urls import get_resolver, resolve

print("=" * 50)
print("VERIFICACIÓN DE CONFIGURACIÓN DE API")
print("=" * 50)

# Obtener el resolver
resolver = get_resolver()

# Listar todas las URLs
print("\nURLs registradas en el proyecto:")
print("-" * 50)
for pattern in resolver.url_patterns:
    print(f"  [OK] {pattern.pattern}")

# Intentar resolver /api/
print("\nProbando resolucion de /api/:")
print("-" * 50)
try:
    match = resolve('/api/')
    print(f"  [OK] Ruta encontrada: {match.url_name}")
    print(f"  [OK] Vista: {match.func}")
    print(f"  [OK] Argumentos: {match.kwargs}")
except Exception as e:
    print(f"  [ERROR] Error: {e}")

# Intentar resolver /api/usuarios/
print("\nProbando resolucion de /api/usuarios/:")
print("-" * 50)
try:
    match = resolve('/api/usuarios/')
    print(f"  [OK] Ruta encontrada: {match.url_name}")
except Exception as e:
    print(f"  [ERROR] Error: {e}")

print("\n" + "=" * 50)
print("Si ves errores, verifica que:")
print("1. El servidor se haya reiniciado")
print("2. Django REST Framework esté instalado")
print("3. Los archivos api_urls.py y urls.py estén correctos")
print("=" * 50)

