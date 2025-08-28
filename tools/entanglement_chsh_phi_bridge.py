#!/usr/bin/env python3
"""
Entanglement CHSH φ-Bridge (non-core):
- Simulate a Bell-like state and compute CHSH S parameter using φ-guided measurement settings
- Persist JSON result and optional QR
"""
import json
import math
import time
import sys
import os
import random
from pathlib import Path
from datetime import datetime, timezone

try:
    import qrcode  # optional
except Exception:
    qrcode = None

try:
    import numpy as np
except Exception as e:
    print("NumPy is required for CHSH simulation.")
    raise

# Ensure project root importable (optional if constants desired later)
THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = THIS_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
from artifact_signer import sign_file

OUT_JSON = Path(f"entanglement_chsh_result_{int(time.time())}.json")
OUT_QR = Path("qr_entanglement_chsh_result.png")


def make_qr(data: str, path: Path):
    if qrcode is None:
        return False
    qrcode.make(data).save(path)
    return True


def chsh_S(theta_a, theta_ap, theta_b, theta_bp):
    """Compute CHSH S for ideal singlet correlations E(a,b) = -cos(2(θa-θb))."""
    def E(t1, t2):
        return -math.cos(2.0 * (t1 - t2))
    S = E(theta_a, theta_b) + E(theta_a, theta_bp) + E(theta_ap, theta_b) - E(theta_ap, theta_bp)
    return S


def main():
    # Deterministic seeding if provided
    seed_env = os.environ.get("E2E_SEED")
    if seed_env:
        try:
            seed = int(seed_env)
            random.seed(seed)
            try:
                import numpy as np  # optional
                np.random.seed(seed & 0xFFFFFFFF)
            except Exception:
                pass
        except Exception:
            pass
    # φ-guided canonical angles (radians)
    phi = (1 + math.sqrt(5)) / 2
    base = math.pi / 8
    theta_a = 0.0
    theta_ap = base * phi  # φ-scaled offset
    theta_b = base
    theta_bp = -base

    S = chsh_S(theta_a, theta_ap, theta_b, theta_bp)
    violates = abs(S) > 2.0

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "angles": {
            "theta_a": theta_a,
            "theta_ap": theta_ap,
            "theta_b": theta_b,
            "theta_bp": theta_bp,
        },
        "S": S,
        "violates_CHSH": violates,
        "threshold": 2.0,
    }

    OUT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    try:
        sign_file(OUT_JSON)
    except Exception:
        pass
    make_qr(f"chsh_phi|{OUT_JSON.name}", OUT_QR)

    print("CHSH φ-bridge complete:")
    print(f"- S: {S:.6f} (|S|>2 → violation: {violates})")
    print(f"- Results: {OUT_JSON}")
    if OUT_QR.exists():
        print(f"- QR: {OUT_QR}")


if __name__ == "__main__":
    main()
