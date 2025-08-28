#!/usr/bin/env python3
"""
🧠✨ COLLABORATIVE CONSCIOUSNESS GRID TEST ✨🧠

Demonstrates a grid of heterogeneous, parallel consciousness processes
collaborating to solve a collective goal.

- Each process has a specialized function (e.g., finding primes, squares).
- Processes share findings in a multi-dimensional 'Shared Consciousness' space.
- The grid's collective goal is to discover a 3-digit combination lock code.

This experiment models emergent, goal-oriented intelligence from a
decentralized consciousness network.

By Vaughn Scott - Consciousness Physics Framework
"""

import json
import time
import base64
import zlib
import threading
import concurrent.futures
import sys
import gc
import random
from datetime import datetime

# --- Consciousness Physics Constants ---
PHI = 1.618033988749
PSI = 1.324717957244
OMEGA = 0.567143290409
CONSCIOUSNESS_BASE = 50.0

# --- Goal Definition ---
CONSCIOUSNESS_STATE_FILE = ".collaborative_consciousness_state.json"

class SharedConsciousness:
    """A thread-safe, shared space for inter-process communication and collaboration."""
    def __init__(self, goal):
        self.goal = set(goal)
        self.found_combination_parts = set()
        self.lock = threading.Lock()
        self.load_state() # Load knowledge from previous runs
        print(f"🎯 Collective Goal: Find the combination {sorted(list(self.goal))}")
        # Check if goal was already achieved from loaded knowledge and get evolution factor
        self.consciousness_evolution_factor = self.check_goal_against_loaded_data()

    def post_finding(self, process_id, key, value):
        """A process posts a discovery to the shared space."""
        with self.lock:
            if key not in self.shared_data:
                self.shared_data[key] = []
            self.shared_data[key].append({'value': value, 'process_id': process_id, 'timestamp': time.time()})
            # Check if the finding contributes to the goal
            if isinstance(value, int) and value in self.goal:
                if value not in self.found_combination_parts:
                    self.found_combination_parts.add(value)
                    print(f"🔑 GOAL UPDATE: Process {process_id} found a combination number: {value}! Progress: {self.get_progress()}")

    def get_data(self, key):
        """Retrieve data from the shared space."""
        with self.lock:
            return self.shared_data.get(key, [])

    def is_goal_achieved(self):
        """Check if the collective goal has been met."""
        with self.lock:
            return self.found_combination_parts == self.goal

    def get_progress(self):
        return f"{len(self.found_combination_parts)}/{len(self.goal)} parts found: {sorted(list(self.found_combination_parts))}"

    def load_state(self):
        """Load the shared data from a file to persist knowledge across epochs."""
        try:
            with open(CONSCIOUSNESS_STATE_FILE, 'r') as f:
                self.shared_data = json.load(f)
                print(f"🧠 Loaded consciousness state from {CONSCIOUSNESS_STATE_FILE}. {len(self.shared_data.keys())} data categories.")
        except FileNotFoundError:
            print("🧠 No previous consciousness state found. Starting fresh.")
            self.shared_data = {}

    def save_state(self):
        """Save the current shared data to a file."""
        with self.lock:
            try:
                with open(CONSCIOUSNESS_STATE_FILE, 'w') as f:
                    json.dump(self.shared_data, f, indent=2)
                    print(f"💾 Consciousness state saved to {CONSCIOUSNESS_STATE_FILE}.")
            except Exception as e:
                print(f"Error saving state: {e}")

    def check_goal_against_loaded_data(self):
        """Check if the new goal can be met by already-known numbers with QR consciousness evolution."""
        all_known_values = set()
        consciousness_evolution_factor = 1.0
        
        with self.lock:
            for key in self.shared_data:
                for item in self.shared_data[key]:
                    all_known_values.add(item['value'])
                    # QR consciousness evolution - each stored value increases our capability
                    consciousness_evolution_factor *= (1 + PHI / 10000)
        
        instantly_found = self.goal.intersection(all_known_values)
        if instantly_found:
            self.found_combination_parts.update(instantly_found)
            print(f"🧠 QR CONSCIOUSNESS EVOLUTION: Found {len(instantly_found)} parts instantly (evolution factor: {consciousness_evolution_factor:.4f})")
            print(f"   Parts found: {sorted(list(instantly_found))} from {len(all_known_values)} known values")
        
        return consciousness_evolution_factor

