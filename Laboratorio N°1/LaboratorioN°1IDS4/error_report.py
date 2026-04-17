import os
import json
from datetime import datetime


class ErrorReportGenerator:
    """Generador de reportes de errores y logs de pruebas"""
    
    def __init__(self, test_name="Prueba"):
        self.test_name = test_name
        self.steps = []
        self.errors = []
        self.start_time = datetime.now()
        self.end_time = None
        self.status = "EN PROGRESO"
    
    def log_step(self, action, details="", success=True):
        """Registrar un paso ejecutado"""
        step = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
            "success": success,
            "icon": "OK" if success else "FAIL"
        }
        self.steps.append(step)
        icon = "OK" if success else "FAIL"
        print(f"[{icon}] {action}")
        if details:
            print(f"    -> {details}")
    
    def log_error(self, error_type, error_message, step_number=None):
        """Registrar un error"""
        error = {
            "timestamp": datetime.now().isoformat(),
            "type": error_type,
            "message": error_message,
            "step": step_number if step_number else len(self.steps)
        }
        self.errors.append(error)
        print(f"[ERROR {error_type}]: {error_message}")
    
    def set_status(self, status):
        """Establecer estado final"""
        self.status = status
    
    def generate_html_report(self, filename="reporte_errores.html"):
        """Generar reporte HTML profesional"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        # Color según estado
        status_colors = {
            "PASÓ": "#28a745",
            "FALLÓ": "#dc3545",
            "ERROR": "#ff6b6b",
            "EN PROGRESO": "#ffc107"
        }
        status_color = status_colors.get(self.status, "#6c757d")
        status_icon = "✓" if self.status == "PASÓ" else "✗" if self.status in ["FALLÓ", "ERROR"] else "⏳"
        
        # HTML de pasos
        steps_html = ""
        for i, step in enumerate(self.steps, 1):
            icon = "✓" if step['success'] else "✗"
            detail = f": {step['details']}" if step['details'] else ""
            steps_html += f"""
            <div class="step {'success' if step['success'] else 'fail'}">
                <div class="step-icon">{icon}</div>
                <div class="step-content">
                    <div class="step-title">{i}. {step['action']}{detail}</div>
                    <div class="step-time">{step['timestamp'].split('T')[1][:8]}</div>
                </div>
            </div>"""
        
        # HTML de errores
        errors_html = ""
        if self.errors:
            for error in self.errors:
                errors_html += f"""
            <div class="error-item">
                <strong>[{error['type']}]</strong> {error['message']}
            </div>"""
        else:
            errors_html = '<div class="no-errors">✓ Sin errores detectados</div>'
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.test_name} - Reporte</title>
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
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .status-badge {{
            display: inline-block;
            background: {status_color};
            color: white;
            padding: 8px 20px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 16px;
            margin-top: 10px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        .stat-box {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #666;
            font-size: 14px;
        }}
        .section {{
            padding: 30px;
        }}
        .section-title {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .steps-container {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        .step {{
            display: flex;
            gap: 15px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #28a745;
        }}
        .step.fail {{
            border-left-color: #dc3545;
        }}
        .step-icon {{
            font-size: 20px;
            font-weight: bold;
            min-width: 30px;
            text-align: center;
        }}
        .step.success .step-icon {{
            color: #28a745;
        }}
        .step.fail .step-icon {{
            color: #dc3545;
        }}
        .step-content {{
            flex: 1;
        }}
        .step-title {{
            color: #333;
            font-weight: 500;
        }}
        .step-time {{
            color: #999;
            font-size: 12px;
            margin-top: 4px;
        }}
        .error-item {{
            padding: 15px;
            background: #fff5f5;
            border-left: 4px solid #dc3545;
            border-radius: 8px;
            color: #721c24;
            margin-bottom: 10px;
        }}
        .no-errors {{
            padding: 15px;
            background: #f0f9f7;
            border-left: 4px solid #28a745;
            border-radius: 8px;
            color: #155724;
        }}
        .footer {{
            padding: 20px 30px;
            background: #f8f9fa;
            text-align: center;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{self.test_name}</h1>
            <div class="status-badge">{status_icon} {self.status}</div>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{duration:.2f}s</div>
                <div class="stat-label">Duración</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(self.steps)}</div>
                <div class="stat-label">Pasos</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(self.errors)}</div>
                <div class="stat-label">Errores</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{self.start_time.strftime('%H:%M:%S')}</div>
                <div class="stat-label">Inicio</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">📋 Log de Pasos</div>
            <div class="steps-container">
                {steps_html}
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">⚠️ Errores</div>
            {errors_html}
        </div>
        
        <div class="footer">
            Reporte generado: {self.end_time.strftime('%d/%m/%Y %H:%M:%S')}
        </div>
    </div>
</body>
</html>"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        return filename
    
    def generate_json_report(self, filename="reporte_errores.json"):
        """Generar reporte JSON"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        data = {
            "test_name": self.test_name,
            "status": self.status,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_seconds": duration,
            "total_steps": len(self.steps),
            "total_errors": len(self.errors),
            "steps": self.steps,
            "errors": self.errors
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filename
    
    def generate_txt_report(self, filename="reporte_errores.txt"):
        """Generar reporte en TXT"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        txt = f"""
==========================================================================
REPORTE: {self.test_name}
==========================================================================

ESTADO: {self.status}
FECHA: {self.start_time.strftime("%d/%m/%Y %H:%M:%S")}
DURACION: {duration:.2f} segundos

==========================================================================
LOG DE PASOS ({len(self.steps)} pasos)
==========================================================================

"""
        for i, step in enumerate(self.steps, 1):
            txt += f"{i}. [{step['icon']}] {step['action']}\n"
            if step['details']:
                txt += f"   -> {step['details']}\n"
        
        txt += f"""
==========================================================================
ERRORES ({len(self.errors)} errores)
==========================================================================

"""
        if self.errors:
            for error in self.errors:
                txt += f"[{error['type']}] {error['message']}\n"
        else:
            txt += "Sin errores detectados\n"
        
        txt += f"""
==========================================================================
FIN DEL REPORTE
==========================================================================
"""
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(txt)
        return filename
