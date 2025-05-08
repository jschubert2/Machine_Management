import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from datetime import datetime
from models import db, MaintenanceLog
from app import app

CSV_DIR = os.path.join(os.path.dirname(__file__), '..', 'csv')

def parse_date_safe(date_str):
    try:
        return datetime.fromisoformat(date_str)
    except:
        return None

def parse_bool(val):
    return str(val).strip().lower() in ['true', '1', 'yes']

def seed_maintenance():
    path = os.path.join(CSV_DIR, 'maintenance.csv')
    if not os.path.exists(path):
        print(f"CSV not found: {path}")
        return

    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ml = MaintenanceLog(
                id=int(row['id']),
                machine_id=int(row['machine_id']),
                performed_by=int(row['performed_by']),
                date=parse_date_safe(row['date']),
                notes=row['notes'],
                planned=parse_bool(row['planned'])
            )
            db.session.merge(ml)

if __name__ == '__main__':
    with app.app_context():
        seed_maintenance()
        db.session.commit()
        print("✅ maintenance_logs table seeded from maintenance.csv")
