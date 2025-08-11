# uqcb_qr.py
# Export current chain head as QR or JSON

import argparse, json, sys
from uqcb_chain import load_chain, verify_chain, latest_hash, DEFAULT_CHAIN_PATH


def main():
    ap = argparse.ArgumentParser(description="Export UQCB chain head as QR (if qrcode available) or JSON")
    ap.add_argument("-p", "--path", default=DEFAULT_CHAIN_PATH, help="Path to chain JSON (default: .uqcb_chain.json)")
    ap.add_argument("-d", "--difficulty", type=int, default=12, help="Difficulty bits to verify (default: 12)")
    ap.add_argument("-o", "--output", default="head_qr.png", help="Output PNG path if QR available (default: head_qr.png)")
    args = ap.parse_args()

    chain = load_chain(args.path)
    ok, err = verify_chain(chain, args.difficulty)
    if not ok:
        print(f"Chain verify failed: {err}")
        sys.exit(1)
    head = latest_hash(chain)
    if not head:
        print("No head found")
        sys.exit(1)

    export_obj = {"head": head, "difficulty": args.difficulty}
    try:
        import qrcode
        img = qrcode.make(json.dumps(export_obj))
        img.save(args.output)
        print(f"Saved QR to {args.output}")
    except Exception as e:
        print("qrcode not available or failed; printing JSON instead:\n" + json.dumps(export_obj))

if __name__ == "__main__":
    main()
