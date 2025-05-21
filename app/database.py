import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# Configuración de la base de datos desde variables de entorno
DB_NAME = os.getenv("DATABASE", "tasklydb")
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DATABASE_USERNAME", "root")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "root")
DB_DATABASE = os.getenv("DATABASE", "tasklydb")

def get_db_connection():
    """Establece una conexión a la base de datos MySQL."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE,
            port=DB_PORT
        )
        return conn
    except mysql.connector.Error as err:
        raise Exception(f"Error al conectar con la base de datos: {err}")

def execute_query(
    query: str,
    params: tuple = (),
    fetchone: bool = False,
    fetchall: bool = False,
    commit: bool = False,
    fetch_lastrowid: bool = False
):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)

        if commit:
            conn.commit()

        if fetch_lastrowid:
            last_id = cursor.lastrowid
            # Limpieza por seguridad
            while cursor.nextset():
                pass
            return last_id

        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        else:
            # Para evitar "Unread result found" si no se especifica fetch
            cursor.fetchall()
            result = None

        # Consumir cualquier resultado adicional
        while cursor.nextset():
            pass

        return result

    except mysql.connector.Error as err:
        raise Exception(f"Error al ejecutar la consulta: {err}")
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


def execute_update(query: str, params: tuple = ()):
    """Ejecuta una consulta SQL que no devuelve resultados (como INSERT, UPDATE, DELETE)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise Exception(f"Error al ejecutar la consulta de actualización: {err}")
    finally:
        cursor.close()
        conn.close()
