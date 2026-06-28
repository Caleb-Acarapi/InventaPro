import os
from datetime import datetime, timedelta
from apps.app import bcrypt, create_app, db
from apps.Categorias.models import Categoria
from apps.Compras.models import Compra, CompraItem
from apps.models import Bitacora, User
from apps.Productos.models import Producto
from apps.Proveedores.models import Proveedor
from apps.Ventas.models import Venta, VentaItem

app = create_app()

with app.app_context():
    # Ensure instance folder exists
    instance_path = app.instance_path
    os.makedirs(instance_path, exist_ok=True)

    # Clear database
    db.drop_all()
    db.create_all()

    print("Base de datos limpia y recreada en:", os.path.join(instance_path, "inventapro.db"))

    # ─── USERS ────────────────────────────────────────────────
    admin = User(
        username="admin",
        email="admin@inventapro.com",
        password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
        role="admin",
    )
    almacenero = User(
        username="almacenero",
        email="almacen@inventapro.com",
        password=bcrypt.generate_password_hash("almacen123").decode("utf-8"),
        role="almacenero",
    )
    vendedor1 = User(
        username="vendedor",
        email="vendedor@inventapro.com",
        password=bcrypt.generate_password_hash("vendedor123").decode("utf-8"),
        role="vendedor",
    )
    vendedor2 = User(
        username="ana",
        email="ana@inventapro.com",
        password=bcrypt.generate_password_hash("ana123").decode("utf-8"),
        role="vendedor",
    )
    db.session.add_all([admin, almacenero, vendedor1, vendedor2])
    db.session.commit()

    # ─── CATEGORIES ──────────────────────────────────────────
    cat_electronica = Categoria(nombre="Electrónica", descripcion="Dispositivos, gadgets y accesorios electrónicos")
    cat_ropa = Categoria(nombre="Ropa & Calzado", descripcion="Prendas de vestir para adultos y niños")
    cat_alimentos = Categoria(nombre="Alimentos & Bebidas", descripcion="Productos perecederos y comestibles")
    cat_hogar = Categoria(nombre="Hogar", descripcion="Artículos para el hogar y limpieza")
    cat_deportes = Categoria(nombre="Deportes", descripcion="Equipamiento e indumentaria deportiva")
    cat_libreria = Categoria(nombre="Librería", descripcion="Útiles escolares y de oficina")
    db.session.add_all([cat_electronica, cat_ropa, cat_alimentos, cat_hogar, cat_deportes, cat_libreria])
    db.session.commit()

    # ─── SUPPLIERS ───────────────────────────────────────────
    prov_tech = Proveedor(empresa="Tech Bolivia S.A.", contacto="Carlos Perez", telefono="78945612", email="ventas@techbolivia.com")
    prov_textiles = Proveedor(empresa="Textiles Andinos", contacto="Maria Quispe", telefono="65478912", email="maria@textilesandinos.com")
    prov_alimentos = Proveedor(empresa="Distribuidora Yungueña", contacto="Pedro Mamani", telefono="62134567", email="pedro@dyunguena.com")
    prov_hogar = Proveedor(empresa="Hogar Total Ltda.", contacto="Lucia Fernandez", telefono="71234567", email="lucia@hogartotal.com")
    prov_deportes = Proveedor(empresa="Deportes Beni", contacto="Jorge Rojas", telefono="77889900", email="jorge@deportesbeni.com")
    prov_libreria = Proveedor(empresa="Papelera Central", contacto="Rosa Choque", telefono="61234567", email="rosa@papcentral.com")
    db.session.add_all([prov_tech, prov_textiles, prov_alimentos, prov_hogar, prov_deportes, prov_libreria])
    db.session.commit()

    # ─── PRODUCTS ────────────────────────────────────────────
    p1 = Producto(nombre="Auriculares Inalámbricos", descripcion="Auriculares Bluetooth cancelación de ruido", precio=120.0, stock=20, stock_minimo=5, categoria_id=cat_electronica.id)
    p2 = Producto(nombre="Mouse Gamer RGB", descripcion="Mouse óptico 6400 DPI", precio=85.0, stock=15, stock_minimo=5, categoria_id=cat_electronica.id)
    p3 = Producto(nombre="Teclado Mecánico", descripcion="Teclado mecánico RGB switches rojos", precio=280.0, stock=10, stock_minimo=3, categoria_id=cat_electronica.id)
    p4 = Producto(nombre="Monitor 24\" LED", descripcion="Monitor Full HD 60Hz", precio=450.0, stock=7, stock_minimo=2, categoria_id=cat_electronica.id)
    p5 = Producto(nombre="Cable USB-C 2m", descripcion="Cable de carga y datos USB-C", precio=25.0, stock=50, stock_minimo=20, categoria_id=cat_electronica.id)
    p6 = Producto(nombre="Casaca de Jean", descripcion="Chaqueta clásica de mezclilla", precio=250.0, stock=8, stock_minimo=3, categoria_id=cat_ropa.id)
    p7 = Producto(nombre="Zapatillas Deportivas", descripcion="Zapatillas para running talla 41", precio=380.0, stock=4, stock_minimo=5, categoria_id=cat_ropa.id)
    p8 = Producto(nombre="Camisa Polo", descripcion="Camisa manga corta algodón talla M", precio=120.0, stock=12, stock_minimo=5, categoria_id=cat_ropa.id)
    p9 = Producto(nombre="Chamarra Impermeable", descripcion="Chamarra cortaviento ligera", precio=320.0, stock=6, stock_minimo=3, categoria_id=cat_ropa.id)
    p10 = Producto(nombre="Café Premium 500g", descripcion="Café tostado de grano yungueño", precio=45.0, stock=30, stock_minimo=10, categoria_id=cat_alimentos.id)
    p11 = Producto(nombre="Té de Coca 100u", descripcion="Té de coca natural boliviano", precio=18.0, stock=40, stock_minimo=15, categoria_id=cat_alimentos.id)
    p12 = Producto(nombre="Agua Mineral 2L", descripcion="Agua mineral sin gas", precio=8.0, stock=60, stock_minimo=20, categoria_id=cat_alimentos.id)
    p13 = Producto(nombre="Quinua Real 1kg", descripcion="Quinua real orgánica", precio=35.0, stock=25, stock_minimo=10, categoria_id=cat_alimentos.id)
    p14 = Producto(nombre="Detergente Líquido 1L", descripcion="Detergente multiusos", precio=22.0, stock=35, stock_minimo=10, categoria_id=cat_hogar.id)
    p15 = Producto(nombre="Escobillón", descripcion="Escobillón de aluminio con repuesto", precio=40.0, stock=15, stock_minimo=5, categoria_id=cat_hogar.id)
    p16 = Producto(nombre="Balde Plástico 10L", descripcion="Balde reforzado color surtido", precio=18.0, stock=20, stock_minimo=8, categoria_id=cat_hogar.id)
    p17 = Producto(nombre="Pelota de Fútbol", descripcion="Pelota profesional talla 5", precio=95.0, stock=10, stock_minimo=3, categoria_id=cat_deportes.id)
    p18 = Producto(nombre="Pesas 2kg", descripcion="Mancuernas de neopreno par", precio=65.0, stock=8, stock_minimo=4, categoria_id=cat_deportes.id)
    p19 = Producto(nombre="Cuerda para Saltar", descripcion="Cuerda ajustable con mango ergonómico", precio=30.0, stock=14, stock_minimo=5, categoria_id=cat_deportes.id)
    p20 = Producto(nombre="Cuaderno Universitario", descripcion="Cuaderno 100 hojas cosido", precio=15.0, stock=80, stock_minimo=20, categoria_id=cat_libreria.id)
    p21 = Producto(nombre="Bolígrafo Azul 4u", descripcion="Paquete de bolígrafos tinta azul", precio=7.0, stock=200, stock_minimo=50, categoria_id=cat_libreria.id)
    p22 = Producto(nombre="Mochila Escolar", descripcion="Mochila acolchada con compartimento laptop", precio=110.0, stock=9, stock_minimo=5, categoria_id=cat_libreria.id)
    db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22])
    db.session.commit()

    # ─── PURCHASES ──────────────────────────────────────────
    today = datetime.utcnow()

    # Compra 1 — Electrónicos
    c1 = Compra(proveedor_id=prov_tech.id, user_id=admin.id, fecha=today - timedelta(days=60), total=0.0)
    db.session.add(c1)
    db.session.commit()
    c1_items = [
        CompraItem(compra_id=c1.id, producto_id=p1.id, cantidad=15, precio_unitario=80.0),
        CompraItem(compra_id=c1.id, producto_id=p2.id, cantidad=10, precio_unitario=50.0),
        CompraItem(compra_id=c1.id, producto_id=p3.id, cantidad=5, precio_unitario=180.0),
        CompraItem(compra_id=c1.id, producto_id=p5.id, cantidad=50, precio_unitario=12.0),
    ]
    db.session.add_all(c1_items)
    c1.total = sum(i.cantidad * i.precio_unitario for i in c1_items)
    db.session.commit()

    # Compra 2 — Ropa
    c2 = Compra(proveedor_id=prov_textiles.id, user_id=almacenero.id, fecha=today - timedelta(days=50), total=0.0)
    db.session.add(c2)
    db.session.commit()
    c2_items = [
        CompraItem(compra_id=c2.id, producto_id=p6.id, cantidad=10, precio_unitario=150.0),
        CompraItem(compra_id=c2.id, producto_id=p7.id, cantidad=8, precio_unitario=250.0),
        CompraItem(compra_id=c2.id, producto_id=p8.id, cantidad=15, precio_unitario=70.0),
        CompraItem(compra_id=c2.id, producto_id=p9.id, cantidad=6, precio_unitario=200.0),
    ]
    db.session.add_all(c2_items)
    c2.total = sum(i.cantidad * i.precio_unitario for i in c2_items)
    db.session.commit()

    # Compra 3 — Alimentos
    c3 = Compra(proveedor_id=prov_alimentos.id, user_id=almacenero.id, fecha=today - timedelta(days=40), total=0.0)
    db.session.add(c3)
    db.session.commit()
    c3_items = [
        CompraItem(compra_id=c3.id, producto_id=p10.id, cantidad=40, precio_unitario=28.0),
        CompraItem(compra_id=c3.id, producto_id=p11.id, cantidad=50, precio_unitario=10.0),
        CompraItem(compra_id=c3.id, producto_id=p12.id, cantidad=80, precio_unitario=4.0),
        CompraItem(compra_id=c3.id, producto_id=p13.id, cantidad=30, precio_unitario=22.0),
    ]
    db.session.add_all(c3_items)
    c3.total = sum(i.cantidad * i.precio_unitario for i in c3_items)
    db.session.commit()

    # Compra 4 — Hogar
    c4 = Compra(proveedor_id=prov_hogar.id, user_id=admin.id, fecha=today - timedelta(days=30), total=0.0)
    db.session.add(c4)
    db.session.commit()
    c4_items = [
        CompraItem(compra_id=c4.id, producto_id=p14.id, cantidad=40, precio_unitario=13.0),
        CompraItem(compra_id=c4.id, producto_id=p15.id, cantidad=20, precio_unitario=25.0),
        CompraItem(compra_id=c4.id, producto_id=p16.id, cantidad=25, precio_unitario=10.0),
    ]
    db.session.add_all(c4_items)
    c4.total = sum(i.cantidad * i.precio_unitario for i in c4_items)
    db.session.commit()

    # Compra 5 — Deportes
    c5 = Compra(proveedor_id=prov_deportes.id, user_id=almacenero.id, fecha=today - timedelta(days=20), total=0.0)
    db.session.add(c5)
    db.session.commit()
    c5_items = [
        CompraItem(compra_id=c5.id, producto_id=p17.id, cantidad=12, precio_unitario=60.0),
        CompraItem(compra_id=c5.id, producto_id=p18.id, cantidad=10, precio_unitario=40.0),
        CompraItem(compra_id=c5.id, producto_id=p19.id, cantidad=20, precio_unitario=18.0),
    ]
    db.session.add_all(c5_items)
    c5.total = sum(i.cantidad * i.precio_unitario for i in c5_items)
    db.session.commit()

    # Compra 6 — Librería
    c6 = Compra(proveedor_id=prov_libreria.id, user_id=admin.id, fecha=today - timedelta(days=15), total=0.0)
    db.session.add(c6)
    db.session.commit()
    c6_items = [
        CompraItem(compra_id=c6.id, producto_id=p20.id, cantidad=100, precio_unitario=8.0),
        CompraItem(compra_id=c6.id, producto_id=p21.id, cantidad=300, precio_unitario=3.5),
        CompraItem(compra_id=c6.id, producto_id=p22.id, cantidad=10, precio_unitario=60.0),
    ]
    db.session.add_all(c6_items)
    c6.total = sum(i.cantidad * i.precio_unitario for i in c6_items)
    db.session.commit()

    # Compra 7 — Reposición Electrónicos
    c7 = Compra(proveedor_id=prov_tech.id, user_id=almacenero.id, fecha=today - timedelta(days=7), total=0.0)
    db.session.add(c7)
    db.session.commit()
    c7_items = [
        CompraItem(compra_id=c7.id, producto_id=p4.id, cantidad=5, precio_unitario=320.0),
        CompraItem(compra_id=c7.id, producto_id=p5.id, cantidad=30, precio_unitario=12.0),
    ]
    db.session.add_all(c7_items)
    c7.total = sum(i.cantidad * i.precio_unitario for i in c7_items)
    db.session.commit()

    # ─── SALES ──────────────────────────────────────────────
    v1 = Venta(user_id=vendedor1.id, fecha=today - timedelta(days=55), total=0.0)
    db.session.add(v1)
    db.session.commit()
    v1_items = [
        VentaItem(venta_id=v1.id, producto_id=p1.id, cantidad=2, precio_unitario=p1.precio),
        VentaItem(venta_id=v1.id, producto_id=p5.id, cantidad=5, precio_unitario=p5.precio),
    ]
    db.session.add_all(v1_items)
    v1.total = sum(i.cantidad * i.precio_unitario for i in v1_items)
    db.session.commit()

    v2 = Venta(user_id=vendedor2.id, fecha=today - timedelta(days=45), total=0.0)
    db.session.add(v2)
    db.session.commit()
    v2_items = [
        VentaItem(venta_id=v2.id, producto_id=p6.id, cantidad=1, precio_unitario=p6.precio),
        VentaItem(venta_id=v2.id, producto_id=p8.id, cantidad=3, precio_unitario=p8.precio),
        VentaItem(venta_id=v2.id, producto_id=p10.id, cantidad=2, precio_unitario=p10.precio),
    ]
    db.session.add_all(v2_items)
    v2.total = sum(i.cantidad * i.precio_unitario for i in v2_items)
    db.session.commit()

    v3 = Venta(user_id=vendedor1.id, fecha=today - timedelta(days=35), total=0.0)
    db.session.add(v3)
    db.session.commit()
    v3_items = [
        VentaItem(venta_id=v3.id, producto_id=p3.id, cantidad=1, precio_unitario=p3.precio),
        VentaItem(venta_id=v3.id, producto_id=p4.id, cantidad=1, precio_unitario=p4.precio),
    ]
    db.session.add_all(v3_items)
    v3.total = sum(i.cantidad * i.precio_unitario for i in v3_items)
    db.session.commit()

    v4 = Venta(user_id=vendedor2.id, fecha=today - timedelta(days=28), total=0.0)
    db.session.add(v4)
    db.session.commit()
    v4_items = [
        VentaItem(venta_id=v4.id, producto_id=p14.id, cantidad=3, precio_unitario=p14.precio),
        VentaItem(venta_id=v4.id, producto_id=p15.id, cantidad=1, precio_unitario=p15.precio),
        VentaItem(venta_id=v4.id, producto_id=p16.id, cantidad=2, precio_unitario=p16.precio),
        VentaItem(venta_id=v4.id, producto_id=p11.id, cantidad=4, precio_unitario=p11.precio),
    ]
    db.session.add_all(v4_items)
    v4.total = sum(i.cantidad * i.precio_unitario for i in v4_items)
    db.session.commit()

    v5 = Venta(user_id=vendedor1.id, fecha=today - timedelta(days=21), total=0.0)
    db.session.add(v5)
    db.session.commit()
    v5_items = [
        VentaItem(venta_id=v5.id, producto_id=p17.id, cantidad=2, precio_unitario=p17.precio),
        VentaItem(venta_id=v5.id, producto_id=p19.id, cantidad=3, precio_unitario=p19.precio),
        VentaItem(venta_id=v5.id, producto_id=p7.id, cantidad=1, precio_unitario=p7.precio),
    ]
    db.session.add_all(v5_items)
    v5.total = sum(i.cantidad * i.precio_unitario for i in v5_items)
    db.session.commit()

    v6 = Venta(user_id=vendedor2.id, fecha=today - timedelta(days=14), total=0.0)
    db.session.add(v6)
    db.session.commit()
    v6_items = [
        VentaItem(venta_id=v6.id, producto_id=p20.id, cantidad=10, precio_unitario=p20.precio),
        VentaItem(venta_id=v6.id, producto_id=p21.id, cantidad=20, precio_unitario=p21.precio),
        VentaItem(venta_id=v6.id, producto_id=p22.id, cantidad=1, precio_unitario=p22.precio),
        VentaItem(venta_id=v6.id, producto_id=p2.id, cantidad=2, precio_unitario=p2.precio),
    ]
    db.session.add_all(v6_items)
    v6.total = sum(i.cantidad * i.precio_unitario for i in v6_items)
    db.session.commit()

    v7 = Venta(user_id=vendedor1.id, fecha=today - timedelta(days=7), total=0.0)
    db.session.add(v7)
    db.session.commit()
    v7_items = [
        VentaItem(venta_id=v7.id, producto_id=p10.id, cantidad=5, precio_unitario=p10.precio),
        VentaItem(venta_id=v7.id, producto_id=p12.id, cantidad=12, precio_unitario=p12.precio),
        VentaItem(venta_id=v7.id, producto_id=p13.id, cantidad=3, precio_unitario=p13.precio),
    ]
    db.session.add_all(v7_items)
    v7.total = sum(i.cantidad * i.precio_unitario for i in v7_items)
    db.session.commit()

    v8 = Venta(user_id=vendedor2.id, fecha=today - timedelta(days=3), total=0.0)
    db.session.add(v8)
    db.session.commit()
    v8_items = [
        VentaItem(venta_id=v8.id, producto_id=p1.id, cantidad=1, precio_unitario=p1.precio),
        VentaItem(venta_id=v8.id, producto_id=p9.id, cantidad=2, precio_unitario=p9.precio),
        VentaItem(venta_id=v8.id, producto_id=p6.id, cantidad=1, precio_unitario=p6.precio),
    ]
    db.session.add_all(v8_items)
    v8.total = sum(i.cantidad * i.precio_unitario for i in v8_items)
    db.session.commit()

    v9 = Venta(user_id=vendedor1.id, fecha=today - timedelta(days=1), total=0.0)
    db.session.add(v9)
    db.session.commit()
    v9_items = [
        VentaItem(venta_id=v9.id, producto_id=p18.id, cantidad=2, precio_unitario=p18.precio),
        VentaItem(venta_id=v9.id, producto_id=p3.id, cantidad=1, precio_unitario=p3.precio),
        VentaItem(venta_id=v9.id, producto_id=p5.id, cantidad=3, precio_unitario=p5.precio),
        VentaItem(venta_id=v9.id, producto_id=p11.id, cantidad=6, precio_unitario=p11.precio),
    ]
    db.session.add_all(v9_items)
    v9.total = sum(i.cantidad * i.precio_unitario for i in v9_items)
    db.session.commit()

    v10 = Venta(user_id=vendedor2.id, fecha=today, total=0.0)
    db.session.add(v10)
    db.session.commit()
    v10_items = [
        VentaItem(venta_id=v10.id, producto_id=p8.id, cantidad=2, precio_unitario=p8.precio),
        VentaItem(venta_id=v10.id, producto_id=p2.id, cantidad=1, precio_unitario=p2.precio),
        VentaItem(venta_id=v10.id, producto_id=p14.id, cantidad=2, precio_unitario=p14.precio),
        VentaItem(venta_id=v10.id, producto_id=p20.id, cantidad=5, precio_unitario=p20.precio),
    ]
    db.session.add_all(v10_items)
    v10.total = sum(i.cantidad * i.precio_unitario for i in v10_items)
    db.session.commit()

    # ─── AUDIT LOG (BITACORA) ────────────────────────────
    bitacora_entries = [
        Bitacora(usuario_id=admin.id, accion="Crear compra",
                 detalles=f"Compra #{c1.id} a {prov_tech.empresa} por Bs.{c1.total:.2f}", fecha=c1.fecha),
        Bitacora(usuario_id=almacenero.id, accion="Crear compra",
                 detalles=f"Compra #{c2.id} a {prov_textiles.empresa} por Bs.{c2.total:.2f}", fecha=c2.fecha),
        Bitacora(usuario_id=almacenero.id, accion="Crear compra",
                 detalles=f"Compra #{c3.id} a {prov_alimentos.empresa} por Bs.{c3.total:.2f}", fecha=c3.fecha),
        Bitacora(usuario_id=admin.id, accion="Crear compra",
                 detalles=f"Compra #{c4.id} a {prov_hogar.empresa} por Bs.{c4.total:.2f}", fecha=c4.fecha),
        Bitacora(usuario_id=almacenero.id, accion="Crear compra",
                 detalles=f"Compra #{c5.id} a {prov_deportes.empresa} por Bs.{c5.total:.2f}", fecha=c5.fecha),
        Bitacora(usuario_id=admin.id, accion="Crear compra",
                 detalles=f"Compra #{c6.id} a {prov_libreria.empresa} por Bs.{c6.total:.2f}", fecha=c6.fecha),
        Bitacora(usuario_id=almacenero.id, accion="Crear compra",
                 detalles=f"Compra #{c7.id} a {prov_tech.empresa} por Bs.{c7.total:.2f}", fecha=c7.fecha),
        Bitacora(usuario_id=vendedor1.id, accion="Crear venta",
                 detalles=f"Venta #{v1.id} por Bs.{v1.total:.2f}", fecha=v1.fecha),
        Bitacora(usuario_id=vendedor2.id, accion="Crear venta",
                 detalles=f"Venta #{v2.id} por Bs.{v2.total:.2f}", fecha=v2.fecha),
        Bitacora(usuario_id=vendedor1.id, accion="Crear venta",
                 detalles=f"Venta #{v3.id} por Bs.{v3.total:.2f}", fecha=v3.fecha),
        Bitacora(usuario_id=vendedor2.id, accion="Crear venta",
                 detalles=f"Venta #{v4.id} por Bs.{v4.total:.2f}", fecha=v4.fecha),
        Bitacora(usuario_id=vendedor1.id, accion="Crear venta",
                 detalles=f"Venta #{v5.id} por Bs.{v5.total:.2f}", fecha=v5.fecha),
        Bitacora(usuario_id=vendedor2.id, accion="Crear venta",
                 detalles=f"Venta #{v6.id} por Bs.{v6.total:.2f}", fecha=v6.fecha),
        Bitacora(usuario_id=vendedor1.id, accion="Crear venta",
                 detalles=f"Venta #{v7.id} por Bs.{v7.total:.2f}", fecha=v7.fecha),
        Bitacora(usuario_id=vendedor2.id, accion="Crear venta",
                 detalles=f"Venta #{v8.id} por Bs.{v8.total:.2f}", fecha=v8.fecha),
        Bitacora(usuario_id=vendedor1.id, accion="Crear venta",
                 detalles=f"Venta #{v9.id} por Bs.{v9.total:.2f}", fecha=v9.fecha),
        Bitacora(usuario_id=vendedor2.id, accion="Crear venta",
                 detalles=f"Venta #{v10.id} por Bs.{v10.total:.2f}", fecha=v10.fecha),
    ]
    db.session.add_all(bitacora_entries)
    db.session.commit()

    # ─── SUMMARY ─────────────────────────────────────────────
    print("Datos de prueba sembrados exitosamente.\n")
    print(f"Usuarios:     {User.query.count()}")
    print(f"Categorías:   {Categoria.query.count()}")
    print(f"Proveedores:  {Proveedor.query.count()}")
    print(f"Productos:    {Producto.query.count()}")
    print(f"Compras:      {Compra.query.count()} (con {CompraItem.query.count()} items)")
    print(f"Ventas:       {Venta.query.count()} (con {VentaItem.query.count()} items)")
    print(f"Bitácora:     {Bitacora.query.count()} registros\n")
    print("Usuarios creados:")
    print("  admin      / admin123      (admin)")
    print("  almacenero / almacen123    (almacenero)")
    print("  vendedor   / vendedor123   (vendedor)")
    print("  ana        / ana123        (vendedor)")
