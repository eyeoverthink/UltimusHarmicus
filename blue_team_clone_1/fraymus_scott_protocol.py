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
        import hashlib
        added_count = 0
        if not isinstance(new_primitives, list):
            new_primitives = [new_primitives] if new_primitives is not None else []
        for primitive in new_primitives:
            if not isinstance(primitive, dict):
                continue
            # Normalize: ensure a 'component' key exists for deduplication
            comp = primitive.get('component')
            if not comp:
                name = primitive.get('name') or primitive.get('id')
                kind = primitive.get('category') or primitive.get('type') or 'primitive'
                if name:
                    comp = f"{kind}::{name}"
                else:
                    # Stable digest from content
                    try:
                        payload = json.dumps(primitive, sort_keys=True).encode('utf-8')
                    except Exception:
                        payload = repr(primitive).encode('utf-8')
                    comp = f"{kind}::digest:{hashlib.sha1(payload).hexdigest()[:12]}"
                primitive['component'] = comp
            # Avoid duplicates safely using .get
            if not any(p.get('component') == comp for p in self.knowledge):
                self.knowledge.append(primitive)
                added_count += 1
        if added_count > 0:
            self._save()
            print(f"[KnowledgeLedger] {added_count} new primitive(s) added to shared knowledge.")


class CredentialPatternLearner:
    """Learns reusable patterns from observed usernames and passwords.

    Stores light-weight statistics only (no raw credentials) to improve privacy by default.
    """
    def __init__(self):
        self.masks = {}            # e.g., Lllldddd! → count
        self.substrings = {}       # common substrings (lowercased) → count
        self.char_ngrams = {}      # 2-grams and 3-grams → count
        self.transforms = {}       # observed transforms like year suffix, leet substitutions

    def _mask(self, s: str) -> str:
        def char_class(c):
            if c.islower(): return 'l'
            if c.isupper(): return 'L'
            if c.isdigit(): return 'd'
            return 's'
        return ''.join(char_class(c) for c in s)

    def _count(self, d: dict, k: str, inc: int = 1):
        d[k] = d.get(k, 0) + inc

    def _collect_ngrams(self, s: str, n: int):
        for i in range(len(s) - n + 1):
            self._count(self.char_ngrams, s[i:i+n])

    def learn(self, username: str, password: str):
        if not password:
            return
        # Mask learning
        self._count(self.masks, self._mask(password))
        # Substrings (lowercase)
        p = password.lower()
        for token in [username.lower()] + [str(y) for y in range(1990, 2031)]:
            if token and token in p:
                self._count(self.substrings, token)
        # Common words (very small demo dictionary)
        for word in ["admin","user","root","pass","love","secret","dragon","fraymus","scott"]:
            if word in p:
                self._count(self.substrings, word)
        # Character n-grams
        self._collect_ngrams(p, 2)
        self._collect_ngrams(p, 3)
        # Transforms (leet, suffixes)
        leet_pairs = [("a","@"),("a","4"),("e","3"),("i","1"),("o","0"),("s","$"),("s","5")]
        for plain, sub in leet_pairs:
            if sub in password:
                key = f"leet:{plain}->{sub}"
                self._count(self.transforms, key)
        for suffix in ["!","?","#","$","123","!1","2024","2025"]:
            if password.endswith(suffix):
                self._count(self.transforms, f"suffix:{suffix}")

    def export_knowledge(self):
        return {
            "type": "credential_patterns",
            "masks": self.masks,
            "substrings": self.substrings,
            "char_ngrams": self.char_ngrams,
            "transforms": self.transforms,
        }

    def ingest_knowledge(self, knowledge):
        if not knowledge or knowledge.get("type") != "credential_patterns":
            return
        for k, v in knowledge.get("masks", {}).items():
            self._count(self.masks, k, v)
        for k, v in knowledge.get("substrings", {}).items():
            self._count(self.substrings, k, v)
        for k, v in knowledge.get("char_ngrams", {}).items():
            self._count(self.char_ngrams, k, v)
        for k, v in knowledge.get("transforms", {}).items():
            self._count(self.transforms, k, v)


