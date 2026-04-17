import os
from datetime import datetime
import json

class ReportGenerator:
    """Generador de reportes HTML para pruebas de Selenium"""
    
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
        self.end_time = None
    
    def add_result(self, test_name, status, description, steps):
        """Agregar resultado de una prueba"""
        self.results.append({
            "name": test_name,
            "status": status,
            "description": description,
            "steps": steps,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_html_report(self, filename="reporte_pruebas.html"):
        """Generar reporte en HTML"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        passed = sum(1 for r in self.results if r["status"] == "PASÓ")
        failed = sum(1 for r in self.results if r["status"] == "FALLÓ")
        total = len(self.results)
        success_rate = (passed / total * 100) if total > 0 else 0
        
        html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Pruebas - Selenium</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .summary-card h3 {{
            color: #666;
            margin-bottom: 10px;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .summary-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .summary-card.failed .number {{
            color: #dc3545;
        }}
        
        .summary-card.passed .number {{
            color: #28a745;
        }}
        
        .summary-card.rate .number {{
            color: #764ba2;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .test-result {{
            margin-bottom: 30px;
            border-left: 5px solid #ccc;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 4px;
        }}
        
        .test-result.passed {{
            border-left-color: #28a745;
            background: #f0f8f4;
        }}
        
        .test-result.failed {{
            border-left-color: #dc3545;
            background: #fdf8f8;
        }}
        
        .test-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .test-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }}
        
        .test-status {{
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        
        .test-status.passed {{
            background: #28a745;
            color: white;
        }}
        
        .test-status.failed {{
            background: #dc3545;
            color: white;
        }}
        
        .test-description {{
            color: #666;
            margin-bottom: 15px;
            font-size: 0.95em;
        }}
        
        .steps {{
            background: white;
            padding: 15px;
            border-radius: 4px;
            border: 1px solid #e9ecef;
        }}
        
        .step {{
            padding: 8px 0;
            border-bottom: 1px solid #e9ecef;
            color: #555;
            font-size: 0.9em;
        }}
        
        .step:last-child {{
            border-bottom: none;
        }}
        
        .step::before {{
            content: "✓ ";
            color: #28a745;
            font-weight: bold;
            margin-right: 8px;
        }}
        
        .step.error::before {{
            content: "✗ ";
            color: #dc3545;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px 40px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e9ecef;
            font-size: 0.9em;
        }}
        
        .footer p {{
            margin: 5px 0;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 10px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            width: {success_rate}%;
            transition: width 0.3s ease;
        }}
        
        .logo {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🧪</div>
            <h1>Reporte de Pruebas Selenium</h1>
            <p>Laboratorio N°1 - IDS4</p>
        </div>
        
        <div class="summary">
            <div class="summary-card passed">
                <h3>Exitosas</h3>
                <div class="number">{passed}</div>
            </div>
            <div class="summary-card failed">
                <h3>Fallidas</h3>
                <div class="number">{failed}</div>
            </div>
            <div class="summary-card">
                <h3>Total</h3>
                <div class="number">{total}</div>
            </div>
            <div class="summary-card rate">
                <h3>Tasa de Éxito</h3>
                <div class="number">{success_rate:.1f}%</div>
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
            </div>
        </div>
        
        <div class="content">
            <h2 style="margin-bottom: 20px; color: #333;">Resultados Detallados</h2>
""".format(
            passed=passed,
            failed=failed, 
            total=total,
            success_rate=success_rate
        )
        
        for i, result in enumerate(self.results, 1):
            status_class = "passed" if result["status"] == "PASÓ" else "failed"
            status_text = "✅ PASÓ" if result["status"] == "PASÓ" else "❌ FALLÓ"
            
            html += f"""
            <div class="test-result {status_class}">
                <div class="test-header">
                    <div class="test-name">Prueba {i}: {result['name']}</div>
                    <div class="test-status {status_class}">{status_text}</div>
                </div>
                <div class="test-description">{result['description']}</div>
                <div class="steps">
"""
            
            for step in result["steps"]:
                html += f'                    <div class="step">{step}</div>\n'
            
            html += """
                </div>
            </div>
"""
        
        html += """
        </div>
        
        <div class="footer">
            <p><strong>Fecha de Ejecución:</strong> {start_date}</p>
            <p><strong>Duración Total:</strong> {duration:.2f} segundos</p>
            <p><strong>Generado por:</strong> Selenium Test Framework - IDS4 2026</p>
        </div>
    </div>
</body>
</html>
""".format(
            start_date=self.start_time.strftime("%d/%m/%Y %H:%M:%S"),
            duration=duration
        )
        
        # Guardar archivo
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        
        return filename
    
    def generate_json_report(self, filename="reporte_pruebas.json"):
        """Generar reporte en JSON"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        data = {
            "titulo": "Reporte de Pruebas Selenium",
            "proyecto": "Laboratorio N°1 IDS4",
            "fecha_inicio": self.start_time.isoformat(),
            "fecha_fin": self.end_time.isoformat(),
            "duracion_segundos": duration,
            "resumen": {
                "total": len(self.results),
                "exitosas": sum(1 for r in self.results if r["status"] == "PASÓ"),
                "fallidas": sum(1 for r in self.results if r["status"] == "FALLÓ"),
                "tasa_exito": (sum(1 for r in self.results if r["status"] == "PASÓ") / len(self.results) * 100) if len(self.results) > 0 else 0
            },
            "resultados": self.results
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filename
