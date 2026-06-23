from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from apps.app import db
from apps.models import Bitacora


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if current_user.role not in roles:
                flash("No tienes permiso para acceder a esta sección.", "danger")
                return redirect(url_for("bp_core.index"))
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def registrar_bitacora(accion, detalles=None):
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        log_entry = Bitacora(usuario_id=user_id, accion=accion, detalles=detalles)
        db.session.add(log_entry)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error registrando bitácora: {e}")
