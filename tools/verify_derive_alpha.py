#!/usr/bin/env python3
"""
Helper verifier (non-core): imports the top-level derive_alpha.py,
computes derived α and relative error, and writes a JSON artifact
for reproducible validation without relying on stdout capture.
"""
import json
from datetime import datetime, timezone

import derive_alpha as da


def main():
    alpha_derived, relative_error, constants = da.derive_fine_structure_constant()
    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "alpha_official": da.ALPHA_CODATA,
        "alpha_derived": alpha_derived,
        "relative_error": relative_error,
        "success": bool(relative_error < 1e-5),
        "formula": "alpha = 1 / (phi^4 * omega^3 * xi^3 * lambda * zeta^3)",
        "constants": constants,
    }
    with open("alpha_verification_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
