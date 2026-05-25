<h1 align="center">
  <img src="https://github.com/user-attachments/assets/3abebde3-8ee0-40d0-ae38-82c52246b528" width="60" height="60" />
  Proyecto: Página para la gestión de servicio social
  <img src="https://github.com/user-attachments/assets/fe29e172-7262-4289-820a-1c08eecaa61b" width="60" height="60" />
</h1>

Repositorio correspondiente al proyecto **Página para la gestión de servicio social**, una aplicación web para administrar el proceso de servicio social mediante módulos diferenciados para administración, alumnos y empresas. El repositorio está organizado en frontend, backend, base de datos y observabilidad, con despliegue preparado mediante Docker Compose.

---

## Información del equipo
| Nombre completo | Matrícula |
|---|---:|
| Acosta Porcayo Alan Omar | 320206102 |
| Araiza Valdés Diego Antonio | 423032833 |
| Salazar Islas Luis Daniel | 320335163 |
| Tapia García Andrés | 320252367 |
| Velasquez Caudillo Osbaldo | 320341704 |

| Campo | Detalle |
|---|---|
| Materia | Sistemas distribuidos |
| Proyecto | Página para la gestión de servicio social |
| Semestre | 2026 - 2 |

---

## Introducción
Este proyecto consiste en una plataforma web para centralizar la administración del servicio social. La aplicación contempla distintos perfiles de usuario y separa las funciones de cada uno: administración de carreras, alumnos y empresas; consulta de vacantes por parte del alumno; y publicación y seguimiento de vacantes por parte de la empresa.

---

## Planteamiento del problema
El objetivo del sistema es digitalizar el proceso de gestión de servicio social para reducir el manejo manual de registros, facilitar el control de vacantes y postulaciones, y ofrecer un acceso diferenciado según el tipo de usuario.

---

## Motivación
La gestión de servicio social requiere seguimiento constante de vacantes, postulaciones, documentos y estados de aceptación. Una plataforma web permite concentrar esa información en un solo lugar, mejorar el control administrativo y dar a cada usuario una vista acorde a su función.

---

## Objetivos
- Centralizar la administración de carreras, alumnos y empresas.
- Permitir a los alumnos consultar vacantes y enviar postulaciones con archivo PDF.
- Permitir a las empresas crear vacantes y administrar postulantes.
- Mostrar paneles con métricas y accesos rápidos para cada rol.
- Mantener control de acceso por tipo de usuario y redirecciones seguras.

---

## Tecnologías
- **Frontend:** Vue 3, Vue Router, Pinia, Axios, Tailwind CSS, Vite, @vitejs/plugin-vue, @tailwindcss/vite.
- **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy, Alembic, Pydantic, pydantic-settings, python-jose, bcrypt, python-multipart, APScheduler, prometheus-client.
- **Base de datos:** PostgreSQL.
- **Infraestructura:** Docker, Docker Compose, Nginx.
- **Observabilidad:** Prometheus.
- **Herramientas de desarrollo y despliegue:** Dockerfile, variables de entorno `.env`, migraciones con Alembic, y servidor ASGI con Uvicorn.

---

## Arquitectura general del sistema

La siguiente arquitectura muestra la estructura general de la aplicación y la forma en que interactúan sus componentes principales.

<img width="1902" height="1109" alt="image" src="https://github.com/user-attachments/assets/8834eb19-6f3e-4b27-aafe-a671bfad887e" />

### Descripción de la arquitectura
- **Cliente web:** el usuario accede desde su navegador.
- **Frontend:** desarrollado con **Vue 3 + Vite** y servido mediante **Nginx**.
- **Backend:** implementado con **FastAPI** y ejecutado con **Uvicorn** en el puerto `8000`.
- **Base de datos:** **PostgreSQL** como sistema de persistencia.
- **Volumen de archivos:** almacenamiento de documentos PDF, CV, cartas e historial en un volumen de carga (`uploads`).
- **Comunicación interna:**
  - El navegador consume la interfaz web por HTTP.
  - El frontend realiza peticiones al backend en rutas `/api/*`.
  - El backend se comunica con la base de datos mediante SQL.

