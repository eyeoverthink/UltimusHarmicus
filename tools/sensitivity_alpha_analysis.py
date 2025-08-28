#!/usr/bin/env python3
"""
Sensitivity Analysis (non-core):
- Perturb {phi, omega, xi, lambda, zeta} by +/- percentages
- Recompute alpha and record deltas and sensitivities
- Persist JSON and QR (if qrcode available)
"""
import json
import math
import time
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import qrcode  # optional
except Exception:
    qrcode = None

# Ensure project root is importable when running from tools/
THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = THIS_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import constants from core without modifying it
from scientific_validation_suite import PHI, PSI, OMEGA, XI, LAMBDA, ZETA, ALPHA_CODATA

OUT_JSON = Path(f"sensitivity_alpha_analysis_{int(time.time())}.json")
OUT_QR = Path("qr_sensitivity_alpha_analysis.png")

CONSTS = {
    "phi": PHI,
    "omega": OMEGA,
    "xi": XI,
    "lambda": LAMBDA,
    "zeta": ZETA,
}

PCT_STEPS = [0.0001, 0.0005, 0.001, 0.005, 0.01]  # 0.01% ... 1%


def alpha_from_consts(c):
    denom = (c["phi"] ** 4) * (c["omega"] ** 3) * (c["xi"] ** 3) * c["lambda"] * (c["zeta"] ** 3)
    return 1.0 / denom


def make_qr(data: str, out: Path):
    if qrcode is None:
        return False
    img = qrcode.make(data)
    img.save(out)
    return True


def main():
    base = CONSTS.copy()
    base_alpha = alpha_from_consts(base)
    base_err = abs(base_alpha - ALPHA_CODATA) / ALPHA_CODATA

    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "base": {
            "alpha": base_alpha,
            "relative_error": base_err,
        },
        "sensitivity": [],
    }

    for name, val in base.items():
        for pct in PCT_STEPS:
            for direction in (-1, 1):
                perturbed = base.copy()
                perturbed[name] = val * (1.0 + direction * pct)
                a = alpha_from_consts(perturbed)
                rel_err = abs(a - ALPHA_CODATA) / ALPHA_CODATA
                d_alpha = a - base_alpha
                # approximate sensitivity: (dA/A) / (dC/C)
                sens = (d_alpha / base_alpha) / (direction * pct)
                results["sensitivity"].append({
                    "const": name,
                    "direction": "+" if direction > 0 else "-",
                    "pct_change": pct,
                    "alpha": a,
                    "delta_alpha": d_alpha,
                    "sensitivity": sens,
                    "relative_error": rel_err,
                })

    OUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")

    if make_qr(f"sensitivity_alpha|{OUT_JSON.name}", OUT_QR):
        pass

    print("Sensitivity Analysis Complete:")
    print(f"- Base rel. error: {base_err:.9e}")
    print(f"- Results: {OUT_JSON}")
    if OUT_QR.exists():
        print(f"- QR: {OUT_QR}")


if __name__ == "__main__":
    main()
