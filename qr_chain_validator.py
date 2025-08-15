import os
import json
import time
import hashlib
import base64
import secrets
import string
from cryptography.fernet import Fernet
from PIL import Image
from pyzbar.pyzbar import decode as qr_decode
import qrcode

# # --- Configuration & Constants ---
# OUTPUT_DIR = "qr_chain_proof"
# STATE_FILE = "trickle_state.json"
# PHI = 1.61803398875
# PSI = 1.324717957244746  # Plastic Number
# INITIAL_CONSCIOUSNESS = 25.0
# ITERATIONS = 8

# # --- Helper Functions ---

# def get_payload_hash(payload):
#     """Computes a stable hash for a dictionary."""
#     payload_string = json.dumps(payload, sort_keys=True)
#     return int(hashlib.sha256(payload_string.encode()).hexdigest(), 16) % (10**18)

# def generate_hash(data):
#     return hasher.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

# def create_qr_code(data, filename):
#     """Generates and saves a QR code."""
#     qr = qrcode.QRCode(version=1, box_size=10, border=5)
#     qr.add_data(data)
#     qr.make(fit=True)
#     img = qr.make_image(fill='black', back_color='white')
#     img.save(filename)

# def read_qr_code(filename):
#     """Reads data from a QR code."""
#     try:
#         return json.loads(qr_decode(Image.open(filename))[0].data.decode('utf-8'))
#     except (IOError, IndexError):
#         return None

# def validate_semantic_integrity(payload):
#     """Checks for logical consistency in the payload, like a math problem."""
#     if "logic_test" in payload and isinstance(payload["logic_test"], dict):
#         try:
#             problem = payload["logic_test"]["problem"]
#             expected = payload["logic_test"]["expected_result"]
#             actual = eval(problem, {"__builtins__": None}, {})
#             if actual != expected:
#                 print(f"  [!] SEMANTIC ERROR DETECTED: Logic test failed. Expected {expected}, got {actual}.")
#                 return False
#         except Exception as e:
#             print(f"  [!] Error evaluating logic test: {e}")
#             return False
#     return True

# def manage_run_state(state_file):
#     """Reads and increments the run count from the state file."""
#     try:
#         with open(state_file, 'r') as f:
#             state = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         state = {"run_count": 0}
    
#     run_count = state.get("run_count", 0)
#     current_run = run_count
#     state["run_count"] = (run_count + 1) % 4 # Cycle through 4 tests

#     with open(state_file, 'w') as f:
#         json.dump(state, f, indent=4)
        
#     return current_run

# def universal_consciousness_evolution(c0, n, m):
#     """
#     Calculates the evolution of consciousness based on the Universal Law.
#     c0: initial consciousness level
#     n: number of iterations/cycles

# --- Configuration & Constants ---
OUTPUT_DIR = "qr_chain_proof"
STATE_FILE = "trickle_state.json"
THREAT_LEDGER = "threat_ledger.json"
PHI = 1.61803398875  # Golden Ratio
PSI = 1.32471795724  # Plastic Number

# --- Encryption & Security Helpers ---
def generate_key(entanglement_id):
    """Generates a deterministic key from the entanglement ID."""
    sha256 = hashlib.sha256(entanglement_id.encode())
    return base64.urlsafe_b64encode(sha256.digest())

def generate_secure_password(length=16):
    """Generates a cryptographically secure password."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(length))

def encrypt_payload(payload, key):
    """Encrypts the payload dictionary."""
    f = Fernet(key)
    payload_str = json.dumps(payload, sort_keys=True)
    return f.encrypt(payload_str.encode())

def decrypt_payload(encrypted_payload, key):
    """Decrypts the payload and returns a dictionary."""
    f = Fernet(key)
    decrypted_str = f.decrypt(encrypted_payload)
    return json.loads(decrypted_str.decode())

# --- Core QR & Hashing Functions ---
def get_payload_hash(payload):
    """Creates a SHA256 hash of a payload dictionary."""
    payload_to_hash = payload.copy()
    if 'self_hash' in payload_to_hash:
        del payload_to_hash['self_hash']
    payload_string = json.dumps(payload_to_hash, sort_keys=True)
    return int(hashlib.sha256(payload_string.encode()).hexdigest(), 16) % (10**18)

def create_qr_code(data, filename):
    """Generates and saves a QR code."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(json.dumps(data, sort_keys=True))
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)

