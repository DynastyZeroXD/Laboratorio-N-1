# 🧪 Laboratorio N°1 – Automatización con Selenium (POM)

![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=java&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Maven](https://img.shields.io/badge/Maven-C71A36?style=for-the-badge&logo=apachemaven&logoColor=white)
![JUnit](https://img.shields.io/badge/JUnit-25A162?style=for-the-badge&logo=testing-library&logoColor=white)

---

## 📌 Descripción
Proyecto de automatización de pruebas usando **Selenium WebDriver en Java**, aplicando el patrón **Page Object Model (POM)** para mejorar la mantenibilidad y escalabilidad del código.

---

## 🚀 Funcionalidades
- ✅ Login de usuario
- 🛒 Agregar producto al carrito
- ✔️ Validar que el carrito contiene 1 producto
- ⏳ Uso de esperas explícitas (`WebDriverWait`)
- 📊 Generación de reportes de pruebas

---

## 🧱 Tecnologías
- Java
- Selenium WebDriver
- JUnit / TestNG
- Maven

---

## 📁 Estructura del proyecto
src/
├── main/
│ └── java/
│ └── pages/ # Clases Page Object
│ ├── LoginPage.java
│ ├── ProductsPage.java
│ └── CartPage.java
│
├── test/
│ └── java/
│ └── tests/ # Casos de prueba
│ ├── LoginTest.java
│ └── CartTest.java
│
└── resources/
└── config.properties # Configuración


---

## 🧩 Patrón Page Object Model (POM)

El patrón POM permite separar la lógica de la UI en clases independientes:

### 📍 Ventajas
- Código más limpio
- Fácil mantenimiento
- Reutilización de métodos
- Escalabilidad del proyecto

---

## ⚙️ Instalación

### 1. Clonar repositorio
```bash
git clone <URL_DEL_REPO>
cd <NOMBRE_DEL_PROYECTO>
mvn clean install
mvn test
