from apps.app import db


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    stock_minimo = db.Column(db.Integer, default=5)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    categoria = db.relationship("Categoria", back_populates="productos")
    compra_items = db.relationship("CompraItem", back_populates="producto")
    venta_items = db.relationship("VentaItem", back_populates="producto")

    def __repr__(self):
        return f"<Producto {self.nombre}>"
