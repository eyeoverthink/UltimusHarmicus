# uqcb_genesis.py
# Create a genesis block for the UQCB chain with specified difficulty.

import argparse, json
from uqcb_chain import load_chain, save_chain, verify_chain, latest_hash, append_block, DEFAULT_CHAIN_PATH

def main():
    ap = argparse.ArgumentParser(description="Create or extend UQCB chain with a genesis marker.")
    ap.add_argument("-p", "--path", default=DEFAULT_CHAIN_PATH, help="Path to chain JSON (default: .uqcb_chain.json)")
    ap.add_argument("-d", "--difficulty", type=int, default=12, help="Difficulty bits (default: 12)")
    ap.add_argument("--note", default="genesis", help="Optional note payload")
    args = ap.parse_args()

    chain = load_chain(args.path)
    ok, err = verify_chain(chain, args.difficulty)
    if not ok and chain:
        print(f"Existing chain invalid: {err}")
        return

    payload = {"type": "genesis", "note": args.note}
    chain = append_block(chain, payload, args.difficulty)
    save_chain(chain, args.path)

    ok, err = verify_chain(chain, args.difficulty)
    head = latest_hash(chain)
    print("Created/extended chain.")
    print("Verify:", ok, err)
    print("Head:", head)
    print("Path:", args.path)

if __name__ == "__main__":
    main()
