from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Machine(db.Model):
    __tablename__ = 'machines' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False) #default="Manual"
    group = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False) #default=datetime.now()

class ToolMetric(db.Model):
    __tablename__ = 'tool_metrics'
    id = db.Column(db.Integer, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    storage_location = db.Column(db.String(100), nullable=False)
    wear_level = db.Column(db.Integer, nullable=False)

class Tool(db.Model):
    __tablename__ = 'tools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False) #default=datetime.now()
    metrics = db.relationship('ToolMetric', backref='tool', lazy=True)

class MaintenanceLog(db.Model):
    __tablename__ = 'maintenance_logs'
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'),nullable=False)
    #performed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    performed_by = db.Column(db.String(50))
    date = db.Column(db.DateTime, nullable=False) #default=datetime.now()
    notes = db.Column(db.Text)
    planned = db.Column(db.Boolean, nullable=False)

class MachineMetric(db.Model):
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
    __tablename__ = 'tool_assignment'
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), unique=True, nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'), nullable=False)