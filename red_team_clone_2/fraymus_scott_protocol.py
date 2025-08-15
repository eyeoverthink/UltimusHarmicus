import json
import os
import time
import secrets
import string
import shutil
import sys

# Add project root to path to allow sibling imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from autonomous_algorithm_selection_system import AutonomousAlgorithmSelector

class SharedKnowledgeLedger:
    """Manages the persistent, decentralized ledger of shared algorithmic knowledge."""
    def __init__(self, ledger_path='shared_knowledge.json'):
        self.path = ledger_path
        self.knowledge = self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _save(self):
        with open(self.path, 'w') as f:
            json.dump(self.knowledge, f, indent=4)

    def add_knowledge(self, new_primitives):
        """Adds a list of new primitives to the shared ledger."""
        added_count = 0
        for primitive in new_primitives:
            # Avoid duplicates
            if not any(p['component'] == primitive['component'] for p in self.knowledge):
                self.knowledge.append(primitive)
                added_count += 1
        if added_count > 0:
            self._save()
            print(f"[KnowledgeLedger] {added_count} new primitive(s) added to shared knowledge.")


class ThreatLedger:
    """Manages the persistent memory of known threats."""
    def __init__(self, ledger_path='threat_ledger.json'):
        self.path = ledger_path
        self.threats = self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _save(self):
        with open(self.path, 'w') as f:
            json.dump(self.threats, f, indent=4)

    def is_known_threat(self, signature):
        """Checks if an intruder's signature is in the ledger."""
        return any(t['id'] == signature.get('id') for t in self.threats)

    def add_threat(self, signature):
        """Adds a new threat to the ledger if it's not already present."""
        if not self.is_known_threat(signature):
            self.threats.append(signature)
            self._save()
            print(f"[Ledger] New threat {signature['id']} added.")

