from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from .models import Tarea
from proyectos.models import Proyecto
from datetime import datetime

class ExportarTareasCSVView(LoginRequiredMixin, View):
    """Exportar tareas a CSV"""
    
    def get(self, request):
        # Verificar permisos
        if not (request.user.is_superuser or request.user.rol == 'admin'):
            proyectos_usuario = Proyecto.objects.filter(
                Q(creador=request.user) | Q(miembros=request.user)
            )
            tareas = Tarea.objects.filter(
                Q(proyecto__in=proyectos_usuario) | 
                Q(asignado_a=request.user) |
                Q(creador=request.user)
            ).distinct()
        else:
            tareas = Tarea.objects.all()
        
        # Crear respuesta HTTP con tipo CSV
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="tareas_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        # Crear escritor CSV
        writer = csv.writer(response)
        writer.writerow(['Título', 'Proyecto', 'Estado', 'Prioridad', 'Asignado a', 'Creador', 'Fecha Creación', 'Fecha Vencimiento'])
        
        # Escribir datos
        for tarea in tareas:
            writer.writerow([
                tarea.titulo,
                tarea.proyecto.nombre,
                tarea.get_estado_display(),
                tarea.get_prioridad_display(),
                tarea.asignado_a.username if tarea.asignado_a else 'Sin asignar',
                tarea.creador.username,
                tarea.fecha_creacion.strftime('%Y-%m-%d %H:%M'),
                tarea.fecha_vencimiento.strftime('%Y-%m-%d') if tarea.fecha_vencimiento else 'Sin fecha'
            ])
        
        return response

class ExportarTareasPDFView(LoginRequiredMixin, View):
    """Exportar tareas a PDF"""
    
    def get(self, request):
        # Verificar permisos
        if not (request.user.is_superuser or request.user.rol == 'admin'):
            proyectos_usuario = Proyecto.objects.filter(
                Q(creador=request.user) | Q(miembros=request.user)
            )
            tareas = Tarea.objects.filter(
                Q(proyecto__in=proyectos_usuario) | 
                Q(asignado_a=request.user) |
                Q(creador=request.user)
            ).distinct()
        else:
            tareas = Tarea.objects.all()
        
        # Crear respuesta HTTP con tipo PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="tareas_{datetime.now().strftime("%Y%m%d")}.pdf"'
        
        # Crear documento PDF
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Título
        title = Paragraph("Reporte de Tareas", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Fecha de generación
        fecha = Paragraph(f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal'])
        elements.append(fecha)
        elements.append(Spacer(1, 0.3*inch))
        
        # Preparar datos de la tabla
        data = [['Título', 'Proyecto', 'Estado', 'Prioridad', 'Asignado a']]
        
        for tarea in tareas:
            data.append([
                tarea.titulo[:25],
                tarea.proyecto.nombre[:20],
                tarea.get_estado_display(),
                tarea.get_prioridad_display(),
                tarea.asignado_a.username[:15] if tarea.asignado_a else 'Sin asignar'
            ])
        
        # Crear tabla
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        return response

