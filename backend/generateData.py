import os
import csv
import random
import hashlib
from datetime import datetime, timedelta, date

# Crée le dossier CSV
os.makedirs('csv', exist_ok=True)

# Config
NUM_MACHINES = 50
NUM_TOOLS = 30
NUM_USERS = 10
DASHBOARD_MONTHS = 3
MAINTENANCE_YEARS = [2021, 2022, 2023]

# Fonctions utilitaires
def random_date(start: date, end: date) -> date:
    """
    Generates a random date between two given dates.

    @param start Lower bound for the generated date (inclusive)
    @param end Upper bound for the generated date (inclusive)
    @return A random date between start and end
    """
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

start_date = date(2018, 1, 1)
end_date = date(2023, 5, 3)

# Listes réalistes
machine_names = [
    "LathePro X", "CNC Master 3000", "ForgeLine Z1", "RoboPress 9",
    "HydraDrill H7", "AutoMill 200", "SwiftCutter S2", "MegaWeld M5"
]
manufacturers = ["Siemens", "Bosch", "GE Industrial", "Mitsubishi", "Fanuc"]
machine_groups = ["CNC", "Assembly A", "Welding Bay", "Painting", "Press"]
machine_status = ["Running", "Offline"]
tool_types = ["Cutting", "Drilling", "Grinding", "Milling"]
tool_statuses = ["in storage", "attached", "scrapped"]
storage_locations = ["Shelf A1", "Rack B2", "Shelf C3", "Rack D4", "Cabinet E5"]

first_names = ["Alice", "Bob", "Claire", "Daniel", "Eva", "Frank", "Grace", "Hugo", "Iris", "Jack"]
last_names = ["Martin", "Durand", "Lemoine", "Bernard", "Petit", "Robert", "Moreau", "Fournier", "Garcia", "Leroy"]

# --- machines.csv ---
# Creates a list of industrial machines with realistic metadata (name, type, group, etc.)
# WHY: Simulates a machine registry for an industrial workshop or factory

machines = []
for mid in range(1, NUM_MACHINES+1):
    machines.append({
        "id": mid,
        "name": f"{random.choice(machine_names)} #{mid}",
        "category": random.choice(["Manual", "Automatic"]),
        "group": random.choice(machine_groups),
        "manufacturer": random.choice(manufacturers),
        "created_at": random_date(start_date, end_date).isoformat()
    })

with open('csv/machines.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=machines[0].keys())
    writer.writeheader()
    writer.writerows(machines)

# --- users.csv ---
# Generates admin and technician users with unique usernames and hashed passwords
# WHY: Mimics a realistic user system with authentication and roles

# WHY (username logic): Prevents duplicate usernames by adding a numeric suffix when needed
# WHY (password hashing): Simulates secure user credentials without storing plaintext passwords

users = []
used_usernames = set()
for uid in range(1, NUM_USERS + 1):
    fname = random.choice(first_names)
    lname = random.choice(last_names)
    username_base = f"{fname.lower()}.{lname.lower()}"
    username = username_base

    suffix = 1
    while username in used_usernames:
        suffix += 1
        username = f"{username_base}{suffix}"
    used_usernames.add(username)

    users.append({
        "id": uid,
        "username": username,
        "firstname": fname,
        "lastname": lname,
        "created_at": random_date(start_date, end_date).isoformat()
    })

with open('csv/users.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=users[0].keys())
    writer.writeheader()
    writer.writerows(users)

# --- tools.csv ---
# Builds a catalog of tools with type and model identifiers
# WHY: Represents the available tooling inventory in a factory setting

tools = []
for tid in range(1, NUM_TOOLS+1):
    tools.append({
        "id": tid,     
        "name": f"{random.choice(['Drill', 'Cutter', 'Grinder', 'End Mill', 'Reamer', 'Boring Bar', 'Insert', 'Chuck', 'Collet', 'Saw'])} Model-{random.randint(100,999)}",
        "type": random.choice(tool_types),
        "created_at": random_date(start_date, end_date).isoformat()
    })

with open('csv/tools.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=tools[0].keys())
    writer.writeheader()
    writer.writerows(tools)

# --- tool_metrics.csv ---
# Assigns a wear level and storage status to each tool
# WHY: Used to track physical condition and availability of tools for maintenance or operational planning

# WHY (storage_location condition): Only tools marked as 'in storage' are assigned a storage rack

tool_metrics = []
for t in tools:
    status = random.choice(tool_statuses)
    tool_metrics.append({
        "id": t["id"],
        "tool_id": t["id"],
        "status": status,
        "storage_location": random.choice(storage_locations) if status=="in storage" else "",
        "wear_level": random.randint(0, 100)
    })

with open('csv/tool_metrics.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=tool_metrics[0].keys())
    writer.writeheader()
    writer.writerows(tool_metrics)

# --- tool_assignments.csv ---
# Links tools to machines in a round-robin pattern
# WHY: Ensures each tool is assigned to a machine for simulation purposes

assignments = []
machine_count = len(machines)
for idx, t in enumerate(tools, start=1):
    assignments.append({
        "id": idx,
        "machine_id": (idx - 1) % machine_count + 1,  # cycles through machine IDs starting at 1
        "tool_id": t["id"]
    })
with open('csv/tool_assignments.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=assignments[0].keys())
    writer.writeheader()
    writer.writerows(assignments)

# --- machine_metrics.csv ---
# Logs daily performance data (OEE, availability, etc.) for each machine over several months
# WHY: Simulates dashboard data that can be visualized in an industrial monitoring system

# WHY (looping logic): Iterates day-by-day and generates multiple metrics per machine per day
# WHY (randomized KPIs): Mimics real-world fluctuations in machine performance

machine_metrics = []
mm_id = 1
today = datetime.now().date()
start_day = today - timedelta(days=30 * DASHBOARD_MONTHS)
cur = start_day
while cur <= today:
    for m in machines:
        machine_metrics.append({
            "id": mm_id,
            "machine_id": m["id"],
            "timestamp": cur.isoformat(),
            "oee": round(random.uniform(50, 100), 2),
            "availability": round(random.uniform(50, 100), 2),
            "performance": round(random.uniform(50, 100), 2),
            "output_quality": round(random.uniform(50, 100), 2),
            "status": random.choice(machine_status)
        })
        mm_id += 1
    cur += timedelta(days=1)

with open('csv/machine_metrics.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=machine_metrics[0].keys())
    writer.writeheader()
    writer.writerows(machine_metrics)

# --- maintenance_logs.csv ---
# Creates annual maintenance records for all machines, performed by technicians
# WHY: Reflects historical maintenance activity, including whether it was planned or reactive

# WHY (random technician): Randomly assigns a valid technician ID for each maintenance log

maintenance = []
maint_id = 1
notes_choices = [
    "Replaced worn out parts",
    "Lubricated moving components",
    "Checked calibration",
    "Replaced filters",
    "Cleaned machine"
]
technician_ids = [u["id"] for u in users]

for m in machines:
    for year in MAINTENANCE_YEARS:
        maintenance.append({
            "id": maint_id,
            "machine_id": m["id"],
            "performed_by": random.choice(technician_ids),
            "date": random_date(date(year,1,1), date(year,12,31)).isoformat(),
            "notes": random.choice(notes_choices),
            "planned": random.choice([True, False])
        })
        maint_id += 1

with open('csv/maintenance_logs.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=maintenance[0].keys())
    writer.writeheader()
    writer.writerows(maintenance)

print("✅ All CSV files with realistic demo data have been generated in the /csv directory.")
# WHY: Gives the user a clear confirmation that the script completed successfully
