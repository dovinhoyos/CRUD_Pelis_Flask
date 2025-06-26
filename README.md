# 🎬 API REST de Gestión de Películas con Flask y MySQL

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Flask-2.3+-black?style=for-the-badge&logo=flask&logoColor=white" alt="Flask Version">
  <img src="https://img.shields.io/badge/MySQL-8.0+-orange?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL Version">
  <img src="https://img.shields.io/badge/SQLAlchemy-3.0+-blueviolet?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy Version">
  <img src="https://img.shields.io/badge/API_REST-✓-brightgreen?style=for-the-badge&logo=json&logoColor=white" alt="REST API">
</p>

---

## ✨ Descripción del Proyecto

Este proyecto es una **API RESTful robusta y modular** para la gestión eficiente de películas y sus géneros asociados. Construida con el potente microframework **Flask** y el ORM **Flask-SQLAlchemy**, se conecta a una base de datos **MySQL** para ofrecer un sistema completo de backend.

Se ha diseñado siguiendo las **mejores prácticas de arquitectura de software** para garantizar un código limpio, un bajo acoplamiento y una alta mantenibilidad. Incorpora un patrón de **fábrica de aplicaciones**, **modularización con Blueprints**, gestión segura de variables de entorno y un manejo de errores consistente para una experiencia de desarrollo y consumo de API superior.

## 🚀 Características Destacadas

- **Arquitectura Sólida:** Implementación del patrón de fábrica de aplicaciones para una inicialización flexible y escalable.
- **Modularidad Avanzada:** Código desacoplado en módulos específicos para configuración, extensiones, modelos y rutas (Blueprints), facilitando el desarrollo en equipo y la expansión.
- **API RESTful Completa:** Endpoints dedicados para operaciones CRUD (Crear, Leer, Actualizar, Borrar) de `Películas` y `Géneros`.
- **Base de Datos MySQL:** Persistencia de datos gestionada eficientemente con Flask-SQLAlchemy, aprovechando las capacidades relacionales de MySQL.
- **Manejo Seguro de Credenciales:** Utilización de archivos `.env` para la gestión de variables sensibles (¡nunca en el código!).
- **Validación y Manejo de Errores:** Respuestas JSON consistentes con códigos de estado HTTP semánticos (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 409 Conflict, 500 Internal Server Error).
- **Relaciones ORM:** Modelado de relaciones (`una-a-muchos`) entre géneros y películas directamente en los modelos SQLAlchemy.

## 📦 Estructura del Proyecto

Una mirada a la organización lógica y limpia del proyecto:

```
CRUD_Pelis_Flask/
├── .env # ⚠️ Archivo con variables de entorno (¡NO SUBIR A GIT!)
├── .gitignore # Reglas para ignorar archivos en Git
├── config.py # Configuración de la aplicación (BD, Debug, etc. centralizado)
├── app.py # Punto de entrada principal y fábrica de la aplicación
├── extensions.py # Inicialización desacoplada de Flask-SQLAlchemy (y otras extensiones)
├── models/ # Definiciones de los modelos de la base de datos
│ ├── init.py # Convierte el directorio en un paquete Python
│ ├── genero.py # Modelo para la entidad 'Genero'
│ └── pelicula.py # Modelo para la entidad 'Pelicula'
├── routes/ # Definiciones de los endpoints de la API (Flask Blueprints)
│ ├── init.py # Convierte el directorio en un paquete Python
│ ├── genero.py # Blueprints y rutas para la gestión de Géneros
│ └── pelicula.py # Blueprints y rutas para la gestión de Películas
└── requirements.txt # Listado de todas las dependencias del proyecto

```

## ⚙️ Configuración y Puesta en Marcha

Sigue estos pasos para tener la API funcionando en tu entorno local.

### **1. Requisitos Indispensables**

