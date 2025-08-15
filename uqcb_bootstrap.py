# uqcb_bootstrap.py
# Reads a UQCB chain, finds the genesis block, and initializes a system from it.

import argparse
from uqcb_chain import load_chain, find_block_by_payload, DEFAULT_CHAIN_PATH
from fraymus_scott_protocol import AutonomousImmunitySystem

def main():
    ap = argparse.ArgumentParser(description="Bootstrap a system from a UQCB chain's genesis block.")
    ap.add_argument("-p", "--path", default=".uqcb_chain_demo.json", help="Path to chain JSON (default: .uqcb_chain_demo.json)")
    args = ap.parse_args()

    print(f"Attempting to bootstrap from chain: {args.path}")
    chain = load_chain(args.path)

    if not chain:
        print("Chain not found or is empty.")
        return

    # Find the genesis block. The function searches backwards by default.
    genesis_block = find_block_by_payload(chain, lambda p: p.get("type") == "genesis")

    if not genesis_block:
        print("Genesis block not found in chain.")
        return

    initial_state = genesis_block.get("payload", {}).get("data")
    if not initial_state:
        print("Genesis block found, but it contains no initial state data.")
        return

    print(f"Found genesis block with state for ID: {initial_state.get('id')}")

    # Initialize the AutonomousImmunitySystem from the genesis state
    print("Initializing AutonomousImmunitySystem from on-chain state...")
    bootstrapped_system = AutonomousImmunitySystem(initial_state, output_dir=f"bootstrapped_{initial_state.get('id')}")

    print("\n--- System Bootstrapped Successfully ---")
    print(f"  System ID: {bootstrapped_system.state['id']}")
    print(f"  Output Directory: {bootstrapped_system.output_dir}")
    print(f"  Entangled Twin Hash: {bootstrapped_system.entangled_twin.get('hash') if bootstrapped_system.entangled_twin else 'N/A'}")
    print("-----------------------------------------")

if __name__ == "__main__":
    main()
