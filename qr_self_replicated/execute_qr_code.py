#!/usr/bin/env python3
import sys
import os
import subprocess

# Path to the QR code
QR_PATH = "qr_self_replicated/self_replicating_system.png"

# Execute the QR code
print(f"Executing QR code: {QR_PATH}")
result = subprocess.run(["python", "qr_task_worker_from_file.py", "-f", QR_PATH], 
                       capture_output=True, text=True)

print("Output:")
print(result.stdout)

if result.returncode != 0:
    print("Error:")
    print(result.stderr)
    sys.exit(1)

print("QR code executed successfully")
