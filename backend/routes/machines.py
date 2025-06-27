from flask import Blueprint, jsonify, request
from datetime import datetime
from models import db, Machine, ToolAssignment, MachineMetric, Tool, ToolMetric

bp = Blueprint('machines', __name__)

@bp.route('/machines', methods=['GET'])
def get_machines():
    """
    Get a paginated list of machines with their latest status
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Page number
      - name: per_page
        in: query
        type: integer
        required: false
        default: 30
        description: Number of machines per page
    responses:
      200:
        description: List of machines
        schema:
          type: object
          properties:
            machines:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  category:
                    type: string
                  group:
                    type: string
                  manufacturer:
                    type: string
                  created_at:
                    type: string
                    format: date
                  status:
                    type: string
            total:
              type: integer
            page:
              type: integer
            pages:
              type: integer
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)

    machines_paginated = Machine.query.paginate(page=page, per_page=per_page, error_out=False)
    machines = machines_paginated.items

    latest_metrics = (
        db.session.query(MachineMetric)
        .distinct(MachineMetric.machine_id)
        .order_by(MachineMetric.machine_id, MachineMetric.id.desc())
        .all()
    )

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
            "status": latest_status_map.get(m.id)
        })

    return jsonify({
        "machines": machine_list,
        "total": machines_paginated.total,
        "page": machines_paginated.page,
        "pages": machines_paginated.pages
    })


@bp.route('/machines', methods=['POST'])
def add_machine():
    """
    Add a new machine
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: machine
        required: true
        schema:
          type: object
          required:
            - name
            - category
            - group
            - manufacturer
            - created_at
          properties:
            name:
              type: string
              example: "Machine X"
            category:
              type: string
              example: "Lathe"
            group:
              type: string
              example: "Heavy Duty"
            manufacturer:
              type: string
              example: "ABC Corp"
            created_at:
              type: string
              format: date-time
              example: "2024-06-23T10:00:00"
    responses:
      201:
        description: Machine added successfully
      400:
        description: Missing field
      500:
        description: Internal server error
    """
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
    """
    Delete a machine by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the machine to delete
    responses:
      200:
        description: Machine deleted successfully
      404:
        description: Machine not found
    """
    machine = Machine.query.get(id)
    if not machine:
        return jsonify({"error": "Machine not found"}), 404

    db.session.delete(machine)
    db.session.commit()
    return jsonify({"message": "Machine deleted successfully!"})


@bp.route('/machines/<int:machine_id>/tool', methods=['PUT'])
def update_machine_tool(machine_id):
    """
    Assign or update a tool for a machine
    ---
    parameters:
      - name: machine_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - tool_id
          properties:
            tool_id:
              type: integer
              example: 3
    responses:
      200:
        description: Tool assigned successfully
      400:
        description: tool_id is required
    """
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
    """
    Get the tool assigned to a machine
    ---
    parameters:
      - name: machine_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Tool info
        schema:
          type: object
          properties:
            tool_name:
              type: string
              example: "Drill Bit A"
            wear_level:
              type: number
              example: 15.2
    """
    assignment = ToolAssignment.query.filter_by(machine_id=machine_id).first()
    
    if assignment is None:
        return jsonify({"tool_name": None, "wear_level": None}), 200

    tool = Tool.query.get(assignment.tool_id)
    metric = ToolMetric.query.filter_by(tool_id=tool.id).first()

    return jsonify({
        "tool_name": tool.name if tool else None,
        "wear_level": metric.wear_level if metric else None
    }), 200
