import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "inventapro-dev-key-2026"
    )

    db_url = os.environ.get("DATABASE_URL", "sqlite:///inventapro.db")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        from apps.models import User

        return User.query.get(int(user_id))

    # Import and register blueprints
    from apps.auth import auth_bp
    from apps.Categorias.routes import bp_categorias
    from apps.Compras.routes import bp_compras
    from apps.core.routes import bp_core
    from apps.Productos.routes import bp_productos
    from apps.Proveedores.routes import bp_proveedores
    from apps.Ventas.routes import bp_ventas

    app.register_blueprint(bp_core)
    app.register_blueprint(auth_bp)
    app.register_blueprint(bp_categorias, url_prefix="/categorias")
    app.register_blueprint(bp_productos, url_prefix="/productos")
    app.register_blueprint(bp_proveedores, url_prefix="/proveedores")
    app.register_blueprint(bp_compras, url_prefix="/compras")
    app.register_blueprint(bp_ventas, url_prefix="/ventas")

    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy metadata
        from apps.models import User, Bitacora
        from apps.Categorias.models import Categoria
        from apps.Productos.models import Producto
        from apps.Proveedores.models import Proveedor
        from apps.Compras.models import Compra, CompraItem
        from apps.Ventas.models import Venta, VentaItem

        db.create_all()

    return app
