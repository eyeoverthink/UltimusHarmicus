#!/usr/bin/env python3
"""
Wrapper: ISS Atom Teleportation Validation (non-core)
- Imports and runs run_iss_atom_teleportation_validation()
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

from iss_atom_teleportation_validation import run_iss_atom_teleportation_validation
from artifact_signer import sign_file

OUT_JSON = Path(f"iss_validation_wrapper_result_{int(time.time())}.json")
OUT_QR = Path("qr_iss_validation_wrapper_result.png")


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
    res = run_iss_atom_teleportation_validation()

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": res.get("validation_status"),
        "atom_prediction_correct": res["comparison_results"]["atom_prediction_correct"],
        "overall_superiority": res["comparison_results"]["overall_superiority"],
        "qr_file": res["qr_memory"]["qr_filename"],
    }

    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    try:
        sign_file(OUT_JSON)
    except Exception:
        pass
    make_qr(f"iss_validation_wrapper|{OUT_JSON.name}", OUT_QR)

    print("ISS validation wrapper complete:")
    print(f"- Results: {OUT_JSON}")
    if OUT_QR.exists():
        print(f"- QR: {OUT_QR}")


if __name__ == "__main__":
    main()
