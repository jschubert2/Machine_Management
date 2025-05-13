import os
import csv
import random
from datetime import datetime, timedelta, date

os.makedirs('csv', exist_ok=True)

NUM_MACHINES = 50
NUM_TOOLS = 30
MAINTENANCE_YEARS = [2021, 2022, 2023]
METRIC_MONTHS = [2, 3, 4]  # February, March, April
CURRENT_YEAR = datetime.now().year


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# 1. Machines
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

# 2. Tools
tools = []
tool_start = date(2018, 1, 1)
tool_end = date(2023, 5, 3)
for tid in range(1, NUM_TOOLS + 1):
    status = random.choice(["storage", "in storage", "attached"])
    include_storage = status in ["storage", "in storage"]
    tools.append({
        "id": tid,
        "name": f"Tool_{tid}",
        "type": random.choice(["Cutting", "Drilling", "Grinding", "Milling"]),
        "created_at": random_date(tool_start, tool_end).isoformat(),
        "status": status,
        "storage_location": random.choice(["Shelf A1", "Shelf B2", "Rack C3"]) if include_storage else "",
        "wear_level": random.randint(0, 100) if include_storage else ""
    })

with open(os.path.join('csv', 'tools.csv'), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=tools[0].keys())
    writer.writeheader()
    writer.writerows(tools)

# 3. Dashboard metrics 
dashboard = []
dash_id = 1
for month in METRIC_MONTHS:
    num_days = (date(CURRENT_YEAR, month % 12 + 1, 1) - timedelta(days=1)).day
    for day in range(1, num_days + 1):
        for m in machines:
            dashboard.append({
                "id": dash_id,
                "machine_id": m["machine_id"],
                "date": date(CURRENT_YEAR, month, day).isoformat(),
                "oee": round(random.uniform(50, 100), 2),
                "availability": round(random.uniform(50, 100), 2),
                "performance": round(random.uniform(50, 100), 2),
                "output_quality": round(random.uniform(50, 100), 2),
                "status": random.choice(["Running", "Offline"])
            })
            dash_id += 1

with open(os.path.join('csv', 'dashboard.csv'), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=dashboard[0].keys())
    writer.writeheader()
    writer.writerows(dashboard)

# 4. Maintenance logs
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

print("✅ CSV files regenerated with machine, tool, dashboard and maintenance data.")
