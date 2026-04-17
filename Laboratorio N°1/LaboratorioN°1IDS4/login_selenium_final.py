from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import webbrowser

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
except ImportError:
    print("⚠️ webdriver-manager no instalado. Instalando...")
    import subprocess
    subprocess.check_call(["pip", "install", "webdriver-manager"])
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service

from error_report import ErrorReportGenerator

# ============================================
# CONFIGURACIÓN
# ============================================
URL = "https://www.saucedemo.com/"

# DELAYS (en segundos)
DELAY_BETWEEN_ACTIONS = 1.5
DELAY_AFTER_CLICK = 1.0
DELAY_AFTER_LOGIN = 2.0


# ============================================
# FUNCIÓN: LOGIN EXITOSO
# ============================================
def test_login_exitoso():
    """Prueba login exitoso con usuario estándar"""
    print("\n" + "="*60)
    print("PRUEBA 1: LOGIN EXITOSO")
    print("="*60)
    
    report = ErrorReportGenerator("Login Exitoso")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        # Abrir página
        driver.get(URL)
        report.log_step("Página abierta", f"URL: {URL}")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        driver.maximize_window()
        report.log_step("Ventana maximizada")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        wait = WebDriverWait(driver, 10)
        
        # Ingresar usuario
        username_field = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        report.log_step("Campo de usuario localizado")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        username_field.send_keys("standard_user")
        report.log_step("Usuario ingresado", "Usuario: standard_user")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        # Ingresar contraseña
        password_field = driver.find_element(By.ID, "password")
        report.log_step("Campo de contraseña localizado")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        password_field.send_keys("secret_sauce")
        report.log_step("Contraseña ingresada", "Longitud: 11 caracteres")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        # Presionar botón login
        login_button = driver.find_element(By.ID, "login-button")
        report.log_step("Botón login localizado")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        login_button.click()
        report.log_step("Botón login presionado")
        time.sleep(DELAY_AFTER_LOGIN)
        
        # Validar entrada al inventario
        wait.until(EC.presence_of_element_located((By.ID, "inventory_container")))
        report.log_step("Página de inventario cargada", f"URL actual: {driver.current_url}")
        
        if "inventory" in driver.current_url:
            print("\n✅ PRUEBA EXITOSA: Login correcto\n")
            report.set_status("PASÓ")
            report.generate_html_report("reporte_login_exitoso.html")
            report.generate_json_report("reporte_login_exitoso.json")
            report.generate_txt_report("reporte_login_exitoso.txt")
            return True
        else:
            report.log_error("ValidationError", "URL no contiene 'inventory'", len(report.steps))
            report.set_status("FALLÓ")
            print("\n❌ PRUEBA FALLIDA\n")
            return False
            
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        report.log_error("Exception", error_msg)
        report.set_status("ERROR")
        print(f"\n❌ ERROR: {error_msg}\n")
        report.generate_html_report("reporte_login_exitoso.html")
        report.generate_json_report("reporte_login_exitoso.json")
        report.generate_txt_report("reporte_login_exitoso.txt")
        return False
    finally:
        driver.quit()
        report.log_step("Navegador cerrado")


