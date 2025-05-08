import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from datetime import datetime
from models import db, MachineMetric
from app import app

CSV_DIR = os.path.join(os.path.dirname(__file__), '..', 'csv')

def parse_date_safe(date_str):
    try:
        return datetime.fromisoformat(date_str)
    except:
        return None

def parse_float_safe(val):
    try:
        return float(val)
    except:
        return None

def seed_machine_metrics():
    path = os.path.join(CSV_DIR, 'machine_metrics.csv')
    if not os.path.exists(path):
        print(f"CSV not found: {path}")
        return

    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mm = MachineMetric(
                id=int(row['id']),
                machine_id=int(row['machine_id']),
                timestamp=parse_date_safe(row['timestamp']),
                oee=parse_float_safe(row['oee']),
                availability=parse_float_safe(row['availability']),
                performance=parse_float_safe(row['performance']),
                output_quality=parse_float_safe(row['output_quality']),
                status=row['status']
            )
            db.session.merge(mm)

if __name__ == '__main__':
    with app.app_context():
        seed_machine_metrics()
        db.session.commit()
        print("✅ machine_metrics table seeded from machine_metrics.csv")
