import os
from sqlalchemy import create_engine #crea conexión a la base de datos
from sqlalchemy.ext.declarative import declarative_base #clase base para los modelos
from sqlalchemy.orm.session import sessionmaker #crea sesión para la base de datos
from databases import Database # Base de datos asíncrona para usar con 'databases'
from dotenv import load_dotenv # Carga las variables de entorno desde el archivo .env

load_dotenv()

dbName = os.getenv("DB_NAME", "tasklybd")
dbHost = os.getenv("DB_HOST", "localhost")
dbPort = os.getenv("DB_PORT", "3306")
dbUser = os.getenv("DB_USER", "root")
dbPassword = os.getenv("DB_PASSWORD", "root")


# Configuración de la base de datos
DATABASE_URL = f"mysql+mysqlconnector://{dbUser}:{dbPassword}@{dbHost}:{dbPort}/{dbName}"  # Usamos la IP del contenedor

# Base de datos asíncrona para usar con 'databases'
database = Database(DATABASE_URL)

# Conexión síncrona con SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)

# Crea una sesión local para la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()