from extensions import db  # Importa la instancia de db ya definida


class Genero(db.Model):
    __tablename__ = "generos"
    idGenero = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genNombre = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Genero {self.genNombre}>"
