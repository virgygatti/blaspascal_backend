# Backend - Sistema de Gestión de Libros

Este proyecto es el backend de una aplicación web para la gestión de libros con autenticación de usuarios, desarrollado en FastAPI y PostgreSQL.

---

## Requisitos

- Python 3.8+
- PostgreSQL

---

## Instalación y configuración

### 1. Clonar el repositorio y entrar al directorio
```bash
cd blaspascal_backend
```

### 2. Crear y activar un entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos
- Crea una base de datos en PostgreSQL (por ejemplo, `librosdb`).
- Puedes usar el siguiente comando:
  ```bash
  psql -U postgres -h <host> -c "CREATE DATABASE librosdb;"
  ```
- Configura las variables de entorno si necesitas cambiar usuario, contraseña, host o puerto:
  - `POSTGRES_USER` (por defecto: postgres)
  - `POSTGRES_PASSWORD` (por defecto: postgres)
  - `POSTGRES_DB` (por defecto: librosdb)
  - `POSTGRES_HOST` (por defecto: 127.0.0.1)
  - `POSTGRES_PORT` (por defecto: 5432)

### 5. Ejecutar el backend
```bash
fastapi dev main.py
```
- Accede a la documentación interactiva en: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Notas adicionales
- Para autenticación en Swagger, usa el endpoint `/login` para obtener el token y pégalo en "Authorize" como `Bearer <token>`.
- El backend crea automáticamente las tablas necesarias al iniciar si la base de datos existe.

---

## Estructura del proyecto

```
blaspascal_backend/
  ├── main.py           # App principal FastAPI
  ├── models.py         # Modelos SQLAlchemy
  ├── schemas.py        # Esquemas Pydantic
  ├── database.py       # Configuración de la base de datos
  ├── requirements.txt  # Dependencias
  └── ...
``` 