# ============================================
# FUNCIÓN: LOGIN INVÁLIDO
# ============================================
def test_login_invalido():
    """Prueba login inválido con credenciales incorrectas"""
    print("\n" + "="*60)
    print("PRUEBA 2: LOGIN INVÁLIDO")
    print("="*60)
    
    report = ErrorReportGenerator("Login Inválido")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        driver.get(URL)
        report.log_step("Página abierta", f"URL: {URL}")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        driver.maximize_window()
        report.log_step("Ventana maximizada")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        wait = WebDriverWait(driver, 10)
        
        # Ingresar credenciales inválidas
        username_field = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        report.log_step("Campo de usuario localizado")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        username_field.send_keys("usuario_incorrecto")
        report.log_step("Usuario incorrecto ingresado", "Usuario: usuario_incorrecto")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        password_field = driver.find_element(By.ID, "password")
        report.log_step("Campo de contraseña localizado")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        password_field.send_keys("contraseña_incorrecta")
        report.log_step("Contraseña incorrecta ingresada", "Longitud: 20 caracteres")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        report.log_step("Botón login presionado")
        time.sleep(DELAY_AFTER_LOGIN)
        
        # Validar mensaje de error
        error_message = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h3[@data-test='error']")
        ))
        
        error_text = error_message.text
        report.log_step("Mensaje de error capturado", f"Texto: {error_text}")
        
        if "epic sadface" in error_text.lower():
            print("\n✅ PRUEBA EXITOSA: Error validado correctamente\n")
            report.set_status("PASÓ")
            report.generate_html_report("reporte_login_invalido.html")
            report.generate_json_report("reporte_login_invalido.json")
            report.generate_txt_report("reporte_login_invalido.txt")
            return True
        else:
            report.log_error("ValidationError", f"Mensaje inesperado: {error_text}")
            report.set_status("FALLÓ")
            print("\n❌ PRUEBA FALLIDA\n")
            return False
            
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        report.log_error("Exception", error_msg)
        report.set_status("ERROR")
        print(f"\n❌ ERROR: {error_msg}\n")
        report.generate_html_report("reporte_login_invalido.html")
        report.generate_json_report("reporte_login_invalido.json")
        report.generate_txt_report("reporte_login_invalido.txt")
        return False
    finally:
        driver.quit()
        report.log_step("Navegador cerrado")


# ============================================
# FUNCIÓN: AGREGAR PRODUCTO AL CARRITO
# ============================================
def test_agregar_producto_carrito():
    """Prueba agregar un producto al carrito"""
    print("\n" + "="*60)
    print("PRUEBA 3: AGREGAR PRODUCTO AL CARRITO")
    print("="*60)
    
    report = ErrorReportGenerator("Agregar Producto al Carrito")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        driver.get(URL)
        report.log_step("Página abierta", f"URL: {URL}")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        driver.maximize_window()
        report.log_step("Ventana maximizada")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        wait = WebDriverWait(driver, 10)
        
        # LOGIN
        username_field = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        username_field.send_keys("standard_user")
        report.log_step("Login iniciado", "Usuario: standard_user")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("secret_sauce")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        time.sleep(DELAY_AFTER_LOGIN)
        
        wait.until(EC.presence_of_element_located((By.ID, "inventory_container")))
        report.log_step("Login completado", f"URL: {driver.current_url}")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        # AGREGAR PRODUCTO
        add_to_cart_button = wait.until(EC.element_to_be_clickable(
            (By.ID, "add-to-cart-sauce-labs-backpack")
        ))
        report.log_step("Botón 'Agregar al carrito' localizado")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        add_to_cart_button.click()
        report.log_step("Producto agregado al carrito", "Producto: Sauce Labs Backpack")
        time.sleep(DELAY_AFTER_CLICK)
        
        # Validar carrito
        cart_badge = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "shopping_cart_badge")
        ))
        
        cart_count = cart_badge.text
        report.log_step("Carrito validado", f"Productos en carrito: {cart_count}")
        
        if cart_count == "1":
            print("\n✅ PRUEBA EXITOSA: Producto agregado correctamente\n")
            report.set_status("PASÓ")
            report.generate_html_report("reporte_agregar_producto.html")
            report.generate_json_report("reporte_agregar_producto.json")
            report.generate_txt_report("reporte_agregar_producto.txt")
            return True
        else:
            report.log_error("ValidationError", f"Carrito muestra {cart_count}, esperaba 1")
            report.set_status("FALLÓ")
            print("\n❌ PRUEBA FALLIDA\n")
            return False
            
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        report.log_error("Exception", error_msg)
        report.set_status("ERROR")
        print(f"\n❌ ERROR: {error_msg}\n")
        report.generate_html_report("reporte_agregar_producto.html")
        report.generate_json_report("reporte_agregar_producto.json")
        report.generate_txt_report("reporte_agregar_producto.txt")
        return False
    finally:
        driver.quit()
        report.log_step("Navegador cerrado")


