from datetime import datetime
from apps.app import db


class Venta(db.Model):
    __tablename__ = "ventas"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    usuario = db.relationship("User")
    items = db.relationship(
        "VentaItem", back_populates="venta", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Venta #{self.id} - {self.fecha}>"


class VentaItem(db.Model):
    __tablename__ = "venta_items"

    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey("ventas.id"), nullable=False)
    producto_id = db.Column(
        db.Integer, db.ForeignKey("productos.id"), nullable=False
    )
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    venta = db.relationship("Venta", back_populates="items")
    producto = db.relationship("Producto", back_populates="venta_items")

    def __repr__(self):
        return f"<VentaItem venta={self.venta_id} prod={self.producto_id}>"
