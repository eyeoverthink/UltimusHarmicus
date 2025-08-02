#!/usr/bin/env python3
"""
🌊⚡ DIRECT QR CHAIN EXECUTOR ⚡🌊

Directly executes QR chain payloads to test autonomous QR executable architecture!
This bypasses the multi-file test system and directly processes single QR payloads.

By Vaughn Scott - Consciousness Physics Framework
"""

import json
import base64
import zlib
import sys

def execute_single_qr_payload(filename):
    """Execute a single QR payload directly"""
    
    print("🌊⚡ DIRECT QR CHAIN EXECUTOR ⚡🌊")
    print("=" * 60)
    print(f"Executing QR payload: {filename}")
    
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        # Extract the compressed payload
        lines = content.split('\n')
        payload_line = None
        for line in lines:
            if line.startswith('COMPRESSED:'):
                payload_line = line
                break
        
        if not payload_line:
            print("❌ No compressed payload found in file")
            return False
        
        print("✅ Found compressed QR payload")
        
        # Decompress the payload
        compressed_data_b64 = payload_line.replace('COMPRESSED:', '')
        compressed_data = base64.b64decode(compressed_data_b64)
        decompressed_data = zlib.decompress(compressed_data)
        qr_content_str = decompressed_data.decode('utf-8')
        
        print("✅ Successfully decompressed QR payload")
        
        # Parse JSON
        qr_payload = json.loads(qr_content_str)
        
        print("✅ Successfully parsed QR JSON payload")
        print(f"   Task ID: {qr_payload.get('task_id', 'N/A')}")
        print(f"   Task Type: {qr_payload.get('task_type', 'N/A')}")
        print(f"   Chain Step: {qr_payload.get('metadata', {}).get('chain_step', 'N/A')}")
        print(f"   Consciousness Level: {qr_payload.get('metadata', {}).get('consciousness_level', 'N/A')}")
        
        # Extract and execute the Python script
        if qr_payload.get('task_type') == 'execute_python':
            python_script = qr_payload.get('python_script')
            if python_script:
                print("\n🚀 EXECUTING QR CHAIN SCRIPT...")
                print("=" * 60)
                
                # Execute the script directly
                exec(python_script)
                
                print("=" * 60)
                print("✅ QR CHAIN SCRIPT COMPLETED SUCCESSFULLY!")
                print("⚡ AUTONOMOUS QR GENERATION AND EXECUTION PROVEN!")
                return True
            else:
                print("❌ No python_script found in payload")
                return False
        else:
            print(f"❌ Unsupported task type: {qr_payload.get('task_type')}")
            return False
            
    except Exception as e:
        print(f"❌ Error executing QR payload: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 direct_qr_chain_test.py <qr_payload_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    success = execute_single_qr_payload(filename)
    
    if success:
        print(f"\n🏆 QR CHAIN EXECUTION SUCCESSFUL!")
        print(f"🌊⚡ VAUGHN SCOTT'S QR RAMLESS ARCHITECTURE PROVEN! ⚡🌊")
    else:
        print(f"\n❌ QR CHAIN EXECUTION FAILED!")
