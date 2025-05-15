import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# Configuración de la base de datos desde variables de entorno
DB_NAME = os.getenv("DB_NAME", "tasklydb")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Conexión directa con mysql-connector
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        return conn
    except mysql.connector.Error as err:
        raise Exception(f"Error al conectar con la base de datos: {err}")

# Función para ejecutar consultas SQL directas
def execute_query(query: str, params: tuple = ()):
    """Ejecuta una consulta SQL y devuelve el resultado."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()  # Obtener todos los resultados
        return result
    except mysql.connector.Error as err:
        raise Exception(f"Error al ejecutar la consulta: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para ejecutar consultas SQL que no devuelvan resultados (INSERT, UPDATE, DELETE)
def execute_update(query: str, params: tuple = ()):
    """Ejecuta una consulta SQL que no devuelve resultados (como INSERT, UPDATE, DELETE)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()  # Hacer commit en caso de cambios en la base de datos
    except mysql.connector.Error as err:
        conn.rollback()  # Hacer rollback si ocurre un error
        raise Exception(f"Error al ejecutar la consulta de actualización: {err}")
    finally:
        cursor.close()
        conn.close()
