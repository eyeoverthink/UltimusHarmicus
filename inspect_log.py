import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet
from PIL import Image
from pyzbar.pyzbar import decode as qr_decode

OUTPUT_DIR = "qr_chain_proof"

# --- Decryption Functions (from qr_chain_validator.py) ---
def generate_key(entity_id):
    """Generates a deterministic key from an ID (entanglement or intrusion)."""
    sha256 = hashlib.sha256(entity_id.encode())
    return base64.urlsafe_b64encode(sha256.digest())

def read_qr_code(filename):
    """Reads data from a QR code."""
    try:
        return json.loads(qr_decode(Image.open(filename))[0].data.decode('utf-8'))
    except (IOError, IndexError) as e:
        print(f"Could not read QR code {os.path.basename(filename)}: {e}")
        return None

def decrypt_payload(encrypted_payload, key):
    """Decrypts the payload and returns a dictionary."""
    try:
        f = Fernet(key)
        decrypted_str = f.decrypt(encrypted_payload)
        return json.loads(decrypted_str.decode())
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

def inspect_log_file(log_filename):
    """Reads, decrypts, and prints the contents of an intrusion log."""
    print(f"--- 🔍 Inspecting Intrusion Log: {log_filename} 🔍 ---")
    
    # Extract intrusion ID from filename (e.g., 'intrusion-1755228673.log.bin' -> 'intrusion-1755228673')
    intrusion_id = os.path.basename(log_filename).split('.')[0]
    
    # Generate the deterministic key from the ID
    key = generate_key(intrusion_id)
    print(f"  [+] Generated decryption key for ID: {intrusion_id}")

    # Read the encrypted log file
    try:
        with open(log_filename, "rb") as f:
            encrypted_log = f.read()
        print(f"  [+] Successfully read encrypted log file.")
    except IOError as e:
        print(f"  [!] Error reading file: {e}")
        return

    # Decrypt the log
    decrypted_log = decrypt_payload(encrypted_log, key)

    if decrypted_log:
        print("  [*] Decryption Successful. Log Contents:")
        print("--------------------------------------------------")
        print(json.dumps(decrypted_log, indent=4, sort_keys=True))
        print("--------------------------------------------------")
        print("--- ✅ Inspection Complete ✅ ---")
    else:
        print("  [!] Could not decrypt or read log content.")

if __name__ == "__main__":
    # Find the most recent intrusion log file to inspect
    try:
        log_files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith('intrusion-') and f.endswith('.log.bin')]
        log_files.sort(key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)))
        if not log_files:
            raise FileNotFoundError("No intrusion logs found in output directory.")
        latest_log = os.path.join(OUTPUT_DIR, log_files[-1])
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit()

    inspect_log_file(latest_log)

    # Now, inspect the final state of the chain to verify the reverse trace
    final_state_qr = os.path.join(OUTPUT_DIR, "chain_step_6.png")
    print(f"\n--- 🔍 Inspecting Final Chain State: {os.path.basename(final_state_qr)} 🔍 ---")
    final_state_data = read_qr_code(final_state_qr)
    if final_state_data:
        print("  [*] QR Code Read Successful. Final State Contents:")
        print("--------------------------------------------------")
        print(json.dumps(final_state_data, indent=4, sort_keys=True))
        print("--------------------------------------------------")
        if 'known_threats' in final_state_data:
            print("--- ✅ REVERSE TRACE VERIFIED: 'known_threats' list is present. ✅ ---")
        else:
            print("--- ❌ REVERSE TRACE FAILED: 'known_threats' list not found in final state. ❌ ---")
    else:
        print("  [!] Could not read final state QR code.")
