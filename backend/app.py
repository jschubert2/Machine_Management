from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
#from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allows frontend to access backend
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mesuser:mespass@localhost:5432/mesdb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/mesdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Machine Model
class Machine(db.Model):
    __tablename__ = 'machines' #new
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

class Tool(db.Model):
    __tablename__ = 'tools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False) #default=datetime.now()
    metrics = db.relationship('ToolMetrics', backref='tool', lazy=True)

class MaintenanceLog(db.Model):
    __tablename__ = 'maintenance_logs'
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'),nullable=False)
    performed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
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

class ToolMetric(db.Model):
    __tablename__ = 'tool_metrics'
    id = db.Column(db.Integer, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    storage_location = db.Column(db.String(100), nullable=False)
    wear_level = db.Column(db.Integer, nullable=False)


class ToolAssignment(db.Model):
    __tablename__ = 'tool_assignment'
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'), primary_key=True)





#with app.app_context():
    #db.drop_all() #Delete all Tables of DB
    #db.create_all() #Create all Tables based on classes of this file

    #Machine.__table__.drop(db.engine) #Delete Specific table
    #Machine.__table__.create(db.engine)

#machine_view
@app.route('/machines', methods=['GET'])
def get_machines():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)

    machines_paginated = Machine.query.paginate(page=page, per_page=per_page, error_out=False)

    machine_list = [
        {
            "id": m.id,
            "name": m.name,
            "category": m.category,
            "group": m.group,
            "manufacturer": m.manufacturer,
            "created_at": m.created_at.isoformat()
        } for m in machines_paginated.items
    ]

    return jsonify({
        "machines": machine_list,
        "total": machines_paginated.total,
        "page": machines_paginated.page,
        "pages": machines_paginated.pages
    })
#def sort_machines(param):

#redundant
@app.route('/machines', methods=['POST'])
def add_machine():
    data = request.json
    required_fields = ['name', 'category', 'group', 'manufacturer', 'created_at']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        new_machine = Machine(
            name=data['name'],
            category=data['category'],
            group=data['group'],
            manufacturer=data['manufacturer'],
            created_at=datetime.fromisoformat(data['created_at'])
        )
        db.session.add(new_machine)
        db.session.commit()
        return jsonify({"message": "Machine added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#redundant
@app.route('/machines/<int:id>', methods=['DELETE'])
def delete_machine(id):
    machine = Machine.query.get(id)
    if not machine:
        return jsonify({"error": "Machine not found"}), 404

    db.session.delete(machine)
    db.session.commit()
    return jsonify({"message": "Machine deleted successfully!"})

#tool_assignment
@app.route('/machines/<int:machine_id>/tool', methods=['PUT'])
def update_machine_tool(machine_id):
    data = request.json
    new_tool_id = data.get("tool_id")

    if not new_tool_id:
        return jsonify({"error": "tool_id is required"}), 400

    assignment = ToolAssignment.query.get(machine_id)

    if assignment:
        assignment.tool_id = new_tool_id  # update existing
    else:
        assignment = ToolAssignment(machine_id=machine_id, tool_id=new_tool_id)  # create new
        db.session.add(assignment)

    db.session.commit()

    return jsonify({"message": f"Tool assigned to machine {machine_id} updated successfully."})

#tool view
@app.route('/tools', methods=['GET'])
def get_tools():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)

    tools_paginated = Tool.query.paginate(page=page, per_page=per_page, error_out=False)

    result = []
    for tool in tools_paginated.items:
        tool_data = {
            "id": tool.id,
            "name": tool.name,
            "type": tool.type,
            "created_at": tool.created_at.isoformat(),
            "metrics": []
        }

        for metric in tool.metrics:
            tool_data["metrics"].append({
                "id": metric.id,
                "status": metric.status,
                "storage_location": metric.storage_location,
                "wear_level": metric.wear_level
            })

        result.append(tool_data)

    return jsonify({
        "tools": result,
        "total": tools_paginated.total,
        "page": tools_paginated.page,
        "pages": tools_paginated.pages
    })

#dashboard
@app.route('/machines/<int:machine_id>/dashboard/<string:param>', methods=['GET'])
def get_machine_metric(machine_id, param):
    allowed_params = {'oee', 'availability', 'performance', 'output_quality', 'status'}
    if param not in allowed_params:
        return jsonify({"error": f"Invalid parameter '{param}'. Must be one of {list(allowed_params)}."}), 400

    days = request.args.get('days', type=int)  # e.g. ?days=30

    query = MachineMetric.query.filter_by(machine_id=machine_id).order_by(MachineMetric.timestamp.desc())

    if days:
        query = query.limit(days)

    metrics = query.all()

    # Reverse to chronological order (oldest to newest)
    metrics.reverse()

    result = [
        {
            "timestamp": m.timestamp.isoformat(),
            param: getattr(m, param)
        } for m in metrics
    ]

    return jsonify({
        "machine_id": machine_id,
        "metric": param,
        "days_requested": days,
        "data": result
    })

#maintenance
@app.route('/machines/<int:machine_id>/maintenance', methods=['GET'])
def get_machine_maintenance(machine_id):
    logs = MaintenanceLog.query.filter_by(machine_id=machine_id).order_by(MaintenanceLog.date.asc()).all()

    data = [
        {
            "id": log.id,
            "machine_id": log.machine_id,
            "performed_by": log.performed_by,
            "date": log.date.isoformat(),
            "notes": log.notes,
            "planned": log.planned
        }
        for log in logs
    ]

    return jsonify({
        "machine_id": machine_id,
        "maintenance_logs": data
    })

@app.route('/maintenance', methods=['POST'])
def add_maintenance():
    data = request.get_json()

    # Input validation (basic)
    required_fields = ['machine_id', 'performed_by', 'notes', 'date']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        maintenance = MaintenanceLog(
            machine_id=data['machine_id'],
            performed_by=data['performed_by'],
            notes=data['notes'],
            date=datetime.fromisoformat(data['date']),  # expects ISO 8601 date string
            planned=False #the maintenance was performed, so it is not planned
        )

        db.session.add(maintenance)
        db.session.commit()
        return jsonify({"message": "Maintenance log added successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)


#testing area:
#with app.test_client() as client:
    #response = client.get('/machines')
    #print(response.get_json())  # prints the JSON response from the endpoint

    #response = client.post('/machines',json={"name": "CNC Router", "status": "Running"}) # this is the test data
    #print("Add response:", response.get_json())  # should print {"message": "Machine added successfully!"}