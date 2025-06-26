from flask_sqlalchemy import SQLAlchemy

# Inicializamos SQLAlchemy sin pasarle la aplicación aún.
# La vinculación se hará en la fábrica de la aplicación.
db = SQLAlchemy()
