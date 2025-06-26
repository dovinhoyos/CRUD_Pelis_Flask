from flask import Blueprint, jsonify, request, current_app
from extensions import db  # Importa la instancia de db desde extensions
from models.genero import Genero  # Importa el modelo Genero
from sqlalchemy import exc

# Define el Blueprint para los géneros
# url_prefix es una buena práctica para agrupar rutas bajo un prefijo
genero_bp = Blueprint("genero_api", __name__, url_prefix="/generos")


@genero_bp.route("/", methods=["GET"])
def listar_generos():
    """
    Lista todos los géneros disponibles.
    """
    try:
        generos = Genero.query.all()
        lista_generos = []
        for g in generos:
            genero_data = {"idGenero": g.idGenero, "nombre": g.genNombre}
            lista_generos.append(genero_data)

        return jsonify(
            {
                "mensaje": "Lista de géneros obtenida exitosamente",
                "generos": lista_generos,
            }
        ), 200

    except exc.SQLAlchemyError as error:
        # Registra el error para depuración en el servidor
        current_app.logger.error(f"Error de SQLAlchemy al listar géneros: {str(error)}")
        return jsonify({"error": "Error interno del servidor al obtener géneros"}), 500
    except Exception as e:
        current_app.logger.error(f"Error inesperado al listar géneros: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500


@genero_bp.route("/", methods=["POST"])
def crear_genero():
    """
    Crea un nuevo género.
    Requiere un JSON con el campo 'genNombre'.
    """
    try:
        data = request.get_json()
        if not data or "genNombre" not in data:
            return jsonify({"error": "Se requiere el campo 'genNombre'"}), 400

        nuevo_genero = Genero(genNombre=data["genNombre"])

        db.session.add(nuevo_genero)
        db.session.commit()

        return jsonify(
            {"mensaje": "Género creado exitosamente", "idGenero": nuevo_genero.idGenero}
        ), 201

    except exc.IntegrityError:
        db.session.rollback()  # Deshacer la transacción en caso de error de unicidad
        return jsonify({"error": "El nombre de género ya existe"}), 409  # Conflict
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        current_app.logger.error(f"Error de SQLAlchemy al crear género: {str(error)}")
        return jsonify({"error": "Error interno del servidor al crear género"}), 500
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error inesperado al crear género: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500


# Puedes añadir más rutas para GET por ID, PUT y DELETE aquí
# Ejemplo de GET por ID:
@genero_bp.route("/<int:genero_id>", methods=["GET"])
def obtener_genero_por_id(genero_id):
    """
    Obtiene un género por su ID.
    """
    genero = Genero.query.get(genero_id)
    if not genero:
        return jsonify({"mensaje": "Género no encontrado"}), 404

    return jsonify({"idGenero": genero.idGenero, "nombre": genero.genNombre}), 200
