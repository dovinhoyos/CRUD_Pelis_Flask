import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


class Config:
    """Clase base de configuración."""

    # Obtener credenciales de la base de datos de las variables de entorno
    DB_USER = os.getenv(
        "DB_USER", "root"
    )  # 'root' como valor por defecto si no se encuentra
    DB_PASSWORD = os.getenv(
        "DB_PASSWORD", "root"
    )  # Poner una contraseña por defecto segura o None
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "gestionpeliculas")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Configuración para el entorno de desarrollo."""

    DEBUG = True


class ProductionConfig(Config):
    """Configuración para el entorno de producción."""

    DEBUG = False
    # Podrías añadir más configuraciones específicas de producción aquí
    # Por ejemplo, diferentes credenciales de DB o logs.


# Mapea los nombres de configuración a las clases
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
