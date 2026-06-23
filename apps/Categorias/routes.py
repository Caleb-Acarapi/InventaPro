from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from apps.app import db
from apps.Categorias.models import Categoria
from apps.utils import registrar_bitacora, role_required

bp_categorias = Blueprint(
    "bp_categorias", __name__, template_folder="templates"
)


@bp_categorias.route("/")
@login_required
def listar():
    items = Categoria.query.all()
    return render_template("categorias/listar.html", items=items)


@bp_categorias.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "almacenero")
def crear():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        descripcion = request.form["descripcion"].strip()

        if not nombre:
            flash("El nombre es requerido.", "danger")
            return redirect(url_for("bp_categorias.crear"))

        if Categoria.query.filter_by(nombre=nombre).first():
            flash("Ya existe una categoría con ese nombre.", "danger")
            return redirect(url_for("bp_categorias.crear"))

        nueva = Categoria(nombre=nombre, descripcion=descripcion)
        db.session.add(nueva)
        db.session.commit()

        registrar_bitacora(
            "Crear Categoría", f"Categoría creada: {nombre} (ID: {nueva.id})"
        )
        flash("Categoría creada exitosamente.", "success")
        return redirect(url_for("bp_categorias.listar"))

    return render_template("categorias/crear.html")


@bp_categorias.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin", "almacenero")
def editar(id):
    item = Categoria.query.get_or_404(id)
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        descripcion = request.form["descripcion"].strip()

        if not nombre:
            flash("El nombre es requerido.", "danger")
            return redirect(url_for("bp_categorias.editar", id=id))

        existente = Categoria.query.filter_by(nombre=nombre).first()
        if existente and existente.id != id:
            flash("Ya existe una categoría con ese nombre.", "danger")
            return redirect(url_for("bp_categorias.editar", id=id))

        old_name = item.nombre
        item.nombre = nombre
        item.descripcion = descripcion
        db.session.commit()

        registrar_bitacora(
            "Editar Categoría",
            f"Categoría ID {id} editada de '{old_name}' a '{nombre}'",
        )
        flash("Categoría actualizada exitosamente.", "success")
        return redirect(url_for("bp_categorias.listar"))

    return render_template("categorias/editar.html", item=item)


@bp_categorias.route("/delete/<int:id>", methods=["POST"])
@login_required
@role_required("admin", "almacenero")
def eliminar(id):
    item = Categoria.query.get_or_404(id)
    nombre = item.nombre
    db.session.delete(item)
    db.session.commit()

    registrar_bitacora(
        "Eliminar Categoría", f"Categoría eliminada: {nombre} (ID: {id})"
    )
    flash("Categoría eliminada exitosamente.", "info")
    return redirect(url_for("bp_categorias.listar"))
