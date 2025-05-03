from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, MaintenanceLog

bp = Blueprint('maintenance', __name__)

@bp.route('/machines/<int:machine_id>/maintenance', methods=['GET'])
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

@bp.route('/maintenance', methods=['POST'])
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
