# Proyecto FastAPI - Taskly

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.25-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-blue)
![Docker](https://img.shields.io/badge/Docker-20.10%2B-blue)
![GitHub](https://img.shields.io/badge/GitHub-Repo-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![GitHub contributors](https://img.shields.io/github/contributors/DanielE0802/taskly-api)

Este proyecto es una API construida con **FastAPI**, **SQLAlchemy** y **MySQL**. A continuación, se detallan los pasos necesarios para comenzar con el proyecto, configurarlo correctamente y empezar a trabajar en él.

## Requisitos

Antes de comenzar, asegúrate de tener instalados los siguientes programas:

- Python 3.8 o superior
- Git
- MySQL (o el contenedor de Docker con MySQL)

## Clonar el Repositorio

Clona el repositorio en tu máquina local:

```bash
git clone https://github.com/DanielE0802/taskly-api
cd taskly-api
```

## Crear un Entorno Virtual
Crea un entorno virtual para el proyecto:

```bash
python -m venv venv
```
Activa el entorno virtual:
- En Windows:
```bash
venv\Scripts\activate
```
- En Linux/Mac:
```bash
source venv/bin/activate
```
## Instalar Dependencias
Instala las dependencias necesarias utilizando `pip`:

```bash
pip install -r requirements.txt
```
## Configurar la Base de Datos
Asegúrate de tener una base de datos MySQL en funcionamiento. Puedes usar un contenedor de Docker para esto:

```bash
docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=taskly -p 3306:3306 -d mysql:latest
```
Crea un archivo `.env` en la raíz del proyecto y configura las variables de entorno necesarias:

si ya tienes una base de datos creada, puedes omitir el paso anterior y crear el archivo `.env` directamente.

```bash

```env
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/taskly
SECRET_KEY=tu_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
## Migraciones de Base de Datos
Aplica las migraciones iniciales a la base de datos:

```bash
alembic upgrade head
```
## Ejecutar la Aplicación
Inicia el servidor de desarrollo:

```bash
uvicorn app.main:app --reload
```
La aplicación estará disponible en `http://localhost:8000`.
## Documentación de la API
La documentación de la API se genera automáticamente y está disponible en `http://localhost:8000/docs` o `http://localhost:8000/redoc`.