### Flujo general
1. El usuario accede a la aplicación desde su navegador.
2. Nginx entrega los archivos estáticos del frontend.
3. El frontend consume la API del backend.
4. FastAPI valida permisos, aplica reglas de negocio y procesa solicitudes.
5. La información se guarda en PostgreSQL.
6. Los documentos enviados por los usuarios se almacenan en el volumen de archivos.

---

## Marco teórico y diseño utilizado
- **Gestión de servicio social:** sistema orientado a organizar vacantes, postulaciones, estados y asignaciones.
- **Control por roles:** el sistema separa el comportamiento de administrador, alumno y empresa.
- **CRUD:** el repositorio documenta creación, edición y eliminación de carreras, alumnos, empresas y vacantes.
- **Flujo de postulación:** el alumno consulta vacantes, entra al detalle y envía su postulación con PDF.
- **Asignación y seguimiento:** el sistema maneja estados como pendiente, aceptada y rechazada, además de un código de confirmación para postulaciones aceptadas.
- **Programación en segundo plano:** se utiliza un scheduler para automatizar tareas periódicas relacionadas con el estado de las postulaciones.

**Diseño en el código actual:**
- El repositorio está organizado en módulos separados: `frontend`, `backend`, `database` y `observability`.
- El despliegue usa `docker-compose.yml` para levantar una base de datos PostgreSQL con volumen persistente, un backend Python expuesto en el puerto `8000` y un frontend expuesto en `3001`.
- El backend ejecuta migraciones con Alembic antes de iniciar el servidor.
- El backend está estructurado con carpetas como `models`, `routers`, `schemas`, `services`, además de `config.py`, `database.py`, `main.py` y `middleware.py`.
- El frontend usa Vite como herramienta de desarrollo y construcción, junto con Vue, Vue Router, Pinia y Axios.
- El repositorio incluye un archivo de observabilidad con `prometheus.yaml`.
- El proyecto incluye un plan de pruebas manual que cubre login, paneles, CRUDs, vacantes, postulaciones y casos de control de acceso por rol.

---

## Desarrollo

### Consideraciones de diseño
- **Autenticación y roles:** el acceso se valida por usuario y redirige al panel correspondiente.
- **Panel administrativo:** muestra métricas y acceso directo a gestión de carreras, alumnos y empresas.
- **Panel del alumno:** muestra vacantes abiertas, postulaciones pendientes, aceptadas y rechazadas.
- **Panel de empresa:** permite ver vacantes, agregar nuevas y revisar postulantes.
- **Documentos de postulación:** el alumno debe enviar un archivo PDF para postular.
- **Seguimiento de estados:** los postulantes pueden pasar por estados pendiente, aceptado o rechazado.
- **Código de confirmación:** al aceptar una postulación, el sistema asigna un código de confirmación de forma automática.

### Implementación
- **Backend:** contiene la lógica principal del sistema, junto con la configuración de migraciones y reinicio de base de datos.
- **Frontend:** concentra la interfaz de usuario y la capa visual de la plataforma.
- **Base de datos:** contiene la definición y estructura de la base de datos.
- **Observabilidad:** incluye configuración para monitoreo con `prometheus.yaml`.
- **Contenedorización:** el proyecto está preparado para ejecutarse con Docker Compose.

### Funcionalidades principales
- Inicio de sesión con rutas por rol.
- Panel de administración con métricas.
- CRUD de carreras.
- CRUD de alumnos.
- CRUD de empresas.
- Panel de alumno con catálogo de vacantes.
- Vista de detalle de vacante.
- Proceso de postulación con PDF.
- Panel de empresa con gestión de vacantes y postulantes.
- Cambio de estado de postulantes.
- Generación automática de código de confirmación para aceptados.

---

## Resultados
El repositorio documenta una implementación funcional que contempla autenticación, paneles por rol, CRUDs y un flujo completo de vacantes y postulaciones. El plan de pruebas incluye escenarios de éxito y casos borde, como acceso a rutas con rol incorrecto, ausencia de PDF en la postulación y redirección automática al login cuando el usuario no tiene permisos.

---

## Cómo ejecutar

### Requisitos
- Docker y Docker Compose instalados.
- Puerto `3001` disponible para el frontend.
- Puerto `8000` disponible para el backend.
- Un entorno compatible con la ejecución de contenedores.

### Ejecutar con Docker Compose
```bash
docker compose up --build