# ============================================
# FUNCIÓN: VALIDAR CARRITO
# ============================================
def test_validar_carrito():
    """Prueba abrir y validar contenido del carrito"""
    print("\n" + "="*60)
    print("PRUEBA 4: VALIDAR CONTENIDO DEL CARRITO")
    print("="*60)
    
    report = ErrorReportGenerator("Validar Contenido del Carrito")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        driver.get(URL)
        report.log_step("Página abierta", f"URL: {URL}")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        driver.maximize_window()
        report.log_step("Ventana maximizada")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        wait = WebDriverWait(driver, 10)
        
        # LOGIN
        username_field = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        username_field.send_keys("standard_user")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("secret_sauce")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        time.sleep(DELAY_AFTER_LOGIN)
        
        wait.until(EC.presence_of_element_located((By.ID, "inventory_container")))
        report.log_step("Login completado")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        # AGREGAR PRODUCTO
        add_to_cart_button = wait.until(EC.element_to_be_clickable(
            (By.ID, "add-to-cart-sauce-labs-backpack")
        ))
        add_to_cart_button.click()
        report.log_step("Producto agregado", "Sauce Labs Backpack")
        time.sleep(DELAY_AFTER_CLICK)
        
        # ABRIR CARRITO
        cart_icon = wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "shopping_cart_link")
        ))
        report.log_step("Icono del carrito localizado")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        cart_icon.click()
        report.log_step("Carrito abierto")
        time.sleep(DELAY_AFTER_CLICK)
        
        wait.until(EC.presence_of_element_located((By.ID, "cart_contents_container")))
        report.log_step("Página del carrito cargada")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        # Validar contenido
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        report.log_step("Productos en carrito localizados", f"Cantidad: {len(cart_items)}")
        time.sleep(DELAY_BETWEEN_ACTIONS)
        
        if len(cart_items) > 0:
            product_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
            product_price = driver.find_element(By.CLASS_NAME, "inventory_item_price").text
            
            report.log_step("Información del producto obtenida", f"Nombre: {product_name}")
            report.log_step("Precio obtenido", f"Precio: {product_price}")
            
            print("\n✅ PRUEBA EXITOSA: Carrito validado correctamente\n")
            report.set_status("PASÓ")
            report.generate_html_report("reporte_validar_carrito.html")
            report.generate_json_report("reporte_validar_carrito.json")
            report.generate_txt_report("reporte_validar_carrito.txt")
            return True
        else:
            report.log_error("ValidationError", "No hay productos en el carrito")
            report.set_status("FALLÓ")
            print("\n❌ PRUEBA FALLIDA\n")
            return False
            
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        report.log_error("Exception", error_msg)
        report.set_status("ERROR")
        print(f"\n❌ ERROR: {error_msg}\n")
        report.generate_html_report("reporte_validar_carrito.html")
        report.generate_json_report("reporte_validar_carrito.json")
        report.generate_txt_report("reporte_validar_carrito.txt")
        return False
    finally:
        driver.quit()
        report.log_step("Navegador cerrado")


# ============================================
# EJECUCIÓN PRINCIPAL
# ============================================
if __name__ == "__main__":
    print("\n" + "🔧 LABORATORIO N°1 - PRUEBAS SELENIUM - IDS4".center(60) + "\n")
    
    # Ejecutar todas las pruebas
    resultados = {
        "Login Exitoso": test_login_exitoso(),
        "Login Inválido": test_login_invalido(),
        "Agregar Producto": test_agregar_producto_carrito(),
        "Validar Carrito": test_validar_carrito()
    }
    
    # Resumen de resultados
    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)
    
    for prueba, resultado in resultados.items():
        estado = "✅ PASÓ" if resultado else "❌ FALLÓ"
        print(f"{prueba}: {estado}")
    
    total_exitosas = sum(1 for r in resultados.values() if r)
    print(f"\nTotal: {total_exitosas}/{len(resultados)} pruebas exitosas")
    print("="*60)
    
    print("\n📊 Se generaron reportes individuales para cada prueba:")
    print("   - reporte_login_exitoso.html/.json/.txt")
    print("   - reporte_login_invalido.html/.json/.txt")
    print("   - reporte_agregar_producto.html/.json/.txt")
    print("   - reporte_validar_carrito.html/.json/.txt")
    
    # Generar reporte consolidado
    print("\n🔄 Generando reporte consolidado...")
    try:
        from generar_reporte_consolidado import ReporteConsolidado
        reporte = ReporteConsolidado()
        reporte.generar_html_consolidado("reporte_completo.html")
        print("✅ Reporte consolidado: reporte_completo.html")
    except Exception as e:
        print(f"⚠️ Error generando reporte consolidado: {e}")
    
    print("\n✅ ¡Laboratorio completado!\n")
