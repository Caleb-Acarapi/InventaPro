from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from apps.app import db
from apps.Proveedores.models import Proveedor
from apps.utils import registrar_bitacora, role_required

bp_proveedores = Blueprint(
    "bp_proveedores", __name__, template_folder="templates"
)


@bp_proveedores.route("/")
@login_required
def listar():
    items = Proveedor.query.all()
    return render_template("proveedores/listar.html", items=items)


@bp_proveedores.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "almacenero")
def crear():
    if request.method == "POST":
        empresa = request.form["empresa"].strip()
        contacto = request.form["contacto"].strip()
        telefono = request.form["telefono"].strip()
        email = request.form["email"].strip()

        if not empresa:
            flash("La empresa es requerida.", "danger")
            return redirect(url_for("bp_proveedores.crear"))

        nuevo = Proveedor(
            empresa=empresa, contacto=contacto, telefono=telefono, email=email
        )
        db.session.add(nuevo)
        db.session.commit()

        registrar_bitacora(
            "Crear Proveedor",
            f"Proveedor creado: {empresa} (Contacto: {contacto})",
        )
        flash("Proveedor creado exitosamente.", "success")
        return redirect(url_for("bp_proveedores.listar"))

    return render_template("proveedores/crear.html")


@bp_proveedores.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin", "almacenero")
def editar(id):
    item = Proveedor.query.get_or_404(id)
    if request.method == "POST":
        empresa = request.form["empresa"].strip()
        contacto = request.form["contacto"].strip()
        telefono = request.form["telefono"].strip()
        email = request.form["email"].strip()

        if not empresa:
            flash("La empresa es requerida.", "danger")
            return redirect(url_for("bp_proveedores.editar", id=id))

        old_name = item.empresa
        item.empresa = empresa
        item.contacto = contacto
        item.telefono = telefono
        item.email = email
        db.session.commit()

        registrar_bitacora(
            "Editar Proveedor",
            f"Proveedor ID {id} editado. Empresa de '{old_name}' a '{empresa}'",
        )
        flash("Proveedor actualizado exitosamente.", "success")
        return redirect(url_for("bp_proveedores.listar"))

    return render_template("proveedores/editar.html", item=item)


@bp_proveedores.route("/delete/<int:id>", methods=["POST"])
@login_required
@role_required("admin", "almacenero")
def eliminar(id):
    item = Proveedor.query.get_or_404(id)
    empresa = item.empresa
    db.session.delete(item)
    db.session.commit()

    registrar_bitacora(
        "Eliminar Proveedor", f"Proveedor eliminado: {empresa} (ID: {id})"
    )
    flash("Proveedor eliminado exitosamente.", "info")
    return redirect(url_for("bp_proveedores.listar"))
