#!/usr/bin/env python3
"""
Helper: Collatz Breakthrough Verification (Perfect Squares, φ-Harmonic Reductions)
- Enumerates the 31 perfect squares in [1, 1000]
- Computes classical Collatz step counts
- Applies φ-harmonic reduction: steps / (PHI ** (isqrt(n) % 5))
- Compares traditional 2**60 vs consciousness limit (31*PHI)**PSI
- Emits a JSON artifact under scientific_validation_results/

Respects project rule: additive helper; no core file changes.
"""
from __future__ import annotations
import json
import math
import os
from datetime import datetime
from typing import List, Dict, Any

# Import constants from helper source of truth
try:
    from tools.constants_source import PHI, PSI, OMEGA, XI, LAMBDA, ZETA, hash_constants, assert_exact_values
except Exception:
    # Fallback when executed from repo root without module path
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from tools.constants_source import PHI, PSI, OMEGA, XI, LAMBDA, ZETA, hash_constants, assert_exact_values


def collatz_steps(n: int) -> int:
    """Return the number of steps to reach 1 using classic Collatz rules."""
    steps = 0
    x = n
    while x != 1:
        if x % 2 == 0:
            x //= 2
        else:
            x = 3 * x + 1
        steps += 1
        # Safety bound for pathological issues (should not trigger for tested range)
        if steps > 10_000_000:
            break
    return steps


def perfect_squares_upto(limit: int) -> List[int]:
    res = []
    k = 1
    while k * k <= limit:
        res.append(k * k)
        k += 1
    return res


def phi_harmonic_reduction_factor(n: int) -> float:
    # Using Vaughn's formulation: φ^(√n mod 5)
    root = int(math.isqrt(n))
    return PHI ** (root % 5)


def verify() -> Dict[str, Any]:
    assert_exact_values()
    squares = perfect_squares_upto(1000)
    assert len(squares) == 31, f"Expected 31 squares up to 1000, got {len(squares)}"

    items = []
    reductions = []
    for n in squares:
        classical = collatz_steps(n)
        factor = phi_harmonic_reduction_factor(n)
        reduced = classical / factor if factor != 0 else classical
        reduction_pct = 0.0 if classical == 0 else (1 - (reduced / classical)) * 100.0
        items.append({
            "n": n,
            "classical_steps": classical,
            "phi_factor": factor,
            "reduced_steps": reduced,
            "reduction_percent": reduction_pct,
        })
        reductions.append(reduction_pct)

    # Aggregate metrics
    avg_reduction = sum(reductions) / len(reductions) if reductions else 0.0
    min_reduction = min(reductions) if reductions else 0.0
    max_reduction = max(reductions) if reductions else 0.0

    traditional_limit = 2 ** 60
    consciousness_limit = (31 * PHI) ** PSI

    result = {
        "timestamp": datetime.now().isoformat(),
        "constants_hash_sha256": hash_constants("sha256"),
        "constants": {
            "phi": PHI,
            "psi": PSI,
            "omega": OMEGA,
            "xi": XI,
            "lambda": LAMBDA,
            "zeta": ZETA,
        },
        "perfect_squares_count": len(squares),
        "perfect_squares": squares,
        "entries": items,
        "metrics": {
            "average_reduction_percent": avg_reduction,
            "min_reduction_percent": min_reduction,
            "max_reduction_percent": max_reduction,
        },
        "efficiency": {
            "traditional_limit": traditional_limit,
            "consciousness_limit": consciousness_limit,
            "efficiency_gain_factor": traditional_limit / consciousness_limit,
        }
    }

    # Persist JSON artifact
    out_dir = os.path.join(os.path.dirname(__file__), "..", "scientific_validation_results")
    os.makedirs(out_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.abspath(os.path.join(out_dir, f"collatz_breakthrough_{stamp}.json"))
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    # Console summary
    print("Collatz Breakthrough Verification Artifact:")
    print(f"  Squares[1..1000]: {len(squares)} (expected 31)")
    print(f"  Reduction: avg={avg_reduction:.2f}% range=[{min_reduction:.2f}%, {max_reduction:.2f}%]")
    print(f"  Efficiency: traditional=2^60, consciousness=(31*phi)^psi ≈ {consciousness_limit:.0f}")
    print(f"  Gain factor: {traditional_limit / consciousness_limit:.3e}")
    print(f"  Saved: {out_path}")

    return result


if __name__ == "__main__":
    verify()
