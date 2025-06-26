from flask import Blueprint, jsonify, request, current_app
from extensions import db  # Importa la instancia de db desde extensions
from models.pelicula import Pelicula  # Importa el modelo Pelicula
from models.genero import (
    Genero,
)  # Importa el modelo Genero para validación y relaciones
from sqlalchemy import exc

# Define el Blueprint para las películas
pelicula_bp = Blueprint("pelicula_api", __name__, url_prefix="/peliculas")


@pelicula_bp.route("/", methods=["GET"])
def listar_peliculas():
    """
    Lista todas las películas disponibles, incluyendo detalles del género.
    """
    try:
        peliculas = Pelicula.query.all()
        lista_peliculas = []
        for p in peliculas:
            pelicula_data = {
                "idPelicula": p.idPelicula,
                "codigo": p.pelCodigo,
                "titulo": p.pelTitulo,
                "protagonista": p.pelProtagonista,
                "duracion": p.pelDuracion,
                "resumen": p.pelResumen,
                "foto": p.pelFoto,
                "genero": {"idGenero": p.genero.idGenero, "nombre": p.genero.genNombre}
                if p.genero
                else None,  # Maneja el caso si genero es None
            }
            lista_peliculas.append(pelicula_data)

        return jsonify(
            {
                "mensaje": "Lista de películas obtenida exitosamente",
                "peliculas": lista_peliculas,
            }
        ), 200

    except exc.SQLAlchemyError as error:
        current_app.logger.error(
            f"Error de SQLAlchemy al listar películas: {str(error)}"
        )
        return jsonify(
            {"error": "Error interno del servidor al obtener películas"}
        ), 500
    except Exception as e:
        current_app.logger.error(f"Error inesperado al listar películas: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500


@pelicula_bp.route("/", methods=["POST"])
def crear_pelicula():
    """
    Crea una nueva película.
    Requiere un JSON con todos los campos obligatorios.
    """
    try:
        data = request.get_json()

        # Validar campos obligatorios
        required_fields = [
            "pelCodigo",
            "pelTitulo",
            "pelProtagonista",
            "pelDuracion",
            "pelResumen",
            "pelFoto",
            "pelGenero",
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

        # Validar que el ID de género exista
        genero_existente = Genero.query.get(data["pelGenero"])
        if not genero_existente:
            return jsonify({"error": "El ID de género proporcionado no existe"}), 400

        nueva_pelicula = Pelicula(
            pelCodigo=data["pelCodigo"],
            pelTitulo=data["pelTitulo"],
            pelProtagonista=data["pelProtagonista"],
            pelDuracion=data["pelDuracion"],
            pelResumen=data["pelResumen"],
            pelFoto=data["pelFoto"],
            pelGenero=data["pelGenero"],
        )

        db.session.add(nueva_pelicula)
        db.session.commit()

        return jsonify(
            {
                "mensaje": "Película creada exitosamente",
                "idPelicula": nueva_pelicula.idPelicula,
                "titulo": nueva_pelicula.pelTitulo,
            }
        ), 201

    except exc.IntegrityError:
        db.session.rollback()
        current_app.logger.error(
            "Error de integridad al crear película (código duplicado o FK inválida)."
        )
        return jsonify(
            {
                "error": "Error de datos: El código de película ya existe o el ID de género es inválido."
            }
        ), 409
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        current_app.logger.error(f"Error de SQLAlchemy al crear película: {str(error)}")
        return jsonify({"error": "Error interno del servidor al crear película"}), 500
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error inesperado al crear película: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500


# Puedes añadir más rutas para GET por ID, PUT y DELETE aquí.
# Ejemplo de GET por ID:
@pelicula_bp.route("/<int:pelicula_id>", methods=["GET"])
def obtener_pelicula_por_id(pelicula_id):
    """
    Obtiene una película por su ID.
    """
    pelicula = Pelicula.query.get(pelicula_id)
    if not pelicula:
        return jsonify({"mensaje": "Película no encontrada"}), 404

    pelicula_data = {
        "idPelicula": pelicula.idPelicula,
        "codigo": pelicula.pelCodigo,
        "titulo": pelicula.pelTitulo,
        "protagonista": pelicula.pelProtagonista,
        "duracion": pelicula.pelDuracion,
        "resumen": pelicula.pelResumen,
        "foto": pelicula.pelFoto,
        "genero": {
            "idGenero": pelicula.genero.idGenero,
            "nombre": pelicula.genero.genNombre,
        }
        if pelicula.genero
        else None,
    }
    return jsonify(pelicula_data), 200
