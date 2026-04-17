# Laboratorio-N-1
📌 Descripción

Este proyecto implementa pruebas automatizadas utilizando Selenium WebDriver en Java, aplicando el patrón Page Object Model (POM) para mejorar la organización y mantenimiento del código.

🚀 Funcionalidades automatizadas
Login de usuario
Agregar producto al carrito
Validar que el carrito contiene 1 producto
Manejo de esperas explícitas (WebDriverWait)
Generación de reportes de pruebas
🧱 Tecnologías usadas
Java
Selenium WebDriver
JUnit / TestNG
Maven (gestión de dependencias)
📁 Estructura del proyecto
src
 ├── main
 │   └── java
 │       └── pages        # Clases Page Object
 ├── test
 │   └── java
 │       └── tests        # Casos de prueba
 └── resources            # Configuraciones
⚙️ Instalación y ejecución
Clonar el repositorio:
git clone <URL_DEL_REPO>
Abrir el proyecto en tu IDE (IntelliJ / Eclipse)
Instalar dependencias con Maven:
mvn clean install
Ejecutar pruebas:
mvn test
🧩 Patrón POM

Cada página de la aplicación se representa como una clase, separando:

Localizadores (By)
Acciones (métodos)
Lógica de interacción
✅ Ejemplo de prueba
Login válido
Selección de producto
Agregar al carrito
Validación del carrito
📊 Reportes

Los reportes de ejecución se generan automáticamente después de correr las pruebas (dependiendo de la configuración de JUnit/TestNG).

⚠️ Requisitos
Java 8 o superior
Maven instalado
Navegador (Chrome/Firefox)
WebDriver configurado
