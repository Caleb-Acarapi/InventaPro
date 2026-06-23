from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from apps.app import bcrypt, db
from apps.auth import auth_bp
from apps.models import User
from apps.utils import registrar_bitacora


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("El nombre de usuario ya existe", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("El correo ya está registrado", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )
        is_first = User.query.count() == 0
        role = "admin" if is_first else "vendedor"
        new_user = User(
            username=username, email=email, password=hashed_password, role=role
        )
        db.session.add(new_user)
        db.session.commit()

        # Log action in bitacora
        registrar_bitacora(
            "Registro de usuario",
            f"Usuario {username} registrado con rol {role}",
        )

        flash(
            "Usuario registrado correctamente. Inicia sesión para continuar.",
            "success",
        )
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("bp_core.index"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            registrar_bitacora("Inicio de sesión", f"Usuario {username} ingresó al sistema")
            flash(f"¡Bienvenido, {user.username}!", "success")
            return redirect(url_for("bp_core.index"))
        flash("Usuario o contraseña incorrectos", "danger")
    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    username = current_user.username
    logout_user()
    registrar_bitacora("Cierre de sesión", f"Usuario {username} salió del sistema")
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("auth.login"))
