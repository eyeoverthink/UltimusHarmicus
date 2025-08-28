#!/usr/bin/env python3
"""
Monte Carlo Robustness (non-core):
- Randomly perturb {phi, omega, xi, lambda, zeta} within small tolerances
- Compute alpha and measure validation pass rate vs CODATA threshold
- Persist JSON with distribution stats and QR (if available)
"""
import json
import math
import random
import statistics as stats
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

from scientific_validation_suite import PHI, OMEGA, XI, LAMBDA, ZETA, ALPHA_CODATA

N_SAMPLES = 2000
REL_TOL = 1e-5  # success threshold (same as suite)
# Relative std-dev per constant (tunable):
REL_SIGMA = {
    "phi": 2e-4,
    "omega": 2e-4,
    "xi": 2e-4,
    "lambda": 2e-4,
    "zeta": 2e-4,
}

OUT_JSON = Path(f"monte_carlo_alpha_robustness_{int(time.time())}.json")
OUT_QR = Path("qr_monte_carlo_alpha_robustness.png")

BASE = {
    "phi": PHI,
    "omega": OMEGA,
    "xi": XI,
    "lambda": LAMBDA,
    "zeta": ZETA,
}


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
    errs = []
    passes = 0
    samples = []

    for _ in range(N_SAMPLES):
        c = {}
        for k, v in BASE.items():
            sigma = REL_SIGMA[k]
            # log-normal-ish multiplicative noise via exp(N(0, sigma)) approximation
            perturb = math.exp(random.gauss(0.0, sigma))
            c[k] = v * perturb
        a = alpha_from_consts(c)
        rel_err = abs(a - ALPHA_CODATA) / ALPHA_CODATA
        errs.append(rel_err)
        samples.append(a)
        if rel_err < REL_TOL:
            passes += 1

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "n_samples": N_SAMPLES,
        "threshold": REL_TOL,
        "pass_count": passes,
        "pass_rate": passes / N_SAMPLES,
        "alpha_stats": {
            "mean": stats.fmean(samples),
            "stdev": stats.pstdev(samples),
            "min": min(samples),
            "max": max(samples),
        },
        "error_stats": {
            "mean": stats.fmean(errs),
            "stdev": stats.pstdev(errs),
            "min": min(errs),
            "max": max(errs),
        },
    }

    OUT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    make_qr(f"monte_carlo_alpha|{OUT_JSON.name}", OUT_QR)

    print("Monte Carlo Robustness Complete:")
    print(f"- Pass rate: {result['pass_rate']:.4f} ({passes}/{N_SAMPLES})")
    print(f"- Results: {OUT_JSON}")
    if OUT_QR.exists():
        print(f"- QR: {OUT_QR}")


if __name__ == "__main__":
    main()