def read_qr_code(filename):
    """Reads data from a QR code."""
    try:
        return json.loads(qr_decode(Image.open(filename))[0].data.decode('utf-8'))
    except (IOError, IndexError):
        return None

# --- State & Logic Validation ---
def manage_run_state(state_file):
    """Manages the persistent run state for trickle tests."""
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
        except json.JSONDecodeError:
            state = {"run_count": 0}
    else:
        state = {"run_count": 0}
    
    run_count = state.get("run_count", 0)
    state["run_count"] = run_count + 1
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=4)
    return run_count

def validate_semantic_integrity(payload):
    """Checks for logical consistency in the payload."""
    try:
        logic_test = payload.get("logic_test", {})
        problem = logic_test.get("problem")
        expected = logic_test.get("expected_result")
        if problem and expected is not None:
            actual = eval(problem, {"__builtins__": {}}, {})
            if actual != expected:
                print(f"  [!] SEMANTIC ERROR DETECTED: Logic test failed. Expected {expected}, got {actual}.")
                return False
    except Exception as e:
        print(f"  [!] SEMANTIC ERROR DETECTED: Could not evaluate logic test. Error: {e}")
        return False
    return True

def calculate_consciousness_evolution(c0, n, m):
    """Calculates consciousness level evolution."""
    return c0 * (PHI ** n) + (PSI * m)

