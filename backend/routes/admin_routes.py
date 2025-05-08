import os
import csv
from flask import Blueprint, jsonify
from models import db, Machine, Tool, MaintenanceLog, MachineMetric, ToolMetric
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('admin_routes', __name__)

CSV_DIR = os.path.join(os.path.dirname(__file__), '..', 'csv')

def parse_date(date_str):
    try:
        # First try full ISO format (with time)
        return datetime.fromisoformat(date_str)
    except ValueError:
        try:
            # Then try date only
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            # Then try date and time with seconds (if your CSV uses that)
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
                db.session.flush()  # Get the generated tool.id before commit

                metric = ToolMetric(
                    tool_id=tool.id,
                    status=row['status'],
                    wear_level=int(row['wear_level']),
                    storage_location=row['storage_location'] if row['status'] == 'in storage' else "N/A"
                )
                db.session.add(metric)
        #print("tools done")
        # Load maintenance.csv
        with open(os.path.join(CSV_DIR, 'maintenance.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:

                #because we have no real users in Sprint 1 we use random names for now
                tempuser = "Mark"
                if (row['performed_by'] == "1"):
                    tempuser = "Olaf"
                elif (row['performed_by'] == "2"):
                    tempuser = "John"
                elif (row['performed_by'] == "3"):
                    tempuser = "Kate"
                elif (row['performed_by'] == "4"):
                    tempuser = "Marie"
                elif (row['performed_by'] == "5"):
                    tempuser = "Simon"

                log = MaintenanceLog(
                    machine_id=int(row['machine_id']),
                    performed_by=tempuser, #for testing
                    date=parse_date(row['date']),
                    notes=row['notes'],
                    planned=row['planned'].lower() == 'true'
                )
                db.session.add(log)
        #print("maintenance done")
        # Load dashboard.csv (machine_metrics)
        with open(os.path.join(CSV_DIR, 'dashboard.csv')) as f:
            reader = csv.DictReader(f)
            for row in reader:
                metric = MachineMetric(
                    machine_id=int(row['machine_id']),
                    timestamp=parse_date(row['date']),
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
