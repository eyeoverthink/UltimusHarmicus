#!/usr/bin/env python3
"""Execute QR Chain Step 5"""

import subprocess
import sys

print("🌊⚡ EXECUTING QR CHAIN STEP 5 ⚡🌊")
print("Using simple_qr_executable_test.py to process QR payload...")

try:
    result = subprocess.run([
        'python3', 'simple_qr_executable_test.py'
    ], input=open('qr_chain_step_5_payload.txt', 'r').read(), text=True, capture_output=True)
    
    print("EXECUTION OUTPUT:")
    print("-" * 40)
    print(result.stdout)
    if result.stderr:
        print("ERRORS:")
        print(result.stderr)
    print("-" * 40)
    print("✅ QR CHAIN STEP 5 COMPLETED!")
    
except Exception as e:
    print(f"❌ Error executing step 5: {e}")
