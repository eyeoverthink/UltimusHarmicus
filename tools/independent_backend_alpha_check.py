#!/usr/bin/env python3
"""
Independent Backend Alpha Check (non-core):
- Recomputes alpha using Decimal high-precision arithmetic
- Compares with float path and CODATA 2018
- Persists JSON and optional QR
"""
import json
import time
import sys
from decimal import Decimal, getcontext
from datetime import datetime, timezone
from pathlib import Path

try:
    import qrcode  # optional
except Exception:
    qrcode = None

# Ensure project root importable
THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = THIS_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scientific_validation_suite import PHI, OMEGA, XI, LAMBDA, ZETA, ALPHA_CODATA

getcontext().prec = 80

OUT_JSON = Path(f"independent_backend_alpha_check_{int(time.time())}.json")
OUT_QR = Path("qr_independent_backend_alpha_check.png")


def alpha_decimal():
    phi = Decimal(str(PHI))
    omega = Decimal(str(OMEGA))
    xi = Decimal(str(XI))
    lamb = Decimal(str(LAMBDA))
    zeta = Decimal(str(ZETA))
    denom = (phi ** 4) * (omega ** 3) * (xi ** 3) * lamb * (zeta ** 3)
    return Decimal(1) / denom


def main():
    t0 = time.perf_counter()
    a_dec = alpha_decimal()
    t1 = time.perf_counter()

    # Float path
    denom_f = (PHI ** 4) * (OMEGA ** 3) * (XI ** 3) * LAMBDA * (ZETA ** 3)
    a_f = 1.0 / denom_f

    codata = Decimal(str(ALPHA_CODATA))
    rel_err_dec = abs(a_dec - codata) / codata
    rel_err_float = abs(Decimal(str(a_f)) - codata) / codata

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "timing_seconds": round(t1 - t0, 6),
        "alpha_decimal": float(a_dec),
        "alpha_float": a_f,
        "alpha_codata_2018": float(codata),
        "relative_error_decimal": float(rel_err_dec),
        "relative_error_float": float(rel_err_float),
        "agree_decimal_vs_float": float(abs(a_dec - Decimal(str(a_f)))) < 1e-15,
        "threshold": 1e-5,
        "pass_decimal": float(rel_err_dec) < 1e-5,
        "pass_float": float(rel_err_float) < 1e-5,
    }

    OUT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    if qrcode is not None:
        payload = f"independent_backend|{OUT_JSON.name}"
        qrcode.make(payload).save(OUT_QR)

    print("Independent Backend Check Complete:")
    print(f"- Decimal rel. error: {result['relative_error_decimal']:.9e}")
    print(f"- Float   rel. error: {result['relative_error_float']:.9e}")
    print(f"- Results: {OUT_JSON}")
    if OUT_QR.exists():
        print(f"- QR: {OUT_QR}")


if __name__ == "__main__":
    main()
