from .machines import bp as machines_bp
from .tools import bp as tools_bp
from .maintenance import bp as maintenance_bp
from .dashboard import bp as dashboard_bp

def register_routes(app):
    app.register_blueprint(machines_bp)
    app.register_blueprint(tools_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(dashboard_bp)