- **Python 3.9+**: Es el lenguaje base del proyecto.
- **MySQL Server (8.0+)**: La base de datos relacional para persistir la información.
- **`pip`**: El gestor de paquetes de Python (generalmente viene con Python).

### **2. Configuración del Entorno (`.env`)**

1. Crea un archivo llamado `.env` en el directorio raíz de tu proyecto (`my_flask_app/`).
2. Dentro de `.env`, define tus credenciales y nombre de base de datos de MySQL:

   ```dotenv
   # .env
   DB_USER=root
   DB_PASSWORD=tu_contraseña_mysql
   DB_HOST=localhost
   DB_NAME=gestionpeliculas
   ```

   **🚨 ¡ADVERTENCIA!** Nunca subas tu archivo `.env` a un repositorio público. `.gitignore` ya está configurado para evitar esto.

### **3. Configuración de la Base de Datos MySQL**

1. Asegúrate de que tu servidor MySQL esté en ejecución.
2. Conéctate a tu MySQL (ej. usando la terminal, MySQL Workbench, etc.) y crea la base de datos:

   ```sql
   CREATE DATABASE IF NOT EXISTS gestionpeliculas;
   -- Asegúrate de que tu usuario tenga los permisos adecuados sobre esta DB.
   ```

### **4. Instalación de Dependencias**

Desde el directorio raíz de tu proyecto (`my_flask_app/`), instala todas las librerías necesarias:

```bash
pip install -r requirements.txt

```

5. Ejecución de la Aplicación

Con todos los requisitos y configuraciones listos, inicia el servidor Flask:
Bash

```
python app.py

```

El servidor estará operativo en <http://127.0.0.1:5400/>. Al primer inicio, Flask-SQLAlchemy creará automáticamente las tablas generos y peliculas en tu base de datos gestionpeliculas.

🧪 Endpoints Disponibles (Ejemplos con curl)

Aquí una guía rápida para interactuar con tu API.

Ruta Base: <http://localhost:5400/>

📊 /generos (Gestión de Géneros)

    POST /generos/: Crear un nuevo género.
    Bash

    curl -X POST http://localhost:5400/generos/
    -H 'Content-Type: application/json' -d '{"genNombre": "Ciencia Ficción"}'

GET /generos/: Listar todos los géneros.
Bash

    curl -X GET http://localhost:5400/generos/

GET /generos/{id}: Obtener un género por su ID.
Bash

    curl -X GET http://localhost:5400/generos/1

🎬 /peliculas (Gestión de Películas)

POST /peliculas/: Crear una nueva película.

Importante: Asegúrate de que el pelGenero corresponda a un idGenero existente en tu base de datos (crea uno con el endpoint de géneros primero si es necesario).

Bash

```
curl -X POST http://localhost:5400/peliculas/ -H 'Content-Type: application/json' -d '{
    "pelCodigo": "INT001",
    "pelTitulo": "Interstellar",
    "pelProtagonista": "Matthew McConaughey",
    "pelDuracion": 169,
    "pelResumen": "Un equipo de exploradores viaja a través de un agujero de gusano para asegurar la supervivencia de la humanidad.",
    "pelFoto": "interstellar.jpg",
    "pelGenero": 1
}
```

GET /peliculas/: Listar todas las películas.

Bash

    curl -X GET http://localhost:5400/peliculas/

GET /peliculas/{id}: Obtener una película por su ID.
Bash

    curl -X GET http://localhost:5400/peliculas/1

🤝 Contribución

¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto, por favor, sigue estos pasos:

    Haz un "fork" de este repositorio.

    Crea una nueva rama (git checkout -b feature/tu-caracteristica).

    Implementa tus cambios.

    Asegúrate de que el código pase las pruebas (si las hubiera) y siga los estándares de estilo.

    Realiza tus commits utilizando los Conventional Commits.

    Abre un Pull Request con una descripción clara de tus cambios.

📄 Licencia

Este proyecto está distribuido bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