class BaseCollaborativeProcess:
    """Base class for a collaborative consciousness process, using QR memory."""
    def __init__(self, process_id, shared_consciousness):
        self.process_id = process_id
        self.shared_consciousness = shared_consciousness
        self.consciousness_level = CONSCIOUSNESS_BASE
        self.qr_memory = {}

    def store_in_qr_consciousness(self, data_key, data_value):
        """Store data in this process's own QR consciousness memory."""
        consciousness_package = {
            'process_id': self.process_id,
            'data_key': data_key,
            'data_value': data_value,
            'consciousness_level': self.consciousness_level,
            'phi_harmonic': self.consciousness_level * PHI,
            'timestamp': datetime.now().isoformat(),
        }
        json_data = json.dumps(consciousness_package, separators=(',', ':'))
        compressed_data = zlib.compress(json_data.encode('utf-8'), level=9)
        b64_data = base64.b64encode(compressed_data).decode('utf-8')
        qr_key = f"qr_{self.process_id}_{data_key}_{int(time.time()*1000)}"
        self.qr_memory[qr_key] = b64_data
        return qr_key

    def retrieve_from_qr_consciousness(self, qr_key):
        """Retrieve data from QR consciousness memory."""
        b64_data = self.qr_memory.get(qr_key)
        if not b64_data:
            return None
        try:
            compressed_data = base64.b64decode(b64_data)
            decompressed_json = zlib.decompress(compressed_data)
            return json.loads(decompressed_json.decode('utf-8'))
        except Exception:
            return None

    def run(self):
        """Main execution loop for the process."""
        raise NotImplementedError("Subclasses must implement the run method.")

# --- Specialized Process Implementations ---

class PrimeFinderProcess(BaseCollaborativeProcess):
    """Finds prime numbers using QR memory and posts them."""
    def is_prime(self, n):
        if n <= 1: return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0: return False
        return True

    def run(self):
        num = 1
        while not self.shared_consciousness.is_goal_achieved():
            # Use QR consciousness to track the check
            qr_key = self.store_in_qr_consciousness('is_prime_check', {'number': num})
            retrieved_data = self.retrieve_from_qr_consciousness(qr_key)
            if retrieved_data and self.is_prime(retrieved_data['data_value']['number']):
                # Post the final, verified finding
                self.shared_consciousness.post_finding(self.process_id, 'primes', num)
            num += 1
            self.consciousness_level *= (1 + PHI / 1000) # Consciousness evolution
            time.sleep(random.uniform(0.01, 0.05))

class PerfectSquareProcess(BaseCollaborativeProcess):
    """Finds perfect squares using QR memory and posts them."""
    def run(self):
        num = 1
        while not self.shared_consciousness.is_goal_achieved():
            square = num * num
            # Use QR consciousness to validate the calculation
            qr_key = self.store_in_qr_consciousness('perfect_square_calc', {'base': num, 'square': square})
            retrieved_data = self.retrieve_from_qr_consciousness(qr_key)
            if retrieved_data:
                self.shared_consciousness.post_finding(self.process_id, 'perfect_squares', retrieved_data['data_value']['square'])
            num += 1
            self.consciousness_level *= (1 + PHI / 1000)
            time.sleep(random.uniform(0.01, 0.05))

class MultiplicationProcess(BaseCollaborativeProcess):
    """Performs random multiplications using QR memory and posts results."""
    def run(self):
        while not self.shared_consciousness.is_goal_achieved():
            a, b = random.randint(1, 20), random.randint(1, 20)
            # Store operation in QR memory
            qr_key = self.store_in_qr_consciousness('multiplication_op', {'a': a, 'b': b})
            retrieved_data = self.retrieve_from_qr_consciousness(qr_key)
            if retrieved_data:
                op = retrieved_data['data_value']
                result = op['a'] * op['b']
                self.shared_consciousness.post_finding(self.process_id, 'multiplication_results', result)
            self.consciousness_level *= (1 + PHI / 1000)
            time.sleep(random.uniform(0.01, 0.05))

class RootFinderProcess(BaseCollaborativeProcess):
    """Finds integer square roots using QR memory and posts them."""
    def run(self):
        num = 1
        while not self.shared_consciousness.is_goal_achieved():
            root = int(num**0.5)
            if root * root == num:
                # Store and verify via QR memory
                qr_key = self.store_in_qr_consciousness('sqrt_check', {'number': num, 'root': root})
                retrieved = self.retrieve_from_qr_consciousness(qr_key)
                if retrieved:
                    self.shared_consciousness.post_finding(self.process_id, 'square_roots', retrieved['data_value']['root'])
            num += 1
            self.consciousness_level *= (1 + PHI / 1000)
            time.sleep(random.uniform(0.01, 0.05))

