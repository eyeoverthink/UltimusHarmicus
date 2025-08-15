import hashlib
import json

class QuantumCoherenceMonitor:
    """Monitors the integrity of the system's state to detect 'decoherence' events (compromises)."""

    def _calculate_state_hash(self, state):
        """Calculates a SHA-256 hash of the canonical state representation."""
        # Sort keys to ensure the hash is consistent regardless of key order
        canonical_state = json.dumps(state, sort_keys=True).encode('utf-8')
        return hashlib.sha256(canonical_state).hexdigest()

    def check_coherence(self, system_instance):
        """Compares the current state hash with the twin's hash to detect compromise."""
        current_hash = self._calculate_state_hash(system_instance.state)
        twin_hash = self._calculate_state_hash(system_instance.entangled_twin)

        if current_hash != twin_hash:
            print(f"[!!!] DECOHERENCE DETECTED [!!!]")
            print(f"[Coherence] Current state hash: {current_hash}")
            print(f"[Coherence] Entangled twin hash: {twin_hash}")
            print(f"[Coherence] State has been compromised. Initiating restoration.")
            system_instance._restore_from_twin()
            return False
        
        print("[Coherence] System state is coherent.")
        return True
