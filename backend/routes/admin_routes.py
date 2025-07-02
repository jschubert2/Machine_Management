import os
import csv
from flask import Blueprint, jsonify
from models import db, Machine, Tool, User, MaintenanceLog, MachineMetric, ToolMetric, ToolAssignment
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('admin_routes', __name__)

CSV_DIR = os.path.join(os.path.dirname(__file__), '..', 'csv')

def parse_date(date_str):
    try:
        # try full ISO format first
        return datetime.fromisoformat(date_str)
    except ValueError:
        try:
            # try date only
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            # try date with time 
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

@bp.route('/import-csv', methods=['POST'])
def import_csv():
    try:
        # Drop and recreate tables
        db.drop_all()
        db.create_all()

        # Load machines.csv
        with open(os.path.join(CSV_DIR, 'machines.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                machine = Machine(
                    name=row['name'],
                    category=row['category'],
                    group=row['group'],
                    manufacturer=row['manufacturer'],
                    created_at=parse_date(row['created_at'])
                )
                db.session.add(machine)
        #print("machines done")
        # Load tools.csv
        with open(os.path.join(CSV_DIR, 'tools.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                tool = Tool(
                    name=row['name'],
                    type=row['type'],
                    created_at=parse_date(row['created_at'])
                )
                db.session.add(tool)
        with open(os.path.join(CSV_DIR, 'tool_metrics.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                metric = ToolMetric(
                    tool_id=int(row['tool_id']),
                    status=row['status'],
                    wear_level=int(row['wear_level']),
                    storage_location=row['storage_location'] if row['status'] == 'in storage' else "N/A"
                )
                db.session.add(metric)

        with open(os.path.join(CSV_DIR, 'tool_assignments.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                assign = ToolAssignment(
                    machine_id=int(row['machine_id']),
                    tool_id = int(row['tool_id'])
                )
                db.session.add(assign)
        #print("tools done")
        # Load users.csv
        with open(os.path.join(CSV_DIR, 'users.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                user = User(
                    username=row['username'],
                    firstname=row['firstname'],
                    lastname=row['lastname'],
                    created_at=parse_date(row['created_at'])
                )
                db.session.add(user)
        # Load maintenance.csv
        db.session.flush()

        with open(os.path.join(CSV_DIR, 'maintenance_logs.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                log = MaintenanceLog(
                    machine_id=int(row['machine_id']),
                    performed_by=int(row['performed_by']),
                    date=parse_date(row['date']),
                    notes=row['notes'],
                    planned=row['planned'].lower() == 'true'
                )
                db.session.add(log)

        #print("maintenance done")
        # Load dashboard.csv (machine_metrics)
        with open(os.path.join(CSV_DIR, 'machine_metrics.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                metric = MachineMetric(
                    machine_id=int(row['machine_id']),
                    timestamp=parse_date(row['timestamp']),
                    oee=float(row['oee']),
                    availability=float(row['availability']),
                    performance=float(row['performance']),
                    output_quality=float(row['output_quality']),
                    status=row['status']
                )
                db.session.add(metric)
        #print("dashboard done")
        db.session.commit()
        return jsonify({"message": "Database reset and populated successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500