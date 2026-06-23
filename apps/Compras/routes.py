from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from apps.app import db
from apps.Compras.models import Compra, CompraItem
from apps.Productos.models import Producto
from apps.Proveedores.models import Proveedor
from apps.utils import registrar_bitacora, role_required

bp_compras = Blueprint("bp_compras", __name__, template_folder="templates")


@bp_compras.route("/")
@login_required
def listar():
    items = Compra.query.order_by(Compra.fecha.desc()).all()
    return render_template("compras/listar.html", items=items)


@bp_compras.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "almacenero")
def crear():
    proveedores = Proveedor.query.all()
    productos = Producto.query.all()

    if request.method == "POST":
        proveedor_id = int(request.form["proveedor_id"])
        producto_ids = request.form.getlist("producto_id[]")
        cantidades = request.form.getlist("cantidad[]")
        precios = request.form.getlist("precio_unitario[]")

        if not proveedor_id:
            flash("El proveedor es requerido.", "danger")
            return redirect(url_for("bp_compras.crear"))

        if not producto_ids or len(producto_ids) == 0:
            flash("Debe agregar al menos un producto.", "danger")
            return redirect(url_for("bp_compras.crear"))

        compra = Compra(proveedor_id=proveedor_id, user_id=current_user.id, total=0.0)
        db.session.add(compra)

        total_compra = 0.0
        items_added = 0

        for prod_id, cant_str, prec_str in zip(producto_ids, cantidades, precios):
            if not prod_id or not cant_str or not prec_str:
                continue

            pid = int(prod_id)
            cantidad = int(cant_str)
            precio_unitario = float(prec_str)

            if cantidad <= 0 or precio_unitario < 0:
                continue

            # Buscar producto
            producto = Producto.query.get(pid)
            if not producto:
                continue

            # Crear item
            item = CompraItem(
                compra=compra,
                producto_id=pid,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
            )
            db.session.add(item)

            # Actualizar stock del producto
            producto.stock += cantidad
            total_compra += cantidad * precio_unitario
            items_added += 1

        if items_added == 0:
            db.session.rollback()
            flash("No se agregaron productos válidos.", "danger")
            return redirect(url_for("bp_compras.crear"))

        compra.total = total_compra
        db.session.commit()

        registrar_bitacora(
            "Crear Compra",
            f"Compra #{compra.id} registrada a Proveedor ID {proveedor_id} por un total de {total_compra} Bs. ({items_added} ítems)",
        )
        flash("Compra registrada exitosamente.", "success")
        return redirect(url_for("bp_compras.listar"))

    return render_template(
        "compras/crear.html", proveedores=proveedores, productos=productos
    )


@bp_compras.route("/delete/<int:id>", methods=["POST"])
@login_required
@role_required("admin", "almacenero")
def eliminar(id):
    compra = Compra.query.get_or_404(id)

    # Revertir stock de los productos
    for item in compra.items:
        producto = Producto.query.get(item.producto_id)
        if producto:
            producto.stock = max(0, producto.stock - item.cantidad)

    total = compra.total
    db.session.delete(compra)
    db.session.commit()

    registrar_bitacora(
        "Eliminar Compra",
        f"Compra #{id} eliminada. Revertido el stock de los productos. Total era: {total} Bs.",
    )
    flash(
        "Compra eliminada y stock de productos revertido exitosamente.", "info"
    )
    return redirect(url_for("bp_compras.listar"))
