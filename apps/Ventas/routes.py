from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from apps.app import db
from apps.Productos.models import Producto
from apps.utils import registrar_bitacora, role_required
from apps.Ventas.models import Venta, VentaItem

bp_ventas = Blueprint("bp_ventas", __name__, template_folder="templates")


@bp_ventas.route("/")
@login_required
def listar():
    items = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template("ventas/listar.html", items=items)


@bp_ventas.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "vendedor")
def crear():
    productos = Producto.query.all()

    if request.method == "POST":
        producto_ids = request.form.getlist("producto_id[]")
        cantidades = request.form.getlist("cantidad[]")

        if not producto_ids or len(producto_ids) == 0:
            flash("Debe agregar al menos un producto.", "danger")
            return redirect(url_for("bp_ventas.crear"))

        venta = Venta(user_id=current_user.id, total=0.0)
        db.session.add(venta)

        total_venta = 0.0
        items_added = 0

        # Primero, validar que todos los productos seleccionados tengan suficiente stock
        stock_valido = True
        productos_a_validar = {}  # prod_id -> cantidad acumulada en este form

        for prod_id, cant_str in zip(producto_ids, cantidades):
            if not prod_id or not cant_str:
                continue

            pid = int(prod_id)
            cantidad = int(cant_str)

            if cantidad <= 0:
                continue

            productos_a_validar[pid] = productos_a_validar.get(pid, 0) + cantidad

        for pid, cantidad in productos_a_validar.items():
            producto = Producto.query.get(pid)
            if not producto or producto.stock < cantidad:
                stock_valido = False
                nombre_prod = producto.nombre if producto else f"ID {pid}"
                stock_actual = producto.stock if producto else 0
                flash(
                    f"Stock insuficiente para '{nombre_prod}'. Solicitado: {cantidad}, Disponible: {stock_actual}.",
                    "danger",
                )
                break

        if not stock_valido:
            db.session.rollback()
            return redirect(url_for("bp_ventas.crear"))

        # Si todo tiene stock, procesar la venta
        for prod_id, cant_str in zip(producto_ids, cantidades):
            if not prod_id or not cant_str:
                continue

            pid = int(prod_id)
            cantidad = int(cant_str)

            if cantidad <= 0:
                continue

            producto = Producto.query.get(pid)
            if not producto:
                continue

            item = VentaItem(
                venta=venta,
                producto_id=pid,
                cantidad=cantidad,
                precio_unitario=producto.precio,
            )
            db.session.add(item)

            # Restar stock
            producto.stock -= cantidad
            total_venta += cantidad * producto.precio
            items_added += 1

        if items_added == 0:
            db.session.rollback()
            flash("No se agregaron productos válidos.", "danger")
            return redirect(url_for("bp_ventas.crear"))

        venta.total = total_venta
        db.session.commit()

        registrar_bitacora(
            "Crear Venta",
            f"Venta #{venta.id} registrada por {current_user.username} por un total de {total_venta} Bs. ({items_added} ítems)",
        )
        flash("Venta registrada exitosamente.", "success")
        return redirect(url_for("bp_ventas.listar"))

    return render_template("ventas/crear.html", productos=productos)


@bp_ventas.route("/delete/<int:id>", methods=["POST"])
@login_required
@role_required("admin")
def eliminar(id):
    venta = Venta.query.get_or_404(id)

    # Revertir stock de los productos
    for item in venta.items:
        producto = Producto.query.get(item.producto_id)
        if producto:
            producto.stock += item.cantidad

    total = venta.total
    db.session.delete(venta)
    db.session.commit()

    registrar_bitacora(
        "Eliminar Venta",
        f"Venta #{id} eliminada por admin. Stock de productos restablecido. Total era: {total} Bs.",
    )
    flash(
        "Venta eliminada y stock de productos restablecido exitosamente.",
        "info",
    )
    return redirect(url_for("bp_ventas.listar"))
