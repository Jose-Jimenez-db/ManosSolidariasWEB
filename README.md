# Manos Solidarias

## Descripción del proyecto

**Manos Solidarias** es un sistema web desarrollado para apoyar la gestión de ayuda alimentaria destinada a comunidades en situación de vulnerabilidad.

La aplicación permite administrar beneficiarios, recursos alimenticios, entregas y reportes, facilitando el control del inventario y el seguimiento de la distribución de los recursos.

El proyecto fue desarrollado utilizando una arquitectura por capas, separando la lógica de negocio, acceso a datos, controladores y la interfaz de usuario.

---

# Tecnologías utilizadas

## Backend

- Python 3
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- PyMySQL

## Frontend

- HTML5
- CSS3
- JavaScript

## Base de datos

- MySQL

---

# Arquitectura del proyecto

El proyecto utiliza una arquitectura por capas compuesta por:

- Configuración
- Entidades (ORM)
- Repositorios
- Servicios
- Controladores
- Esquemas (Schemas)
- Autenticación
- Frontend

Esta separación facilita el mantenimiento, reutilización del código y escalabilidad del sistema.

---

# Funcionalidades

## Autenticación

- Inicio de sesión
- Registro de usuarios
- Gestión de sesión mediante token
- Cierre de sesión

---

## Beneficiarios

- Registrar beneficiarios
- Consultar beneficiarios
- Buscar por identificación
- Editar beneficiarios
- Eliminar beneficiarios

---

## Recursos alimenticios

- Registrar recursos
- Consultar recursos
- Buscar por código
- Editar recursos
- Eliminar recursos
- Control del inventario disponible

---

## Entregas alimentarias

- Registrar entregas
- Consultar historial
- Buscar por código
- Editar información permitida
- Eliminar entregas
- Restauración automática del inventario
- Descuento automático del inventario

---

## Reportes

El sistema genera los siguientes reportes:

- Beneficiarios por comunidad.
- Recursos con inventario bajo.
- Recursos más entregados.
- Costo total de la ayuda distribuida.

---

# Estructura del proyecto

```
app/

├── auth/
├── config/
├── controller/
├── entity/
├── repository/
├── schemas/
├── service/
└── main.py

web/

├── css/
├── js/
├── beneficiarios.html
├── entregas.html
├── login.html
├── principal.html
├── recursos.html
└── reportes.html
```

---

# Base de datos

El sistema utiliza MySQL.

Base de datos:

```
manos_solidarias_db
```

La creación de las tablas se realiza automáticamente mediante SQLAlchemy al iniciar la aplicación.

---

# Usuario por defecto

Al iniciar el sistema se crea automáticamente un usuario administrador.

Usuario:

```
admin
```

Contraseña:

```
admin123
```

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
```

---

## 2. Crear entorno virtual

Windows

```bash
python -m venv .venv
```

Activar

```bash
.venv\Scripts\activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Crear la base de datos

Crear una base llamada

```
manos_solidarias_db
```

---

## 5. Configurar la conexión

Modificar en

```
app/config/database.py
```

la cadena de conexión según el servidor MySQL.

---

## 6. Ejecutar la aplicación

```bash
python -m app.main
```

o

```bash
uvicorn app.main:app --reload
```

---

# Acceso al sistema

Backend

```
http://127.0.0.1:8000
```

Frontend

Abrir el archivo

```
login.html
```

---

# Diagrama UML

El proyecto incluye el diagrama UML correspondiente, el cual representa las clases principales, relaciones y estructura general del sistema.

---

# Descripción general

El sistema fue diseñado siguiendo principios de separación de responsabilidades.

Cada capa posee una función específica:

- **Entity:** representa las tablas de la base de datos mediante SQLAlchemy.

- **Repository:** realiza todas las operaciones CRUD sobre la base de datos.

- **Service:** implementa la lógica de negocio y las validaciones.

- **Controller:** expone los endpoints REST utilizando FastAPI.

- **Schemas:** validan las entradas y salidas mediante Pydantic.

- **Frontend:** proporciona la interfaz gráfica utilizando HTML, CSS y JavaScript.

---

# Autor

Proyecto desarrollado para el curso de Desarrollo de Software III por:

- Esteban Salas Araya (C5J444).

- Jose Jiménez Araya (C5G177). 

- Gabriel Mora Ramírez (C5H497). 

Universidad de Costa Rica, Sede del Pacifico.