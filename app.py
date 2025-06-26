from flask import Flask
from config import config_by_name  # Importa la configuración
from extensions import db  # Importa la instancia de db (sin app aún)


def create_app(config_name="default"):
    """
    Crea y configura la instancia de la aplicación Flask.

    Args:
        config_name (str): Nombre de la configuración a cargar (ej. 'development', 'production').

    Returns:
        Flask: La instancia de la aplicación Flask configurada.
    """
    app = Flask(__name__)

    # Carga la configuración de la aplicación
    app.config.from_object(config_by_name[config_name])

    # Inicializa las extensiones de Flask con la aplicación
    # Ahora 'db' está vinculado a esta instancia de 'app'
    db.init_app(app)

    # Importa y registra los Blueprints (las rutas de la API)
    # Es crucial que estas importaciones se hagan AQUÍ, después de db.init_app(app),
    # para evitar problemas de importación circular y asegurar que 'db' esté listo.
    from routes.genero import genero_bp
    from routes.pelicula import pelicula_bp

    app.register_blueprint(genero_bp)
    app.register_blueprint(pelicula_bp)

    # Importa los modelos para que db.create_all() pueda descubrirlos.
    # No es necesario asignarles un nombre si solo se importan para db.create_all().
    import models.genero
    import models.pelicula

    # Crea las tablas de la base de datos si no existen.
    # Esto se hace dentro del contexto de la aplicación, ya que db está vinculado.
    with app.app_context():
        db.create_all()

    # Ruta de prueba simple
    @app.route("/")
    def index():
        return "¡API Flask de Gestión de Películas funcionando!"

    return app


# Punto de entrada principal para ejecutar la aplicación
if __name__ == "__main__":
    # Puedes cambiar 'development' a 'production' según tu necesidad
    app_instance = create_app("development")
    app_instance.run(port=5400, debug=True)
