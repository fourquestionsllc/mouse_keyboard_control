from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+
import subprocess
import time
import os

import subprocess
import sys
import os

# ====== CONFIG ======
run_time = datetime(2026, 2, 15, 13, 48, tzinfo=ZoneInfo("America/Chicago"))  # Example: Feb 20 2026, 3:30 PM CT
project_path = r"C:\Users\yanli\mouse_keyboard_control"
venv_activate = os.path.join(project_path, r"venv\Scripts\Activate.ps1")
script_to_run = os.path.join(project_path, "enrollment.py")
# ====================

print(f"Waiting to run at {run_time} Central Time...")

while True:
    now = datetime.now(ZoneInfo("America/Chicago"))
    if now >= run_time:
        print("Time reached! Running enrollment.py...")
        
        project_path = r"C:\Users\yanli\mouse_keyboard_control"
        script_to_run = os.path.join(project_path, "enrollment.py")

        subprocess.run(
            [sys.executable, script_to_run],
            cwd=project_path
        )
        break

    time.sleep(30)  # check every 30 seconds
