import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from datetime import datetime
from models import db, User
from app import app

# Paths
dir_path = os.path.dirname(__file__)
CSV_DIR = os.path.join(dir_path, '..', 'csv')

# Utility: safe ISO date parser
def parse_date_safe(date_str):
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        return None

# Seed only the users table
def seed_users():
    path = os.path.join(CSV_DIR, 'users.csv')
    if not os.path.exists(path):
        print(f"CSV not found: {path}")
        return

    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            u = User(
                id=int(row['id']),
                username=row['username'],
                password_hash=row['password_hash'],
                role=row['role'],
                created_at=parse_date_safe(row['created_at'])
            )
            db.session.merge(u)

if __name__ == '__main__':
    with app.app_context():
        seed_users()
        db.session.commit()
        print("✅ users table seeded from users.csv")
