from extensions import db  # Importa la instancia de db
from sqlalchemy import Text  # Importa Text si lo usas
from models.genero import Genero  # Importa el modelo Genero para la relación


class Pelicula(db.Model):
    __tablename__ = "peliculas"
    idPelicula = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pelCodigo = db.Column(db.String(9), nullable=False, unique=True)
    pelTitulo = db.Column(db.String(50), nullable=False)
    pelProtagonista = db.Column(db.String(50), nullable=False)
    pelDuracion = db.Column(db.Integer, nullable=False)
    pelResumen = db.Column(db.Text, nullable=False)
    pelFoto = db.Column(db.String(45), nullable=False)
    # Define la clave foránea usando el nombre de la columna en la tabla 'generos'
    pelGenero = db.Column(db.Integer, db.ForeignKey("generos.idGenero"), nullable=False)

    # Relación entre Pelicula y Genero
    # 'Genero' es el nombre de la clase del modelo
    # backref='peliculas' creará una propiedad 'peliculas' en el objeto Genero
    # que será una lista de películas asociadas a ese género.
    genero = db.relationship("Genero", backref=db.backref("peliculas", lazy=True))

    def __repr__(self):
        return f"<Pelicula {self.pelTitulo}>"