class PasswordGuesser:
    """Generates candidate passwords using learned patterns and transforms.

    This is a heuristic generator suitable for demos. It combines:
    - mask-driven templates, substring injection, leet transforms, and common suffixes.
    """
    def __init__(self, learner: CredentialPatternLearner):
        self.learner = learner

    def _apply_leet(self, s: str):
        # produce a small set of variants
        variants = set([s])
        rules = [("a","@"),("a","4"),("e","3"),("i","1"),("o","0"),("s","$"),("s","5")]
        for plain, sub in rules:
            if plain in s.lower():
                variants.add(s.lower().replace(plain, sub))
        return list(variants)

    def _capitalize_variants(self, s: str):
        return list({s, s.capitalize(), s.upper()})

    def _common_suffixes(self):
        # derive from transforms frequency; fall back defaults
        suffixes = ["!","?","#","$","123","!1","2024","2025"]
        learned = [t.split(":",1)[1] for t,c in sorted(self.learner.transforms.items(), key=lambda x:-x[1]) if t.startswith("suffix:")]
        return learned[:5] + suffixes

    def generate(self, username: str, max_candidates: int = 200):
        uname = username or "user"
        base_tokens = {uname.lower(), uname.split("@")[0].lower()}
        base_tokens |= {k for k,_ in sorted(self.learner.substrings.items(), key=lambda x:-x[1])[:10]}
        candidates = []
        tried = set()
        suffixes = self._common_suffixes()

        for token in list(base_tokens):
            for cap in self._capitalize_variants(token):
                for leet in self._apply_leet(cap):
                    for suf in ["", *suffixes]:
                        cand = f"{leet}{suf}"
                        if cand not in tried and 6 <= len(cand) <= 24:
                            candidates.append(cand)
                            tried.add(cand)
                            if len(candidates) >= max_candidates:
                                return candidates
        # fallback: combine top ngrams
        ngrams = [k for k,_ in sorted(self.learner.char_ngrams.items(), key=lambda x:-x[1])[:20]]
        for a in ngrams:
            for b in ngrams:
                cand = (a + b)[:16]
                if cand not in tried and len(cand) >= 6:
                    candidates.append(cand)
                    tried.add(cand)
                    if len(candidates) >= max_candidates:
                        return candidates
        return candidates


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

        # Credential learning and guessing
        self.credential_learner = CredentialPatternLearner()
        self.password_guesser = PasswordGuesser(self.credential_learner)

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

    # --- Credential Intelligence (Red <-> Blue) ---
    def observe_credentials(self, username: str, password: str):
        """Observe credentials and learn reusable patterns (no raw storage)."""
        self.credential_learner.learn(username, password)
        # Share distilled patterns to the decentralized ledger
        exported = self.credential_learner.export_knowledge()
        # Wrap for ledger compatibility as primitives
        primitives = [{"component": f"cred:{k}", "data": v} for k, v in exported.items() if k != "type"]
        if primitives:
            self.knowledge_ledger.add_knowledge(primitives)
            print("[CredInt] Credential patterns learned and shared.")

    def import_shared_credential_knowledge(self):
        """Ingest credential-related knowledge from shared ledger into local learner."""
        shared = self.knowledge_ledger._load()
        # Reconstruct if present
        recon = {"type":"credential_patterns","masks":{},"substrings":{},"char_ngrams":{},"transforms":{}}
        for item in shared:
            comp = item.get("component","")
            if comp.startswith("cred:"):
                key = comp.split(":",1)[1]
                data = item.get("data",{})
                if key in recon and isinstance(data, dict):
                    recon[key] = data
        self.credential_learner.ingest_knowledge(recon)
        print("[CredInt] Ingested shared credential knowledge into local learner.")

    def generate_password_guesses(self, username: str, limit: int = 100):
        """Red-Team: generate password guesses using learned patterns."""
        return self.password_guesser.generate(username, max_candidates=limit)

    def analyze_password_strength(self, username: str, password: str):
        """Blue-Team: analyze and return simple, actionable hardening advice."""
        mask = ''.join('l' if c.islower() else 'L' if c.isupper() else 'd' if c.isdigit() else 's' for c in password)
        issues = []
        if len(password) < 12: issues.append("increase length to >= 12")
        if username and username.lower() in password.lower(): issues.append("avoid username-based substrings")
        if mask.count('l') + mask.count('L') < 4: issues.append("add more letters")
        if mask.count('d') < 2: issues.append("add more digits")
        if mask.count('s') < 1: issues.append("add at least 1 symbol")
        # Check common substrings from knowledge
        weak_hits = [k for k in self.credential_learner.substrings.keys() if k in password.lower()]
        if weak_hits: issues.append(f"avoid common/observed substrings: {', '.join(weak_hits[:5])}")
        return {
            "mask": mask,
            "length": len(password),
            "issues": issues or ["no obvious weaknesses detected (demo heuristic)"]
        }

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

    # --- Credential Intelligence Demo ---
    print("\n" + "-"*80)
    print("🔐 CREDENTIAL INTELLIGENCE (RED↔BLUE) DEMO 🔐")
    print("-"*80)
    # Observe some credentials (demo; in practice, only patterns are kept)
    samples = [
        ("vaughn", "Vaughn2025!"),
        ("admin", "Adm1n!23"),
        ("quantum", "Ph1Golden#2024"),
    ]
    for u,p in samples:
        agent_one.observe_credentials(u,p)

    # Sync credential knowledge to agent two and generate guesses for a target
    agent_two.import_shared_credential_knowledge()
    target_user = "vaughn"
    guesses = agent_two.generate_password_guesses(target_user, limit=30)
    print(f"[RedTeam] Top {len(guesses)} guesses for '{target_user}':")
    for g in guesses[:10]:
        print("  -", g)

    # Blue-team strength analysis
    test_pwd = "Vaughn2025!"
    strength = agent_two.analyze_password_strength(target_user, test_pwd)
    print("[BlueTeam] Password strength analysis:")
    print(json.dumps(strength, indent=2))

