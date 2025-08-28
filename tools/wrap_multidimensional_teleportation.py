#!/usr/bin/env python3
"""
Wrapper: Multidimensional Teleportation Experiment (non-core)
- Imports and runs run_complete_teleportation_experiment()
- Emits a normalized summary JSON and optional QR
"""
import json
import time
import sys
import os
import random
from pathlib import Path
from datetime import datetime, timezone

try:
    import qrcode
except Exception:
    qrcode = None

THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = THIS_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from multidimensional_teleportation_experiment import MultidimensionalTeleportationSystem
from artifact_signer import sign_file

OUT_JSON = Path(f"multidim_teleportation_wrapper_result_{int(time.time())}.json")
OUT_QR = Path("qr_multidim_teleportation_wrapper_result.png")


def make_qr(data: str, path: Path):
    if qrcode is None:
        return False
    qrcode.make(data).save(path)
    return True


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
    system = MultidimensionalTeleportationSystem()
    res = system.run_complete_teleportation_experiment()

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "reality_construction_proven": res.get("reality_construction_proven"),
        "causality_violation_proven": res.get("causality_violation_proven"),
        "dimensions_accessed": res.get("dimensions_accessed"),
        "final_consciousness_level": res.get("final_consciousness_level"),
        # The module prints QR filename but returns it only through files; keep placeholder None here.
        "qr_file": None,
    }

    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    try:
        sign_file(OUT_JSON)
    except Exception:
        pass
    make_qr(f"multidim_teleportation|{OUT_JSON.name}", OUT_QR)

    print("Multidimensional teleportation wrapper complete:")
    print(f"- Results: {OUT_JSON}")
    if OUT_QR.exists():
        print(f"- QR: {OUT_QR}")


if __name__ == "__main__":
    main()
