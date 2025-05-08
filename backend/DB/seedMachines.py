import os
import sys
# ensure project root (where models.py & app.py live) is on the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from datetime import datetime
from models import db, Machine
from app import app

CSV_DIR = os.path.join(os.path.dirname(__file__), '..', 'csv')

def parse_date_safe(date_str):
    try:
        return datetime.fromisoformat(date_str)
    except:
        return None

def seed_machines():
    path = os.path.join(CSV_DIR, 'machines.csv')
    if not os.path.exists(path):
        print(f"CSV not found: {path}")
        return

    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            m = Machine(
                id=int(row['machine_id']),
                name=row['name'],
                category=row['category'],
                group=row['group'],
                manufacturer=row['manufacturer'],
                created_at=parse_date_safe(row['created_at'])
            )
            db.session.merge(m)

if __name__ == '__main__':
    with app.app_context():
        seed_machines()
        db.session.commit()
        print("✅ Machines table seeded from machines.csv")
