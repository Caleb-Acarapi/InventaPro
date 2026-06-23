from apps.app import db


class Proveedor(db.Model):
    __tablename__ = "proveedores"

    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String(150), nullable=False)
    contacto = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(150))
    compras = db.relationship("Compra", back_populates="proveedor")

    def __repr__(self):
        return f"<Proveedor {self.empresa}>"
