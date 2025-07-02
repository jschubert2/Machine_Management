from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Machine(db.Model):
    """
    Represents a machine in the factory.

    WHY: Stores technical and categorization info for each machine used in production or maintenance.
    """
    __tablename__ = 'machines' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False) #default="Manual"
    group = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

class User(db.Model):
    """
    Stores user credentials and roles.

    WHY: Differentiates admin and technician access. Used for login/authentication.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False) #default=datetime.now()

class ToolMetric(db.Model):
    """
    Describes real-time condition and location data for a tool.

    WHY: Helps track tool availability, degradation, and physical storage.
    """
    __tablename__ = 'tool_metrics'
    id = db.Column(db.Integer, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    storage_location = db.Column(db.String(100), nullable=False)
    wear_level = db.Column(db.Integer, nullable=False)

class Tool(db.Model):
    """
    Represents a physical tool used by machines.

    WHY: Tracks tool identity and type. Links to metrics via one-to-many relationship.
    """
    __tablename__ = 'tools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False) #default=datetime.now()
    metrics = db.relationship('ToolMetric', backref='tool', lazy=True)

class MaintenanceLog(db.Model):
    """
    Logs a maintenance action performed on a machine.

    WHY: Useful for maintenance history tracking and preventive maintenance strategies.
    """
    __tablename__ = 'maintenance_logs'
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'),nullable=False)
    performed_by = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.DateTime, nullable=False) #default=datetime.now()
    notes = db.Column(db.Text)
    planned = db.Column(db.Boolean, nullable=False)
    performer = db.relationship('User', backref='maintenance_logs')

class MachineMetric(db.Model):
    """
    Daily performance metrics for a machine.

    WHY: Used for dashboard analytics (OEE, availability, etc.)
    """
    __tablename__ = 'machine_metrics'
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'),nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)  # default=datetime.now()
    oee = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Float, nullable=False)
    performance = db.Column(db.Float, nullable=False)
    output_quality = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)

class ToolAssignment(db.Model):
    """
    Represents a fixed assignment between a tool and a machine.

    WHY: Prevents random re-use and enforces 1-to-1 mapping (unique constraint on machine_id).
    """
    __tablename__ = 'tool_assignment'
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), unique=True, nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'), nullable=False)