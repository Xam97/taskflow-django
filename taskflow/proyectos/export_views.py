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
from .models import Proyecto
from datetime import datetime

class ExportarProyectosCSVView(LoginRequiredMixin, View):
    """Exportar proyectos a CSV"""
    
    def get(self, request):
        # Verificar permisos
        if not (request.user.is_superuser or request.user.rol == 'admin'):
            proyectos = Proyecto.objects.filter(
                Q(creador=request.user) | Q(miembros=request.user)
            ).distinct()
        else:
            proyectos = Proyecto.objects.all()
        
        # Crear respuesta HTTP con tipo CSV
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="proyectos_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        # Crear escritor CSV
        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Descripción', 'Estado', 'Creador', 'Fecha Creación', 'Fecha Vencimiento', 'Total Tareas', 'Tareas Completadas'])
        
        # Escribir datos
        for proyecto in proyectos:
            writer.writerow([
                proyecto.nombre,
                proyecto.descripcion[:100],  # Limitar descripción
                proyecto.get_estado_display(),
                proyecto.creador.username,
                proyecto.fecha_creacion.strftime('%Y-%m-%d %H:%M'),
                proyecto.fecha_vencimiento.strftime('%Y-%m-%d'),
                proyecto.total_tareas(),
                proyecto.tareas_completadas()
            ])
        
        return response

class ExportarProyectosPDFView(LoginRequiredMixin, View):
    """Exportar proyectos a PDF"""
    
    def get(self, request):
        # Verificar permisos
        if not (request.user.is_superuser or request.user.rol == 'admin'):
            proyectos = Proyecto.objects.filter(
                Q(creador=request.user) | Q(miembros=request.user)
            ).distinct()
        else:
            proyectos = Proyecto.objects.all()
        
        # Crear respuesta HTTP con tipo PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="proyectos_{datetime.now().strftime("%Y%m%d")}.pdf"'
        
        # Crear documento PDF
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Título
        title = Paragraph("Reporte de Proyectos", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Fecha de generación
        fecha = Paragraph(f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal'])
        elements.append(fecha)
        elements.append(Spacer(1, 0.3*inch))
        
        # Preparar datos de la tabla
        data = [['Nombre', 'Estado', 'Creador', 'Fecha Vencimiento', 'Tareas']]
        
        for proyecto in proyectos:
            data.append([
                proyecto.nombre[:30],
                proyecto.get_estado_display(),
                proyecto.creador.username,
                proyecto.fecha_vencimiento.strftime('%Y-%m-%d'),
                f"{proyecto.tareas_completadas()}/{proyecto.total_tareas()}"
            ])
        
        # Crear tabla
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        return response

