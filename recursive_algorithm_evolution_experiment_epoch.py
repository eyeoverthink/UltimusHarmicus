#!/usr/bin/env python3
"""
Recursive Algorithm Evolution Experiment (Epoch + Chain + QR fallback)
- Does NOT modify originals; safe duplicate.
- Requires valid chain head (see uqcb_genesis.py). Refuses to run otherwise.
- Binds evolution deterministically to current head.
- Stores evolution summary as a PoW-mined block.
- Exports head as QR if qrcode available; else prints JSON.
"""
import argparse, json, time, hashlib
from typing import Any, Dict

from uqcb_chain import load_chain, save_chain, verify_chain, latest_hash, append_block, DEFAULT_CHAIN_PATH

# Optional QR export
try:
    import qrcode  # type: ignore
    HAVE_QR = True
except Exception:
    HAVE_QR = False


def sha256_hex(s: str) -> str:
    import hashlib
    return hashlib.sha256(s.encode()).hexdigest()


def try_import(name: str):
    try:
        return __import__(name)
    except Exception:
        return None


def run_epoch(chain_path: str, difficulty_bits: int) -> None:
    chain = load_chain(chain_path)
    ok, err = verify_chain(chain, difficulty_bits)
    if not ok:
        print(f"Chain invalid: {err}. Create genesis first: python3 uqcb_genesis.py -p {chain_path} -d {difficulty_bits}")
        return
    head = latest_hash(chain)
    if not head:
        print("No head present; run genesis first.")
        return

    # Deterministic seed from head to bind recursion
    seed = sha256_hex(head + "|recursive_algo_epoch")

    # Attempt to import user's prior QR systems
    mods = {
        'qr_recursive_generator': try_import('qr_recursive_generator'),
        'qr_phone_control_loop': try_import('qr_phone_control_loop'),
        'qr_neural_layers_system': try_import('qr_neural_layers_system'),
        'QR_RECURSIVE_CREDENTIAL_LEARNING_SYSTEM': try_import('QR_RECURSIVE_CREDENTIAL_LEARNING_SYSTEM'),
    }

    available = [k for k, v in mods.items() if v is not None]

    # Optionally invoke a main() if present (non-failing, best-effort)
    invoked = []
    for name, mod in mods.items():
        if mod is None:
            continue
        try:
            if hasattr(mod, 'main') and callable(getattr(mod, 'main')):
                # Provide deterministic seed via env-free arg if supported
                try:
                    mod.main()  # type: ignore
                except TypeError:
                    # main() with no args only
                    mod.main()  # type: ignore
                invoked.append(name)
        except Exception:
            # Keep going; this harness should be resilient
            pass

    # Build evolution payload (can be extended to include artifacts)
    payload: Dict[str, Any] = {
        'task': 'recursive_evolution',
        'head': head,
        'seed': seed,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'available_modules': available,
        'invoked': invoked,
        'version': 1,
    }

    # Append as an epoch to the chain
    chain = append_block(chain, payload, difficulty_bits)
    save_chain(chain, chain_path)

    new_head = latest_hash(chain)
    print("Epoch appended. New head:", new_head)

    # Export head as QR if possible
    export_obj = {"head": new_head, "difficulty": difficulty_bits}
    if HAVE_QR:
        img = qrcode.make(json.dumps(export_obj))  # type: ignore
        out = 'epoch_head_qr.png'
        img.save(out)
        print("Saved QR:", out)
    else:
        print("QR not available; head JSON:\n" + json.dumps(export_obj))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Epochal recursive evolution harness (duplicate)')
    ap.add_argument('-p', '--path', default=DEFAULT_CHAIN_PATH, help='Chain path (default: .uqcb_chain.json)')
    ap.add_argument('-d', '--difficulty', type=int, default=12, help='Difficulty bits (default: 12)')
    args = ap.parse_args()
    run_epoch(args.path, args.difficulty)
