# 📊 Generador de Reportes de Errores y Logs

## ¿Qué es?

El nuevo generador de reportes crea **3 tipos de reportes** detallados para cada prueba:

1. **HTML** - Interfaz visual atractiva
2. **JSON** - Formato estructurado para análisis  
3. **TXT** - Formato texto plano para lectura rápida

---

## 📁 Archivos Generados

Después de ejecutar `login_selenium_final.py`, se crean reportes para cada prueba:

```
reporte_login_exitoso.html/.json/.txt
reporte_login_invalido.html/.json/.txt
reporte_agregar_producto.html/.json/.txt
reporte_validar_carrito.html/.json/.txt
```

---

## 📝 Contenido de los Reportes

### 1. Reporte TXT (fácil de leer)
```
==========================================================================
REPORTE: Login Exitoso
==========================================================================

ESTADO: PASÓ
FECHA: 16/04/2026 14:55:03
DURACION: 20.24 segundos

==========================================================================
LOG DE PASOS (9 pasos)
==========================================================================

1. [OK] Página abierta
   -> URL: https://www.saucedemo.com/
2. [OK] Ventana maximizada
3. [OK] Campo de usuario localizado
4. [OK] Usuario ingresado
   -> Usuario: standard_user
...

==========================================================================
ERRORES (0 errores)
==========================================================================

Sin errores detectados
```

### 2. Reporte JSON (para procesamiento)
```json
{
  "test_name": "Login Exitoso",
  "status": "PASÓ",
  "start_time": "2026-04-16T14:55:03.123456",
  "end_time": "2026-04-16T14:55:23.234567",
  "duration_seconds": 20.24,
  "total_steps": 9,
  "total_errors": 0,
  "steps": [
    {
      "timestamp": "2026-04-16T14:55:03.123456",
      "action": "Página abierta",
      "details": "URL: https://www.saucedemo.com/",
      "success": true,
      "icon": "OK"
    },
    ...
  ],
  "errors": []
}
```

### 3. Reporte HTML (interfaz visual)
- Abre automáticamente en el navegador
- Muestra estado con colores
- Estadísticas resumidas
- Interfaz interactiva

---

## 🔍 Información Registrada

Cada reporte incluye:

✅ **Pasos ejecutados**
- Timestamp exacto
- Descripción de la acción  
- Detalles adicionales
- Estado (OK/FAIL)

❌ **Errores detectados**
- Tipo de error
- Mensaje completo
- Número de paso donde ocurrió

📊 **Estadísticas**
- Total de pasos
- Pasos exitosos
- Pasos fallidos
- Total de errores
- Duración total

⏱️ **Información de tiempo**
- Fecha de inicio
- Hora de inicio y fin
- Duración exacta

---

## 🎯 Casos de Uso

### Debugging de Errores
Abre el reporte TXT o JSON para identificar exactamente dónde falló:
```
[ERROR Exception]: TimeoutException: Message: 
```

### Auditoría
Los reportes JSON tienen timestamps exactos para auditoría:
```json
"timestamp": "2026-04-16T14:55:23.456789"
```

### Integración con CI/CD
Los reportes JSON pueden ser parseados por scripts:
```python
import json
with open("reporte_login_exitoso.json") as f:
    data = json.load(f)
    if data["status"] == "PASÓ":
        print("Prueba exitosa")
```

### Presentaciones
Abre el HTML para mostrar un reporte visual durante presentaciones.

---

## 📜 Estructura de la Clase

```python
class ErrorReportGenerator:
    def __init__(self, test_name="Prueba")
    
    def log_step(action, details="", success=True)
        # Registra un paso ejecutado
    
    def log_error(error_type, error_message, step_number=None)
        # Registra un error
    
    def set_status(status)
        # Establece estado final: "PASÓ", "FALLÓ", "ERROR"
    
    def generate_html_report(filename="reporte_errores.html")
        # Genera reporte HTML
    
    def generate_json_report(filename="reporte_errores.json")
        # Genera reporte JSON
    
    def generate_txt_report(filename="reporte_errores.txt")
        # Genera reporte TXT
```

---

## 💡 Ejemplo de Uso

```python
from error_report import ErrorReportGenerator

# Crear reporte para la prueba
report = ErrorReportGenerator("Mi Prueba")

# Registrar pasos
report.log_step("Página abierta", "URL: https://ejemplo.com")
report.log_step("Usuario ingresado", "Usuario: admin")
report.log_step("Contraseña ingresada")

# Si hay error
try:
    # ... código ...
except Exception as e:
    report.log_error("ValueError", str(e))
    report.set_status("ERROR")

# Generar reportes
report.set_status("PASÓ")
report.generate_html_report("reporte.html")
report.generate_json_report("reporte.json")
report.generate_txt_report("reporte.txt")
```

---

## 🎨 Estados Posibles

- **PASÓ** - Prueba completada exitosamente
- **FALLÓ** - Prueba completada pero con fallo
- **ERROR** - Error durante la ejecución
- **EN PROGRESO** - Prueba aún ejecutándose

---

## 📌 Tips Útiles

1. **Busca en TXT** - Abre el archivo .txt con cualquier editor para búsqueda rápida
2. **Analiza JSON** - Usa herramientas online para visualizar JSON
3. **Visualiza HTML** - Abre en navegador para ver colores y estadísticas
4. **Automatiza** - Lee JSON en scripts para procesamiento automático

---

*Laboratorio N°1 IDS4 - Generador de Reportes de Errores*
