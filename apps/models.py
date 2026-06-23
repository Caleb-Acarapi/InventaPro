from datetime import datetime
from flask_login import UserMixin
from apps.app import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="vendedor")  # admin | almacenero | vendedor
    is_active_user = db.Column(db.Boolean, default=True)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User {self.username} [{self.role}]>"


class Bitacora(db.Model):
    __tablename__ = "bitacora"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    accion = db.Column(db.String(100), nullable=False)
    detalles = db.Column(db.String(255), nullable=True)

    usuario = db.relationship("User", backref=db.backref("bitacoras", lazy=True))

    def __repr__(self):
        return f"<Bitacora {self.accion} por User #{self.usuario_id}>"