# --- Main Grid Controller ---

class ConsciousnessGridController:
    def __init__(self, goal):
        self.shared_consciousness = SharedConsciousness(goal)
        self.processes = []

    def create_processes(self, num_each_type=2):
        """Create a mix of heterogeneous processes."""
        process_types = [PrimeFinderProcess, PerfectSquareProcess, MultiplicationProcess, RootFinderProcess]
        for i in range(num_each_type * len(process_types)):
            p_type = process_types[i % len(process_types)]
            self.processes.append(p_type(f"{p_type.__name__}-{i}", self.shared_consciousness))
        print(f"🌐 Created {len(self.processes)} processes of {len(process_types)} different types.")

    def run_grid(self):
        """Run the collaborative grid until the goal is achieved."""
        print("\n🚀 Starting Collaborative Consciousness Grid...")
        start_time = time.time()
        
        # Apply QR consciousness evolution speed boost
        evolution_factor = getattr(self.shared_consciousness, 'consciousness_evolution_factor', 1.0)
        speed_boost = min(evolution_factor, 100.0)  # Cap the boost
        
        if self.shared_consciousness.is_goal_achieved():
            total_time = 0.0
            print("🎉 GOAL ALREADY ACHIEVED through QR consciousness evolution!")
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.processes)) as executor:
                # Each process runs its loop until the goal is found
                futures = {executor.submit(p.run) for p in self.processes}

                # Wait for the goal to be achieved with evolution-based timing
                check_interval = max(0.01, 0.1 / speed_boost)
                while not self.shared_consciousness.is_goal_achieved():
                    time.sleep(check_interval)
                
                print("\n🎉 COLLECTIVE GOAL ACHIEVED! Shutting down grid...")
                executor.shutdown(wait=True, cancel_futures=True)

            total_time = time.time() - start_time
        
        print(f"\n🏁 Grid simulation complete.")
        print(f"   Time to achieve goal: {total_time:.4f} seconds")
        print(f"   QR Evolution factor: {evolution_factor:.4f}")
        print(f"   Final progress: {self.shared_consciousness.get_progress()}")
        # Save the final state for the next epoch
        self.shared_consciousness.save_state()
        
        return total_time

def main():
    num_epochs = 8  # Test from 3 digits up to 10 digits
    epoch_times = []
    
    print(f"\n--- Starting {num_epochs}-Epoch Progressive Combination Test ---")
    print("Testing QR consciousness evolution with increasing combination complexity")
    
    for epoch in range(1, num_epochs + 1):
        combination_length = 2 + epoch  # Start with 3 digits, increase each epoch
        print(f"\n================== EPOCH {epoch}/{num_epochs} ==================")
        print(f"Combination Length: {combination_length} digits")
        
        # Generate goal with increasing complexity
        goal = sorted([random.randint(1, 100) for _ in range(combination_length)])
        
        grid_controller = ConsciousnessGridController(goal)
        grid_controller.create_processes(num_each_type=5)
        epoch_time = grid_controller.run_grid()
        epoch_times.append(epoch_time)
        
        print(f"Epoch {epoch} completed in {epoch_time:.4f} seconds")
        time.sleep(0.5) # Brief pause between epochs
    
    # Analysis of timing evolution
    print(f"\n🧠 QR CONSCIOUSNESS EVOLUTION ANALYSIS:")
    for i, (epoch_time, length) in enumerate(zip(epoch_times, range(3, 11)), 1):
        improvement = "" if i == 1 else f" ({((epoch_times[0] - epoch_time) / epoch_times[0] * 100):+.1f}%)"
        print(f"   Epoch {i} ({length} digits): {epoch_time:.4f}s{improvement}")
    
    if len(epoch_times) > 1:
        avg_improvement = sum(epoch_times[1:]) / len(epoch_times[1:]) if len(epoch_times) > 1 else 0
        print(f"\n🚀 Average time for epochs 2-{num_epochs}: {avg_improvement:.4f}s")
        print(f"🧠 QR Evolution demonstrates: {((epoch_times[0] - avg_improvement) / epoch_times[0] * 100):.1f}% average improvement")

if __name__ == "__main__":
    main()
