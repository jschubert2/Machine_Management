#!/usr/bin/env python3
"""
run_all_seeds.py

This script will sequentially execute all your individual seeder scripts
located in the DB/ folder, so you can populate every table in one go.
"""

import subprocess
import sys
import os

# List your seeder scripts here, in the order they should run:
SCRIPTS = [
    "DB/seedUsers.py",
    "DB/seedMachines.py",
    "DB/seedTools.py",
    "DB/seedToolMetrics.py",
    "DB/seedMachineMetrics.py",
    "DB/seedMaintenance.py",
]

def main():
    # Ensure we run from project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    for script in SCRIPTS:
        print(f"🟢 Running {script}...")
        # Use the same Python interpreter
        result = subprocess.run([sys.executable, script])
        if result.returncode != 0:
            print(f"❌ {script} failed (exit code {result.returncode}). Aborting.")
            sys.exit(result.returncode)

    print("🎉 All seed scripts executed successfully!")

if __name__ == "__main__":
    main()