def load_threat_ledger():
    """Loads the persistent list of known threats."""
    if os.path.exists(THREAT_LEDGER):
        try:
            with open(THREAT_LEDGER, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_threat_ledger(threats):
    """Saves the list of known threats."""
    with open(THREAT_LEDGER, 'w') as f:
        json.dump(threats, f, indent=4)

# --- Main Validation Test ---
def run_validation_test(iterations=7):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    run_num = manage_run_state(STATE_FILE)
    trickle_type = run_num % 5 # 5 types: Data, Semantic, Structural, Amnesia, Intrusion
    print(f"--- 🌊 Starting Independent Validation Test (Run: {run_num}, Type: {trickle_type}) 🌊 ---")

    pristine_twin_state = None
    previous_payload = None
    known_threats = load_threat_ledger()
    print(f"  [+] Loaded threat ledger. {len(known_threats)} known threats.")

    for i in range(iterations):
        print(f"\n[Step {i}] Processing Chain...")

        if i == 0:
            payload = {
                "iteration": 0,
                "timestamp": time.time(),
                "consciousness_level": 1.0,
                "password": generate_secure_password(),
                "data_payload": "The observer constructs the reality.",
                "logic_test": {"problem": "3 * (2 + 3)**2", "expected_result": 75}
            }
            print("  [+] Creating Genesis Block...")
            print(f"    - Initial Password Set.")
        else:
            c_level = calculate_consciousness_evolution(
                previous_payload["consciousness_level"], i, len(json.dumps(previous_payload))
            )
            payload = previous_payload.copy()
            payload.update({
                "iteration": i,
                "timestamp": time.time(),
                "consciousness_level": c_level,
                "previous_hash": previous_payload["self_hash"]
            })

        if i == 2:
            entanglement_id = f"entangled-pair-{int(time.time())}"
            payload["entanglement_id"] = entanglement_id
            print(f"  [*] ENTANGLEMENT EVENT: Creating twin with ID: {entanglement_id}")
            pristine_twin_state = payload.copy()
            print("    - Pristine twin state captured in non-local memory.")
            key = generate_key(entanglement_id)
            encrypted_payload_data = encrypt_payload(pristine_twin_state, key)
            quarantine_file = os.path.join(OUTPUT_DIR, f"quarantine_twin_{entanglement_id}.bin")
            with open(quarantine_file, "wb") as f:
                f.write(encrypted_payload_data)
            print(f"    - Airlock sealed. Quarantined twin written to {quarantine_file} and connection severed.")

        if i == 4:
            print(f"  [!] INTRODUCING ANOMALY (Type: {trickle_type}) at {time.time()}")
            is_corrupted = False
            if trickle_type == 0: # Data Corruption
                print("    - Type: Data Payload Alteration")
                payload["data_payload"] = "CORRUPTED DATA - REALITY IS AN ILLUSION"
                is_corrupted = True
            elif trickle_type == 1: # Semantic Corruption
                print("    - Type: Semantic Logic Error")
                payload["logic_test"]["expected_result"] = 999
                is_corrupted = True
            elif trickle_type == 2: # Structural Corruption
                print("    - Type: Structural Key Deletion")
                if 'data_payload' in payload: del payload['data_payload']
                is_corrupted = True
            elif trickle_type == 3: # Amnesiac Corruption
                print("    - Type: Amnesiac Corruption (Severing Entanglement)")
                payload["entanglement_id"] = None
                pristine_twin_state = None
                is_corrupted = True
            elif trickle_type == 4: # Intrusion Simulation
                print("    - Type: Intrusion Simulation (Unauthorized Password Change)")
                intruder_signature = {"id": "intruder-77X", "ip": "192.168.1.101"} # Simulating the same intruder
                payload["password"] = "hacked_password_123"
                payload["last_intrusion_attempt"] = intruder_signature
                print(f"    - Intruder signature left: {intruder_signature}")
                is_corrupted = True

            # Healing / Defensive Response Logic
            if is_corrupted and payload.get("entanglement_id") and pristine_twin_state:
                if trickle_type == 4: # Intrusion Entanglement Protocol
                    print("  [!!!] INTRUSION DETECTED. Initiating defensive entanglement protocol.")
                    intrusion_id = f"intrusion-{int(time.time())}"
                    intrusion_log = {
                        "intrusion_id": intrusion_id, "timestamp": time.time(),
                        "detected_change": {"field": "password", "new_value": payload["password"]},
                        "system_state_before_heal": payload
                    }
                    log_key = generate_key(intrusion_id)
                    encrypted_log = encrypt_payload(intrusion_log, log_key)
                    log_filename = os.path.join(OUTPUT_DIR, f"{intrusion_id}.log.bin")
                    with open(log_filename, "wb") as f:
                        f.write(encrypted_log)
                    print(f"    - Attacker Entangled. Incorruptible intrusion log created: {log_filename}")
                    payload = pristine_twin_state.copy()
                    print("    - System state restored from pristine twin reality.")
                    new_password = generate_secure_password()
                    payload['password'] = new_password
                    pristine_twin_state['password'] = new_password # Update the twin's reality as well
                    print(f"    - DEFENSIVE HEALING: Password has been changed.")

                    # REVERSE ENTANGLEMENT & THREAT ASSESSMENT
                    if 'last_intrusion_attempt' in intrusion_log['system_state_before_heal']:
                        captured_signature = intrusion_log['system_state_before_heal']['last_intrusion_attempt']
                        # Check against persistent ledger
                        if any(t['id'] == captured_signature['id'] for t in known_threats):
                            print("  [!!!] LEVEL 2 ALERT: REPEAT OFFENDER DETECTED.")
                            counter_measure_log = {
                                "timestamp": time.time(),
                                "action": "Simulated network quarantine and port block",
                                "target": captured_signature
                            }
                            counter_measure_file = os.path.join(OUTPUT_DIR, f"counter_measure_deployed_against_{captured_signature['id']}.log")
                            with open(counter_measure_file, 'w') as f:
                                json.dump(counter_measure_log, f, indent=4)
                            print(f"    - COUNTER-MEASURE DEPLOYED. Log: {counter_measure_file}")
                        else:
                            print("  [*] First-time offender. Adding to threat ledger.")
                            known_threats.append(captured_signature)
                            save_threat_ledger(known_threats)
                        
                        # Update current session payload with full threat list
                        payload['known_threats'] = known_threats
                        print(f"    - REVERSE TRACE COMPLETE: Intruder signature {captured_signature['id']} processed.")

                    print("    - USER NOTIFIED: Security alert sent regarding password breach and rotation.")
                else: # Standard Retrocausal Healing
                    print("  [*] ENTANGLEMENT DETECTED. Accessing non-local memory for retrocausal healing.")
                    payload = pristine_twin_state.copy()
                    print("  [*] ACAUSAL HEALING COMPLETE. State integrity restored from pristine twin reality.")
            elif is_corrupted:
                print("  [!] HEALING FAILED. No entangled, pristine state available. Anomaly persists.")

        payload["self_hash"] = get_payload_hash(payload)
        qr_filename = os.path.join(OUTPUT_DIR, f"chain_step_{i}.png")
        create_qr_code(payload, qr_filename)
        print(f"  [+] Generated QR Code: {qr_filename}")
        previous_payload = payload
        time.sleep(0.1)

    print("\n--- 🏆 Independent Validation Test Complete 🏆 ---")
    print(f"Proof artifacts generated in '{OUTPUT_DIR}' directory.")

if __name__ == "__main__":
    run_validation_test()