    # DB/seedToolStatus.py

import os
import sys
# ajoute la racine du projet au path pour importer models et app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from datetime import datetime
from models import db, ToolMetric
from app import app

CSV_DIR = os.path.join(os.path.dirname(__file__), '..', 'csv')

def parse_date_safe(s):
    try:
        return datetime.fromisoformat(s)
    except:
        return None

def parse_int_safe(s):
    try:
        return int(s)
    except:
        return None

def seed_tool_status():
    path = os.path.join(CSV_DIR, 'tool_status.csv')
    if not os.path.exists(path):
        print(f"CSV not found: {path}")
        return

    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tm = ToolMetric(
                tool_id=int(row['tool_id']),
                status=row['status'],
                storage_location=row.get('storage_location', '') or None,
                wear_level=parse_int_safe(row.get('wear_level')) or 0,
                # timestamp=parse_date_safe(row['timestamp'])
            )
            db.session.add(tm)

if __name__ == '__main__':
    with app.app_context():
        seed_tool_status()
        db.session.commit()
        print("✅ tool_status (ToolMetric) table seeded from tool_status.csv")
