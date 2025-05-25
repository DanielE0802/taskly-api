# 🚀 Taskly API - FastAPI + MySQL + JWT

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-blue)
![Docker](https://img.shields.io/badge/Docker-20.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Taskly API** es una aplicación backend construida con **FastAPI**, **MySQL** y **JWT**, que permite gestionar usuarios, proyectos y tareas. Este sistema incluye autenticación segura y soporte para múltiples ambientes (desarrollo y producción) mediante Docker.

---

## 📦 Estructura del Proyecto

```bash
taskly-api/
├── app/                   # Código fuente principal
│   ├── auth/              # Autenticación y seguridad (JWT)
│   ├── tasks/             # Endpoints y modelos para tareas
│   ├── projects/          # Endpoints y modelos para proyectos
│   ├── database.py        # Conexión a base de datos
│   ├── main.py            # Entrada principal de la app
│   └── local.env          # Variables de entorno
├── mysql/                 # Archivos de configuración MySQL
│   ├── db/                # SQL de estructura y datos iniciales
│   └── local.env          # Variables MySQL
├── docker-compose.yml     # Entorno de desarrollo
├── docker-compose.prod.yml# Entorno de producción
├── Dockerfile             # Imagen principal
└── requirements.txt
```

---

## ✅ Requisitos

- Python 3.12+
- Docker y Docker Compose
- Git

---

## 🔁 Clonar el Repositorio

```bash
git clone https://github.com/DanielE0802/taskly-api
cd taskly-api
```

---

## 🐳 Ejecución con Docker

### 🔧 Ambiente de Desarrollo

```bash
DEBUG=true INIT_DB=true docker-compose up --build
```

- `DEBUG=true`: habilita el debugger remoto en el puerto 5678.
- `INIT_DB=true`: carga la estructura y datos iniciales solo una vez.

### 🌐 Producción

```bash
docker-compose -f docker-compose.prod.yml up --build
```

---

## 🧪 Sin Docker (local)

### 1. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Crear archivo `.env`

```dotenv
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USERNAME=root
DATABASE_PASSWORD=root
DATABASE=tasklydb

SECRET_KEY=tu_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Ejecutar

```bash
uvicorn main:app --reload
```

Accede a: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Autenticación

Usa JWT. Luego de hacer login en `/auth/login`, utiliza:

```http
Authorization: Bearer <tu_token>
```

---

## 📌 Funcionalidades

### 👤 Usuarios
- Registro y login con JWT
- Recuperación de contraseña (próximamente)

### 📁 Proyectos
- CRUD de proyectos
- Relación N:M con usuarios (roles por proyecto)

### ✅ Tareas
- CRUD de tareas
- Relación con usuarios y responsables

---

## ⚙️ Variables Docker Útiles

| Variable   | Valores       | Descripción                                      |
|------------|---------------|--------------------------------------------------|
| DEBUG      | true / false  | Activa modo debugger remoto                      |
| INIT_DB    | true / false  | Carga estructura y datos al iniciar por primera vez |

---

## ⚙️ Variables de entorno

### 📁 `app/local.env`

| Variable                 | Descripción                                           |
|--------------------------|-------------------------------------------------------|
| `APP_SECRET_STRING`      | Se usa para firmar el JWT                             |
| `DATABASE_USERNAME`      | Usuario de la base de datos                           |
| `DATABASE_PASSWORD`      | Contraseña del usuario de la base de datos            |
| `DATABASE`               | Nombre de la base de datos                            |
| `DATABASE_HOST`          | Nombre del servicio de MySQL en Docker (por defecto: `mysql`) |
| `DATABASE_PORT`          | Puerto donde corre MySQL                              |
| `ENV`                    | Ambiente de ejecución (`dev` o `prod`)                |

### 📁 `mysql/local.env`

| Variable              | Descripción                                           |
|-----------------------|-------------------------------------------------------|
| `MYSQL_USER`          | Usuario no root de MySQL                              |
| `MYSQL_ROOT_PASSWORD` | Contraseña del usuario root                           |
| `MYSQL_PASSWORD`      | Contraseña del usuario definido en `MYSQL_USER`       |
| `MYSQL_DATABASE`      | Nombre de la base de datos que se creará automáticamente |
| `ENV`                 | Ambiente de ejecución (`dev` o `prod`)                |

---

## 📄 Licencia

MIT © 2025 [Daniel Estupiñán](https://github.com/DanielE0802)
