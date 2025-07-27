from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# =====================
# Configuración de la base de datos PostgreSQL
# =====================

# Variables de entorno para la conexión
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'librosdb')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '172.24.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# URL de conexión para SQLAlchemy
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Crear el engine y la sesión
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.
    Cierra la sesión automáticamente al finalizar la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
