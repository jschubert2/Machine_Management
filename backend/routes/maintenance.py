from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, MaintenanceLog

bp = Blueprint('maintenance', __name__)

@bp.route('/machines/<int:machine_id>/maintenance', methods=['GET'])
def get_machine_maintenance(machine_id):
    """
    Get maintenance logs for a specific machine
    ---
    parameters:
      - name: machine_id
        in: path
        type: integer
        required: true
        description: ID of the machine
    responses:
      200:
        description: A list of maintenance logs for the given machine
        schema:
          type: object
          properties:
            machine_id:
              type: integer
              example: 5
            maintenance_logs:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 12
                  machine_id:
                    type: integer
                    example: 5
                  performed_by:
                    type: string
                    example: "Technician A"
                  date:
                    type: string
                    format: date
                    example: "2024-06-20"
                  notes:
                    type: string
                    example: "Replaced belt and lubricated motor"
                  planned:
                    type: boolean
                    example: false
    """
    logs = MaintenanceLog.query.filter_by(machine_id=machine_id).order_by(MaintenanceLog.date.asc()).all()

    data = [
        {
            "id": log.id,
            "machine_id": log.machine_id,
            "performed_by": log.performed_by,
            "date": log.date.strftime('%Y-%m-%d'),
            "notes": log.notes,
            "planned": log.planned
        }
        for log in logs
    ]

    return jsonify({
        "machine_id": machine_id,
        "maintenance_logs": data
    })


@bp.route('/maintenance', methods=['POST'])
def add_maintenance():
    """
    Add a new maintenance log
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: maintenance
        required: true
        schema:
          type: object
          required:
            - machine_id
            - performed_by
            - notes
            - date
            - planned
          properties:
            machine_id:
              type: integer
              example: 5
            performed_by:
              type: string
              example: "Technician A"
            notes:
              type: string
              example: "Routine inspection and oiling"
            date:
              type: string
              format: date-time
              example: "2024-06-22T10:00:00"
            planned:
              type: boolean
              example: true
    responses:
      201:
        description: Maintenance log added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Maintenance log added successfully!"
      400:
        description: Missing or invalid input
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing field: machine_id"
      500:
        description: Server error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Internal server error"
    """
    data = request.get_json()

    # basic input validation
    required_fields = ['machine_id', 'performed_by', 'notes', 'date', 'planned']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        planned = str(data['planned']).lower() == 'true'  # Convert to bool

        maintenance = MaintenanceLog(
            machine_id=data['machine_id'],
            performed_by=data['performed_by'],
            notes=data['notes'],
            date=datetime.fromisoformat(data['date']),
            planned=planned
        )

        db.session.add(maintenance)
        db.session.commit()
        return jsonify({"message": "Maintenance log added successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