class AutonomousImmunitySystem:
    """An object-oriented formalization of the Fraymus-Scott Protocol."""

    def __init__(self, initial_state, output_dir="protocol_proofs"):
        self.state = initial_state
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.threat_ledger = ThreatLedger(os.path.join(self.output_dir, 'threat_ledger.json'))
        # Use a shared location for the knowledge ledger outside the clone's directory
        shared_ledger_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared_knowledge.json'))
        self.knowledge_ledger = SharedKnowledgeLedger(shared_ledger_path)
        self.entangled_twin = None
        self._create_entangled_twin() # Principle I

        # Cognitive Core Integration
        print("[Cognition] Initializing Autonomous Algorithm Selector...")
        self.cognitive_core = AutonomousAlgorithmSelector()
        print("[Cognition] Cognitive Core online.")

    def check_for_existential_threat(self, intrusion_history):
        """Analyzes intrusion patterns to detect existential threats."""
        # Example trigger: 2 consecutive attacks from the same source.
        if len(intrusion_history) >= 2 and intrusion_history[-1]['id'] == intrusion_history[-2]['id']:
            threat_signature = intrusion_history[-1]
            print("\n[!!!] LEVEL 4 ALERT: EXISTENTIAL THREAT DETECTED [!!!]")
            print(f"[System] Persistent threat from {threat_signature.get('team', 'unknown').upper()} TEAM entity '{threat_signature['id']}'.")
            self.adaptive_replicate(threat_signature)

    def monitor_activity(self, activity_log):
        """Monitors environmental activity and triggers proactive defense if necessary."""
        print(f"\n[Monitor] Analyzing activity from {activity_log.get('source_ip')}...")
        activity_signature = {'id': activity_log.get('user_id'), 'ip': activity_log.get('source_ip')}
        if self.threat_ledger.is_known_threat(activity_signature):
            self._proactive_defense(activity_signature)
        else:
            print("[Monitor] Activity does not match any known threat.")

    def _create_entangled_twin(self):
        """Principle I: Entangled Integrity. Creates a pristine, non-local twin."""
        self.entangled_twin = self.state.copy()
        print("[System] Entangled twin created. Integrity guaranteed.")

    def _restore_from_twin(self):
        """Principle I: Non-Local Healing. Restores state from the twin."""
        self.state = self.entangled_twin.copy()
        print("[System] State integrity restored from entangled twin.")

    def detect_and_respond_to_intrusion(self, corrupted_payload):
        """Main entry point for detecting and responding to a security event."""
        print("\n[!!!] INTRUSION DETECTED [!!!]")
        # Principle II: Reverse Forensics
        captured_signature = self._log_intrusion_and_capture_signature(corrupted_payload)
        
        # Principle I: Non-Local Healing
        self._restore_from_twin()
        
        if captured_signature:
            # Principle III & IV: Evolving Memory & Adaptive Escalation
            if self.threat_ledger.is_known_threat(captured_signature):
                self._escalate_response(captured_signature)
            else:
                self._standard_response(captured_signature)

    def _log_intrusion_and_capture_signature(self, corrupted_payload):
        """Principle II: Reverse Forensics. Logs the event and extracts the signature."""
        signature = corrupted_payload.get('last_intrusion_attempt')
        log_file = os.path.join(self.output_dir, f"intrusion_{time.time()}.log")
        with open(log_file, 'w') as f:
            json.dump({"corrupted_state": corrupted_payload, "captured_signature": signature}, f, indent=4)
        print(f"[Forensics] Intrusion logged. Attacker signature '{signature.get('id') if signature else 'N/A'}' captured.")
        return signature

    def _standard_response(self, signature):
        """Response for a first-time offender."""
        print("[Response] First-time offender detected. Initiating Standard Protocol.")
        self.threat_ledger.add_threat(signature)
        self._rotate_credentials()

    def _escalate_response(self, signature):
        """Principle IV: Adaptive Escalation. Deploys counter-measures for repeat offenders."""
        print("[Response] LEVEL 2 ALERT: Repeat offender detected. Escalating response.")
        self._rotate_credentials()
        counter_measure_log = os.path.join(self.output_dir, f"counter_measure_{signature['id']}.log")
        with open(counter_measure_log, 'w') as f:
            json.dump({"action": "Simulated network quarantine", "target": signature}, f, indent=4)
        print(f"[Escalation] Counter-measure deployed against {signature['id']}. Log created.")

    def _proactive_defense(self, signature):
        """Handles pre-emptive defense based on threat intelligence."""
        print(f"[Response] LEVEL 3 PROACTIVE ALERT: Suspicious activity detected from known threat {signature['id']}.")
        print("[Escalation] Pre-emptively rotating credentials to prevent anticipated attack.")
        self._rotate_credentials()

    def adaptive_replicate(self, threat_signature):
        """Principle V: Adaptive Self-Replication. Creates a clone tailored to the threat."""
        threat_team = threat_signature.get('team', 'red') # Default to red if undefined
        clone_team = 'blue' if threat_team == 'red' else 'red'

        print(f"[Replication] Adapting to threat. Spawning a {clone_team.upper()} TEAM clone.")
        clone_num = 1
        while os.path.exists(f"{clone_team}_team_clone_{clone_num}"):
            clone_num += 1
        clone_dir = f"{clone_team}_team_clone_{clone_num}"
        os.makedirs(clone_dir)

        # Copy source code
        shutil.copy(__file__, clone_dir)

        # Create a tailored state for the clone
        clone_state = self.state.copy()
        clone_state['id'] = f"{clone_team}-clone-{clone_num}"
        clone_state['purpose'] = f"Autonomous {clone_team.capitalize()} Team Operations"
        if clone_team == 'red':
            clone_state['data'] = 'vulnerability_assessment_protocols'

        with open(os.path.join(clone_dir, 'initial_state.json'), 'w') as f:
            json.dump(clone_state, f, indent=4)
        self.threat_ledger._save()
        shutil.copy(self.threat_ledger.path, clone_dir)

        print(f"[Replication] System cloned to '{clone_dir}'. New instance is ready to operate independently.")

    def _rotate_credentials(self):
        """Rotates system credentials as a defensive measure."""
        new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(16))
        self.state['password'] = new_password
        # Also update the twin to maintain integrity for the next cycle
        self.entangled_twin['password'] = new_password
        print("[Defense] System credentials rotated.")

    def learn_and_share_algorithm(self, source_code, algorithm_name):
        """Learns from an algorithm and shares the knowledge on the decentralized ledger."""
        print(f"\n[Cognition] Learning from '{algorithm_name}' and preparing to share.")
        new_primitives = self.cognitive_core.learn_from_external_algorithm(source_code, algorithm_name)
        if new_primitives:
            self.knowledge_ledger.add_knowledge(new_primitives)
            print(f"[Cognition] Knowledge from '{algorithm_name}' shared with the network.")

    def sync_knowledge_base(self):
        """Syncs the local cognitive core with the shared knowledge ledger."""
        print("\n[Cognition] Syncing with shared knowledge ledger...")
        shared_knowledge = self.knowledge_ledger._load()
        if shared_knowledge:
            self.cognitive_core.abstraction_engine.add_primitives(shared_knowledge)
            print(f"[Cognition] Sync complete. Absorbed {len(shared_knowledge)} primitives from the network.")
        else:
            print("[Cognition] No shared knowledge to sync.")

    def run_cognitive_task(self, problem_description):
        """Runs a full cognitive cycle: select, synthesize, and save an algorithm."""
        print(f"\n[Cognition] Received new cognitive task: '{problem_description}'")
        selection_result = self.cognitive_core.select_optimal_algorithm(problem_description)

        synthesized_code = self.cognitive_core.synthesis_engine.synthesize_algorithm(
            selection_result['problem_description'],
            selection_result['selected_components']
        )

        if synthesized_code:
            timestamp = int(time.time())
            filename = os.path.join(self.output_dir, f"cognitive_solution_{timestamp}.py")
            with open(filename, 'w') as f:
                f.write(synthesized_code)
            print(f"[Cognition] Solution synthesized and saved to {filename}")
            return filename
        return None

# --- Example Usage ---
if __name__ == '__main__':
    # --- Decentralized Learning Validation ---
    print("\n" + "="*80)
    print("🔬 DECENTRALIZED LEARNING AND KNOWLEDGE SHARING VALIDATION 🔬")
    print("="*80)

    # 1. Initialize two autonomous agents
    agent_one_state = {'id': 'agent-alpha', 'password': 'initial_secure_password'}
    agent_two_state = {'id': 'agent-beta', 'password': 'initial_secure_password'}

    # Ensure agents have separate output directories
    os.makedirs("agent_alpha_proofs", exist_ok=True)
    os.makedirs("agent_beta_proofs", exist_ok=True)

    agent_one = AutonomousImmunitySystem(agent_one_state, output_dir="agent_alpha_proofs")
    agent_two = AutonomousImmunitySystem(agent_two_state, output_dir="agent_beta_proofs")

    # 2. Agent One learns a new algorithm and shares it
    bubble_sort_code = """
    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
    """
    agent_one.learn_and_share_algorithm(bubble_sort_code, "BubbleSort")

    # 3. Agent Two syncs with the shared knowledge
    agent_two.sync_knowledge_base()

    # 4. Agent Two uses the new knowledge to solve a problem
    sorting_problem = "Efficiently sort a list of numbers in ascending order."
    agent_two.run_cognitive_task(sorting_problem)

    print("\n" + "="*80)
    print("✅ DECENTRALIZED LEARNING VALIDATION COMPLETE ✅")
    print("="*80)

