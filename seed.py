from datetime import datetime
from apps.app import bcrypt, create_app, db
from apps.Categorias.models import Categoria
from apps.Compras.models import Compra, CompraItem
from apps.models import User
from apps.Productos.models import Producto
from apps.Proveedores.models import Proveedor
from apps.Ventas.models import Venta, VentaItem

app = create_app()

with app.app_context():
    # Clear database
    db.drop_all()
    db.create_all()

    print("Base de datos limpia y recreada.")

    # Create admin user
    hashed_pwd = bcrypt.generate_password_hash("admin123").decode("utf-8")
    admin = User(
        username="admin",
        email="admin@inventapro.com",
        password=hashed_pwd,
        role="admin",
    )
    db.session.add(admin)

    # Create other users
    hashed_pwd_almacen = bcrypt.generate_password_hash("almacen123").decode(
        "utf-8"
    )
    almacenero = User(
        username="almacenero",
        email="almacen@inventapro.com",
        password=hashed_pwd_almacen,
        role="almacenero",
    )
    db.session.add(almacenero)

    hashed_pwd_vendedor = bcrypt.generate_password_hash("vendedor123").decode(
        "utf-8"
    )
    vendedor = User(
        username="vendedor",
        email="vendedor@inventapro.com",
        password=hashed_pwd_vendedor,
        role="vendedor",
    )
    db.session.add(vendedor)

    # Create categories
    cat_electronica = Categoria(
        nombre="Electrónica",
        descripcion="Dispositivos, gadgets y accesorios electrónicos",
    )
    cat_ropa = Categoria(
        nombre="Ropa & Calzado",
        descripcion="Prendas de vestir para adultos y niños",
    )
    cat_alimentos = Categoria(
        nombre="Alimentos & Bebidas",
        descripcion="Productos perecederos y comestibles",
    )
    db.session.add_all([cat_electronica, cat_ropa, cat_alimentos])
    db.session.commit()  # Commit to get IDs

    # Create suppliers
    prov1 = Proveedor(
        empresa="Tech Bolivia S.A.",
        contacto="Carlos Perez",
        telefono="78945612",
        email="ventas@techbolivia.com",
    )
    prov2 = Proveedor(
        empresa="Textiles Andinos",
        contacto="Maria Quispe",
        telefono="65478912",
        email="maria@textilesandinos.com",
    )
    db.session.add_all([prov1, prov2])
    db.session.commit()

    # Create products
    p1 = Producto(
        nombre="Auriculares Inalámbricos",
        descripcion="Auriculares Bluetooth cancelacion de ruido",
        precio=120.0,
        stock=20,
        stock_minimo=5,
        categoria_id=cat_electronica.id,
    )
    p2 = Producto(
        nombre="Mouse Gamer RGB",
        descripcion="Mouse óptico 6400 DPI",
        precio=85.0,
        stock=15,
        stock_minimo=5,
        categoria_id=cat_electronica.id,
    )
    p3 = Producto(
        nombre="Casaca de Jean",
        descripcion="Chaqueta clásica de mezclilla",
        precio=250.0,
        stock=8,
        stock_minimo=3,
        categoria_id=cat_ropa.id,
    )
    p4 = Producto(
        nombre="Zapatillas Deportivas",
        descripcion="Zapatillas para running talla 41",
        precio=380.0,
        stock=4,
        stock_minimo=5,
        categoria_id=cat_ropa.id,
    )  # stock bajo!
    p5 = Producto(
        nombre="Café Premium 500g",
        descripcion="Café tostado de grano yungueño",
        precio=45.0,
        stock=30,
        stock_minimo=10,
        categoria_id=cat_alimentos.id,
    )
    db.session.add_all([p1, p2, p3, p4, p5])
    db.session.commit()

    # Create a purchase (Compra)
    compra = Compra(
        proveedor_id=prov1.id, user_id=admin.id, fecha=datetime.utcnow(), total=0.0
    )
    db.session.add(compra)
    db.session.commit()

    item_c1 = CompraItem(
        compra_id=compra.id, producto_id=p1.id, cantidad=10, precio_unitario=80.0
    )
    item_c2 = CompraItem(
        compra_id=compra.id, producto_id=p2.id, cantidad=5, precio_unitario=50.0
    )
    db.session.add_all([item_c1, item_c2])
    compra.total = (10 * 80.0) + (5 * 50.0)
    db.session.commit()

    # Create a sale (Venta)
    venta = Venta(user_id=vendedor.id, fecha=datetime.utcnow(), total=0.0)
    db.session.add(venta)
    db.session.commit()

    item_v1 = VentaItem(
        venta_id=venta.id,
        producto_id=p1.id,
        cantidad=2,
        precio_unitario=p1.precio,
    )
    item_v2 = VentaItem(
        venta_id=venta.id,
        producto_id=p5.id,
        cantidad=4,
        precio_unitario=p5.precio,
    )
    db.session.add_all([item_v1, item_v2])
    venta.total = (2 * p1.precio) + (4 * p5.precio)
    db.session.commit()

    print("Datos de prueba sembrados exitosamente.")
    print("Usuarios creados:")
    print("  - admin / admin123  (Rol: admin)")
    print("  - almacenero / almacen123 (Rol: almacenero)")
    print("  - vendedor / vendedor123 (Rol: vendedor)")
