#!/usr/bin/env python3
"""
QR Web Bridge - Creates JSON from web form and generates real QR codes using existing system
"""

import json
import sys
import subprocess
import os
from pathlib import Path

def create_json_from_web_data(actions_data):
    """Convert web form data to JSON format compatible with qr_phone_control_loop.py"""
    json_actions = []
    
    for i, action in enumerate(actions_data):
        step = {
            "step": i + 1,
            "description": action["name"],
            "url": action["url"]
        }
        json_actions.append(step)
    
    return json_actions

def generate_qr_codes(actions_data, output_dir="qr_output"):
    """Generate QR codes using the existing proven system"""
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Create temporary JSON file
    temp_json = f"{output_dir}/temp_actions.json"
    json_actions = create_json_from_web_data(actions_data)
    
    with open(temp_json, 'w') as f:
        json.dump(json_actions, f, indent=2)
    
    # Run the proven QR generator
    cmd = [
        "python3", "qr_phone_control_loop.py",
        "--actions", temp_json,
        "--ecc", "Q",
        "--delay", "0.1",
        "--output-dir", output_dir
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            return {
                "success": True,
                "message": "QR codes generated successfully",
                "output_dir": output_dir,
                "stdout": result.stdout
            }
        else:
            return {
                "success": False,
                "error": result.stderr,
                "stdout": result.stdout
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Example usage
    sample_actions = [
        {
            "name": "Send SMS Message",
            "url": "sms:+1-555-123-4567&body=Test%20message%20from%20QR%20control"
        },
        {
            "name": "Open Camera",
            "url": "camera://"
        }
    ]
    
    result = generate_qr_codes(sample_actions)
    print(json.dumps(result, indent=2))
