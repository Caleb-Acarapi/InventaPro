from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from apps.app import db
from apps.Categorias.models import Categoria
from apps.Productos.models import Producto
from apps.utils import registrar_bitacora, role_required

bp_productos = Blueprint("bp_productos", __name__, template_folder="templates")


@bp_productos.route("/")
@login_required
def listar():
    items = Producto.query.all()
    return render_template("productos/listar.html", items=items)


@bp_productos.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "almacenero")
def crear():
    categorias = Categoria.query.all()
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        descripcion = request.form["descripcion"].strip()
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])
        stock_minimo = int(request.form["stock_minimo"])
        categoria_id = int(request.form["categoria_id"])

        if not nombre:
            flash("El nombre es requerido.", "danger")
            return redirect(url_for("bp_productos.crear"))

        nuevo = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            stock_minimo=stock_minimo,
            categoria_id=categoria_id,
        )
        db.session.add(nuevo)
        db.session.commit()

        registrar_bitacora(
            "Crear Producto",
            f"Producto creado: {nombre} (Stock: {stock}, Precio: {precio})",
        )
        flash("Producto creado exitosamente.", "success")
        return redirect(url_for("bp_productos.listar"))

    return render_template("productos/crear.html", categorias=categorias)


@bp_productos.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin", "almacenero")
def editar(id):
    item = Producto.query.get_or_404(id)
    categorias = Categoria.query.all()
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        descripcion = request.form["descripcion"].strip()
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])
        stock_minimo = int(request.form["stock_minimo"])
        categoria_id = int(request.form["categoria_id"])

        if not nombre:
            flash("El nombre es requerido.", "danger")
            return redirect(url_for("bp_productos.editar", id=id))

        old_name = item.nombre
        item.nombre = nombre
        item.descripcion = descripcion
        item.precio = precio
        item.stock = stock
        item.stock_minimo = stock_minimo
        item.categoria_id = categoria_id
        db.session.commit()

        registrar_bitacora(
            "Editar Producto",
            f"Producto ID {id} modificado. Nombre: de '{old_name}' a '{nombre}'",
        )
        flash("Producto actualizado exitosamente.", "success")
        return redirect(url_for("bp_productos.listar"))

    return render_template(
        "productos/editar.html", item=item, categorias=categorias
    )


@bp_productos.route("/delete/<int:id>", methods=["POST"])
@login_required
@role_required("admin", "almacenero")
def eliminar(id):
    item = Producto.query.get_or_404(id)
    nombre = item.nombre
    db.session.delete(item)
    db.session.commit()

    registrar_bitacora(
        "Eliminar Producto", f"Producto eliminado: {nombre} (ID: {id})"
    )
    flash("Producto eliminado exitosamente.", "info")
    return redirect(url_for("bp_productos.listar"))
