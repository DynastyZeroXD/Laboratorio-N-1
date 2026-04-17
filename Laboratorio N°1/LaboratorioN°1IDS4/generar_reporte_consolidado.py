import json
import os
from datetime import datetime
from pathlib import Path

class ReporteConsolidado:
    """Genera un único reporte HTML consolidado con todas las pruebas"""
    
    def __init__(self):
        self.reportes = {}
        self.cargar_reportes()
    
    def cargar_reportes(self):
        """Carga todos los reportes JSON generados"""
        archivos = [
            "reporte_login_exitoso.json",
            "reporte_login_invalido.json",
            "reporte_agregar_producto.json",
            "reporte_validar_carrito.json"
        ]
        
        for archivo in archivos:
            if os.path.exists(archivo):
                try:
                    with open(archivo, 'r', encoding='utf-8') as f:
                        self.reportes[archivo.replace('.json', '')] = json.load(f)
                except Exception as e:
                    print(f"Error cargando {archivo}: {e}")
    
    def generar_html_consolidado(self, filename="reporte_completo.html"):
        """Genera un único HTML con todas las pruebas"""
        
        if not self.reportes:
            print("No hay reportes para consolidar")
            return
        
        # Calcular estadísticas generales
        total_pasos = sum(len(r.get('steps', [])) for r in self.reportes.values())
        total_errores = sum(len(r.get('errors', [])) for r in self.reportes.values())
        pruebas_pasadas = sum(1 for r in self.reportes.values() if r.get('status') == 'PASÓ')
        total_pruebas = len(self.reportes)
        
        # Generar HTML de cada prueba
        pruebas_html = ""
        for idx, (nombre, datos) in enumerate(self.reportes.items()):
            estado = datos.get('status', 'DESCONOCIDO')
            color_estado = '#28a745' if estado == 'PASÓ' else '#dc3545'
            icon_estado = '✓' if estado == 'PASÓ' else '✗'
            
            # Pasos
            pasos_html = ""
            for i, step in enumerate(datos.get('steps', []), 1):
                icon = '✓' if step.get('success', False) else '✗'
                detail = f": {step.get('details', '')}" if step.get('details') else ""
                tiempo = step.get('timestamp', '').split('T')[1][:8] if 'T' in step.get('timestamp', '') else ''
                pasos_html += f"""
                <div class="paso {'paso-ok' if step.get('success') else 'paso-error'}">
                    <div class="paso-numero">{i}</div>
                    <div class="paso-contenido">
                        <div class="paso-accion">{icon} {step.get('action', '')}{detail}</div>
                        <div class="paso-hora">{tiempo}</div>
                    </div>
                </div>
                """
            
            # Errores
            errores_html = ""
            if datos.get('errors'):
                for error in datos.get('errors', []):
                    errores_html += f"""
                    <div class="error-item">
                        <strong>[{error.get('type', 'ERROR')}]</strong><br>
                        {error.get('message', 'Sin detalles')}
                    </div>
                    """
            else:
                errores_html = '<div class="sin-errores">✓ Sin errores</div>'
            
            # Duración
            duracion = datos.get('duration_seconds', 0)
            
            pruebas_html += f"""
            <div class="prueba-card">
                <div class="prueba-header" style="background-color: {color_estado}">
                    <div class="prueba-titulo">
                        <span class="prueba-icon">{icon_estado}</span>
                        <span class="prueba-nombre">{datos.get('test_name', nombre)}</span>
                    </div>
                    <div class="prueba-stats">
                        <span class="stat">{len(datos.get('steps', []))} pasos</span>
                        <span class="stat">{duracion:.2f}s</span>
                    </div>
                </div>
                <div class="prueba-body">
                    <div class="section-pasos">
                        <h3>📋 Pasos Ejecutados</h3>
                        <div class="pasos-container">
                            {pasos_html}
                        </div>
                    </div>
                    <div class="section-errores">
                        <h3>⚠️ Errores</h3>
                        {errores_html}
                    </div>
                </div>
            </div>
            """
        
        # Generar HTML completo
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte Consolidado - Laboratorio N°1 IDS4</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 32px;
            color: #333;
            margin-bottom: 10px;
        }}
        
        .header p {{
            color: #666;
            font-size: 16px;
        }}
        
        .estadisticas {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        
        .estadistica-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .estadistica-numero {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .estadistica-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            margin-top: 10px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: #28a745;
            width: {pruebas_pasadas/total_pruebas*100}%;
            transition: width 0.3s ease;
        }}
        
        .pruebas-container {{
            display: grid;
            gap: 20px;
        }}
        
        .prueba-card {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        .prueba-header {{
            padding: 20px;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: bold;
        }}
        
        .prueba-titulo {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 18px;
        }}
        
        .prueba-icon {{
            font-size: 24px;
        }}
        
        .prueba-stats {{
            display: flex;
            gap: 15px;
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .prueba-body {{
            padding: 20px;
        }}
        
        .section-pasos, .section-errores {{
            margin-bottom: 20px;
        }}
        
        .section-pasos h3, .section-errores h3 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 16px;
        }}
        
        .pasos-container {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .paso {{
            display: flex;
            gap: 12px;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #28a745;
        }}
        
        .paso-error {{
            border-left-color: #dc3545;
        }}
        
        .paso-numero {{
            min-width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #667eea;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .paso-contenido {{
            flex: 1;
        }}
        
        .paso-accion {{
            color: #333;
            font-weight: 500;
            word-break: break-word;
        }}
        
        .paso-hora {{
            color: #999;
            font-size: 12px;
            margin-top: 4px;
        }}
        
        .error-item {{
            padding: 12px;
            background: #fff5f5;
            border-left: 4px solid #dc3545;
            border-radius: 6px;
            color: #721c24;
            margin-bottom: 8px;
            font-size: 14px;
            line-height: 1.5;
        }}
        
        .sin-errores {{
            padding: 12px;
            background: #f0f9f7;
            border-left: 4px solid #28a745;
            border-radius: 6px;
            color: #155724;
            text-align: center;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            padding: 20px;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
        }}
        
        @media (max-width: 768px) {{
            .prueba-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
            .prueba-stats {{
                width: 100%;
                justify-content: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Reporte Consolidado - Laboratorio N°1 IDS4</h1>
            <p>Pruebas Selenium - {datetime.now().strftime('%d de %B de %Y')}</p>
            
            <div class="estadisticas">
                <div class="estadistica-box">
                    <div class="estadistica-numero">{total_pruebas}</div>
                    <div class="estadistica-label">Pruebas Totales</div>
                </div>
                <div class="estadistica-box">
                    <div class="estadistica-numero">{pruebas_pasadas}/{total_pruebas}</div>
                    <div class="estadistica-label">Pruebas Exitosas</div>
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                </div>
                <div class="estadistica-box">
                    <div class="estadistica-numero">{total_pasos}</div>
                    <div class="estadistica-label">Total de Pasos</div>
                </div>
                <div class="estadistica-box">
                    <div class="estadistica-numero">{total_errores}</div>
                    <div class="estadistica-label">Errores Detectados</div>
                </div>
            </div>
        </div>
        
        <div class="pruebas-container">
            {pruebas_html}
        </div>
        
        <div class="footer">
            <p>📊 Reporte generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p>Laboratorio N°1 IDS4 - Pruebas de Automatización Web</p>
        </div>
    </div>
</body>
</html>"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Reporte consolidado generado: {filename}")
        return filename

if __name__ == "__main__":
    reporte = ReporteConsolidado()
    reporte.generar_html_consolidado()
