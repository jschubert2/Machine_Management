from flask import Blueprint, jsonify, request
from datetime import datetime
from models import db, Machine, ToolAssignment, MachineMetric, Tool, ToolMetric

bp = Blueprint('machines', __name__)

@bp.route('/machines', methods=['GET'])
def get_machines():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)

    machines_paginated = Machine.query.paginate(page=page, per_page=per_page, error_out=False)
    machines = machines_paginated.items

    # Get latest metrics for each machine
    latest_metrics = (
        db.session.query(MachineMetric)
        .distinct(MachineMetric.machine_id)
        .order_by(MachineMetric.machine_id, MachineMetric.id.desc())
        .all()
    )

    # Map machine_id to status
    latest_status_map = {metric.machine_id: metric.status for metric in latest_metrics}

    machine_list = []
    for m in machines:
        machine_list.append({
            "id": m.id,
            "name": m.name,
            "category": m.category,
            "group": m.group,
            "manufacturer": m.manufacturer,
            "created_at": m.created_at.strftime('%Y-%m-%d'),
            "status": latest_status_map.get(m.id)  # May be None if no metrics exist yet
        })

    return jsonify({
        "machines": machine_list,
        "total": machines_paginated.total,
        "page": machines_paginated.page,
        "pages": machines_paginated.pages
    })

@bp.route('/machines', methods=['POST'])
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

@bp.route('/machines/<int:id>', methods=['DELETE'])
def delete_machine(id):
    machine = Machine.query.get(id)
    if not machine:
        return jsonify({"error": "Machine not found"}), 404

    db.session.delete(machine)
    db.session.commit()
    return jsonify({"message": "Machine deleted successfully!"})

@bp.route('/machines/<int:machine_id>/tool', methods=['PUT'])
def update_machine_tool(machine_id):
    data = request.json
    new_tool_id = data.get("tool_id")

    if not new_tool_id:
        return jsonify({"error": "tool_id is required"}), 400

    assignment = ToolAssignment.query.get(machine_id)

    if assignment:
        assignment.tool_id = new_tool_id
    else:
        assignment = ToolAssignment(machine_id=machine_id, tool_id=new_tool_id)  
        db.session.add(assignment)

    db.session.commit()

    return jsonify({"message": f"Tool assigned to machine {machine_id} updated successfully."})

@bp.route('/machines/<int:machine_id>/tool', methods=['GET'])
def get_machine_tool(machine_id):
    assignment = ToolAssignment.query.filter_by(machine_id=machine_id).first()
    
    if assignment is None:
        return jsonify({"tool_name": None, "wear_level": None}), 200

    tool = Tool.query.get(assignment.tool_id)
    metric = ToolMetric.query.filter_by(tool_id=tool.id).first()

    return jsonify({
        "tool_name": tool.name if tool else None,
        "wear_level": metric.wear_level if metric else None
    }), 200