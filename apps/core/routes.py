from datetime import datetime, timedelta
from flask import Blueprint, render_template
from flask_login import current_user, login_required
from apps.app import db
from apps.Compras.models import Compra
from apps.models import Bitacora
from apps.Productos.models import Producto
from apps.Proveedores.models import Proveedor
from apps.Ventas.models import Venta
from sqlalchemy import func

bp_core = Blueprint("bp_core", __name__, template_folder="templates")


@bp_core.route("/")
@login_required
def index():
    productos_count = Producto.query.count()
    ventas_count = Venta.query.count()
    compras_count = Compra.query.count()
    proveedores_count = Proveedor.query.count()

    # Productos con stock bajo
    productos_bajos = Producto.query.filter(
        Producto.stock <= Producto.stock_minimo
    ).all()

    # Últimas 5 ventas
    ultimas_ventas = Venta.query.order_by(Venta.fecha.desc()).limit(5).all()

    # Últimos 5 registros de bitácora
    recientes_bitacora = (
        Bitacora.query.order_by(Bitacora.fecha.desc()).limit(5).all()
    )

    # Total vendido (suma de todos los totales de venta)
    total_ventas = db.session.query(func.sum(Venta.total)).scalar() or 0

    # Ventas por día (últimos 7 días) para Chart.js
    hoy = datetime.utcnow().date()
    labels = []
    data_ventas = []
    for i in range(6, -1, -1):
        dia = hoy - timedelta(days=i)
        labels.append(dia.strftime("%d/%m"))
        # Filter where sale date matches the day
        total_dia = (
            db.session.query(func.sum(Venta.total))
            .filter(func.date(Venta.fecha) == dia)
            .scalar()
            or 0
        )
        data_ventas.append(float(total_dia))

    return render_template(
        "core/index.html",
        productos_count=productos_count,
        ventas_count=ventas_count,
        compras_count=compras_count,
        proveedores_count=proveedores_count,
        productos_bajos=productos_bajos,
        ultimas_ventas=ultimas_ventas,
        recientes_bitacora=recientes_bitacora,
        total_ventas=total_ventas,
        chart_labels=labels,
        chart_data=data_ventas,
    )
