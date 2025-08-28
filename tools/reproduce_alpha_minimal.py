#!/usr/bin/env python3
import math
from datetime import datetime, timezone

ALPHA_CODATA = 7.2973525693e-3

PHI = (1 + math.sqrt(5)) / 2
OMEGA = 0.5671432904097838730
XI = math.e
LAMBDA = math.pi
ZETA = 1.2020569031595942854

denominator = (PHI**4) * (OMEGA**3) * (XI**3) * LAMBDA * (ZETA**3)
alpha_derived = 1.0 / denominator
relative_error = abs(alpha_derived - ALPHA_CODATA) / ALPHA_CODATA

with open("alpha_reproduction.txt", "w", encoding="utf-8") as f:
    f.write(f"timestamp_utc: {datetime.now(timezone.utc).isoformat()}\n")
    f.write(f"alpha_official: {ALPHA_CODATA:.12e}\n")
    f.write(f"alpha_derived:  {alpha_derived:.12e}\n")
    f.write(f"relative_error: {relative_error:.6e}\n")
    f.write("threshold_ok: {}\n".format(relative_error < 1e-5))
