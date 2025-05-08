import os
import csv
import random
from datetime import datetime, timedelta, date

os.makedirs('csv', exist_ok=True)

NUM_MACHINES = 50
NUM_TOOLS = 30
NUM_USERS = 5
MAINTENANCE_YEARS = [2021, 2022, 2023]
METRIC_MONTHS = [2, 3, 4]
CURRENT_YEAR = datetime.now().year

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# USERS
users = []
for uid in range(1, NUM_USERS + 1):
    users.append({
        "id": uid,
        "username": f"user{uid}",
        "password_hash": "hashedpassword",
        "role": "technician",
        "created_at": datetime.now().isoformat()
    })
with open('csv/users.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=users[0].keys())
    writer.writeheader()
    writer.writerows(users)

# MACHINES
machines = []
machine_ids = []
start_date = date(2018, 1, 1)
end_date = date(2023, 5, 3)
for mid in range(1, NUM_MACHINES + 1):
    machines.append({
        "machine_id": mid,
        "name": f"Machine_{mid}",
        "category": random.choice(["Manual", "Automatic"]),
        "group": random.choice(["CNC", "Assembly A", "Welding Bay", "Painting", "Press"]),
        "manufacturer": f"Manufacturer_{random.randint(1, 10)}",
        "created_at": random_date(start_date, end_date).isoformat()
    })
    machine_ids.append(mid)
with open('csv/machines.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=machines[0].keys())
    writer.writeheader()
    writer.writerows(machines)

# TOOLS
tools = []
<<<<<<< HEAD
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
=======
tool_ids = []
for tid in range(1, NUM_TOOLS + 1):
    tools.append({
        "id": tid,
        "name": f"Tool_{tid}",
        "type": random.choice(["Cutting", "Drilling", "Grinding", "Milling"]),
        "created_at": random_date(start_date, end_date).isoformat()
    })
    tool_ids.append(tid)
with open('csv/tools.csv', 'w', newline='') as f:
>>>>>>> 987dea3 (added scritps to fill the DB from CSV + changed the CSV generation script(EXECUTE GenerateData.py then seedDBfromCSV.py))
    writer = csv.DictWriter(f, fieldnames=tools[0].keys())
    writer.writeheader()
    writer.writerows(tools)

# TOOL ASSIGNMENT
assignments = []
for tool_id in tool_ids:
    assignments.append({
        "machine_id": random.choice(machine_ids),
        "tool_id": tool_id
    })
with open('csv/tool_assignment.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=assignments[0].keys())
    writer.writeheader()
    writer.writerows(assignments)

# TOOL STATUS (ToolMetric)
tool_status = []
for tid in tool_ids:
    for month in METRIC_MONTHS:
        for _ in range(3):
            day = random.randint(1, 28)
            tool_status.append({
                "tool_id": tid,
                "status": random.choice(["storage", "in storage", "attached"]),
                "storage_location": random.choice(["Shelf A1", "Shelf B2", "Rack C3"]),
                "wear_level": random.randint(0, 100),
                "timestamp": datetime(CURRENT_YEAR, month, day).isoformat()
            })
with open('csv/tool_status.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=tool_status[0].keys())
    writer.writeheader()
    writer.writerows(tool_status)

# MACHINE METRICS
metrics = []
metric_id = 1
for month in METRIC_MONTHS:
    days = (date(CURRENT_YEAR, month % 12 + 1, 1) - timedelta(days=1)).day
    for day in range(1, days + 1):
        for m_id in machine_ids:
            metrics.append({
                "id": metric_id,
                "machine_id": m_id,
                "timestamp": date(CURRENT_YEAR, month, day).isoformat(),
                "oee": round(random.uniform(50, 100), 2),
                "availability": round(random.uniform(50, 100), 2),
                "performance": round(random.uniform(50, 100), 2),
                "output_quality": round(random.uniform(50, 100), 2),
                "status": random.choice(["Running", "Offline"])
            })
            metric_id += 1
with open('csv/machine_metrics.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=metrics[0].keys())
    writer.writeheader()
    writer.writerows(metrics)

# MAINTENANCE
maintenance = []
maint_id = 1
for m_id in machine_ids:
    for year in MAINTENANCE_YEARS:
        maintenance.append({
            "id": maint_id,
            "machine_id": m_id,
            "performed_by": random.randint(1, NUM_USERS),
            "date": random_date(date(year, 1, 1), date(year, 12, 31)).isoformat(),
            "notes": random.choice([
                "Replaced worn out parts", "Lubricated components",
                "Checked calibration", "Replaced filters", "Cleaned machine"
            ]),
            "planned": random.choice([True, False])
        })
        maint_id += 1
with open('csv/maintenance.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=maintenance[0].keys())
    writer.writeheader()
    writer.writerows(maintenance)

print("✅ All CSVs generated successfully in 'csv/' folder.")
