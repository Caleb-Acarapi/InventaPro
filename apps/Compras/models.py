from datetime import datetime
from apps.app import db


class Compra(db.Model):
    __tablename__ = "compras"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total = db.Column(db.Float, default=0.0)
    proveedor_id = db.Column(
        db.Integer, db.ForeignKey("proveedores.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    proveedor = db.relationship("Proveedor", back_populates="compras")
    usuario = db.relationship("User")
    items = db.relationship(
        "CompraItem", back_populates="compra", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Compra #{self.id} - {self.fecha}>"


class CompraItem(db.Model):
    __tablename__ = "compra_items"

    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(
        db.Integer, db.ForeignKey("compras.id"), nullable=False
    )
    producto_id = db.Column(
        db.Integer, db.ForeignKey("productos.id"), nullable=False
    )
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    compra = db.relationship("Compra", back_populates="items")
    producto = db.relationship("Producto", back_populates="compra_items")

    def __repr__(self):
        return f"<CompraItem compra={self.compra_id} prod={self.producto_id}>"
