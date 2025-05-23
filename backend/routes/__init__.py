from .machines import bp as machines_bp
from .tools import bp as tools_bp
from .maintenance import bp as maintenance_bp
from .dashboard import bp as dashboard_bp
from .admin_routes import bp as admin_routes_bp
from .users import bp as users_bp

def register_routes(app):
    app.register_blueprint(machines_bp)
    app.register_blueprint(tools_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_routes_bp)
    app.register_blueprint(users_bp)
