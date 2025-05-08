import os
import csv
import random
import calendar
from datetime import datetime, timedelta, date

# Crée le dossier csv si nécessaire
os.makedirs('csv', exist_ok=True)

# Configuration
NUM_MACHINES = 50
NUM_TOOLS = 30
DASHBOARD_MONTHS = 3
MAINTENANCE_YEARS = [2021, 2022, 2023]

# Fonction utilitaire pour générer une date aléatoire
def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# 1. Génération des machines
machines = []
start_date = date(2018, 1, 1)
end_date = date(2023, 5, 3)
for mid in range(1, NUM_MACHINES + 1):
    machines.append({
        "machine_id": mid,
        "name": f"Machine_{mid}",
        "category": random.choice(["Manual", "Automatic"]),
        "group": random.choice(["CNC", "Assembly A", "Welding Bay", "Painting", "Press"]),
        "manufacturer": f"Manufacturer_{random.randint(1, 10)}",
        "created_at": random_date(start_date, end_date).isoformat(),
        "status": random.choice(["Running", "Offline"])
    })

with open(os.path.join('csv', 'machines.csv'), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=machines[0].keys())
    writer.writeheader()
    writer.writerows(machines)

# 2. Génération des outils
tools = []
tool_start = date(2018, 1, 1)
tool_end = date(2023, 5, 3)
statuses = ["in storage", "scrapped", "attached"]
storage_locations = ["Shelf A1", "Rack B2", "Shelf C3", "Rack D4", "Cabinet E5"]

for tid in range(1, NUM_TOOLS + 1):
    status = random.choice(statuses)
    tool = {
        "id": tid,
        "name": f"Tool_{tid}",
        "type": random.choice(["Cutting", "Drilling", "Grinding", "Milling"]),
        "created_at": random_date(tool_start, tool_end).isoformat(),
        "status": status,
        "wear_level": random.randint(0, 100),
        "storage_location": random.choice(storage_locations) if status == "in storage" else ""
    }
    tools.append(tool)
    
with open(os.path.join('csv', 'tools.csv'), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=tools[0].keys())
    writer.writeheader()
    writer.writerows(tools)

# 3. Génération des données de dashboard (3 mois récents)
dashboard = []
dash_id = 1
end_day = datetime.now().date()
start_day = end_day - timedelta(days=30 * DASHBOARD_MONTHS)
current_day = start_day

while current_day <= end_day:
    for m in machines:
        dashboard.append({
            "id": dash_id,
            "machine_id": m["machine_id"],
            "date": current_day.isoformat(),
            "oee": round(random.uniform(50, 100), 2),
            "availability": round(random.uniform(50, 100), 2),
            "performance": round(random.uniform(50, 100), 2),
            "output_quality": round(random.uniform(50, 100), 2),
            "status": random.choice(["Running", "Offline"])
        })
        dash_id += 1
    current_day += timedelta(days=1)

with open(os.path.join('csv', 'dashboard.csv'), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=dashboard[0].keys())
    writer.writeheader()
    writer.writerows(dashboard)

# 4. Génération des maintenances
maintenance = []
maint_id = 1
notes_choices = [
    "Replaced worn out parts",
    "Lubricated moving components",
    "Checked calibration",
    "Replaced filters",
    "Cleaned machine"
]
for m in machines:
    for year in MAINTENANCE_YEARS:
        maintenance.append({
            "id": maint_id,
            "machine_id": m["machine_id"],
            "performed_by": random.randint(1, 5),
            "date": random_date(date(year, 1, 1), date(year, 12, 31)).isoformat(),
            "notes": random.choice(notes_choices),
            "planned": random.choice([True, False])
        })
        maint_id += 1

with open(os.path.join('csv', 'maintenance.csv'), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=maintenance[0].keys())
    writer.writeheader()
    writer.writerows(maintenance)

print("✅ CSV files regenerated with updated tool statuses and fields.")
