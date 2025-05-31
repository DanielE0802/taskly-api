import os
import mysql.connector
from mysql.connector import Error, MySQLConnection
from mysql.connector.connection_cext import CMySQLConnection
from dotenv import load_dotenv
from typing import Any, List, Optional, Union

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DATABASE_USERNAME", "root"),
    "password": os.getenv("DATABASE_PASSWORD", "root"),
    "database": os.getenv("DATABASE", "tasklydb"),
}

def get_db_connection():
    """
    Crea y devuelve una conexión a la base de datos MySQL.
    Lanza RuntimeError en caso de fallo.
    """
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as err:
        raise RuntimeError(f"Error al conectar con la base de datos: {err}")

def execute_query(
    query: str,
    params: Optional[tuple[Any, ...]] = None,
    *,
    fetchone: bool = False,
    fetchall: bool = False,
    commit: bool = False,
    return_lastrowid: bool = False
):
    """
    Ejecuta una consulta SQL según los flags:
      - fetchone: devuelve un dict con una fila
      - fetchall: devuelve una lista de dicts
      - commit: hace commit (para INSERT/UPDATE/DELETE)
      - return_lastrowid: devuelve cursor.lastrowid
    En caso de error lanza RuntimeError.
    """
    params = params or ()
    result = None

    try:
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)

                if commit:
                    conn.commit()

                if return_lastrowid:
                    result = cursor.lastrowid
                elif fetchone:
                    result = cursor.fetchone()
                elif fetchall:
                    result = cursor.fetchall()

    except Error as err:
        raise RuntimeError(f"Error al ejecutar la consulta: {err}")

    return result


def execute_update(query: str, params: tuple[Any, ...] = ()) -> None:
    """
    Ejecuta un INSERT/UPDATE/DELETE y confirma la transacción.
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
    except Error as err:
        raise RuntimeError(f"Error al ejecutar la consulta de actualización: {err}")
