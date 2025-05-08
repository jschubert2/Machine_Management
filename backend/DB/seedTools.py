# DB/seedTools.py

import os
import sys
# ajoute la racine du projet au path pour importer models et app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from datetime import datetime
from models import db, Tool
from app import app

CSV_DIR = os.path.join(os.path.dirname(__file__), '..', 'csv')

def parse_date_safe(s):
    try:
        return datetime.fromisoformat(s)
    except:
        return None

def seed_tools():
    path = os.path.join(CSV_DIR, 'tools.csv')
    if not os.path.exists(path):
        print(f"CSV not found: {path}")
        return

    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tool = Tool(
                id=int(row['id']),
                name=row['name'],
                type=row['type'],
                created_at=parse_date_safe(row['created_at'])
            )
            db.session.merge(tool)

if __name__ == '__main__':
    with app.app_context():
        seed_tools()
        db.session.commit()
        print("✅ tools table seeded from tools.csv")
