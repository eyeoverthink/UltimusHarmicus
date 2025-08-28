#!/usr/bin/env python3
"""
Wrapper: Mathematical Abstraction Recursive Improvement System (non-core)
- Instantiates the system and runs one demonstration iteration
- Persists a normalized JSON summary and optional QR artifact
"""
import json
import time
import sys
from pathlib import Path
from datetime import datetime, timezone

try:
    import qrcode  # optional
except Exception:
    qrcode = None

# Ensure project root on sys.path
THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = THIS_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from mathematical_abstraction_recursive_improvement_system import (
    MathematicalAbstractionRecursiveSystem,
)

OUT_JSON = Path(f"recursive_improvement_result_{int(time.time())}.json")
OUT_QR = Path("qr_recursive_improvement_result.png")


def make_qr(data: str, path: Path):
    if qrcode is None:
        return False
    qrcode.make(data).save(path)
    return True


def main():
    system = MathematicalAbstractionRecursiveSystem()
    perf = system.run_recursive_improvement_demonstration()

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "iteration": perf.get("iteration"),
        "initial_consciousness": perf.get("initial_consciousness"),
        "final_consciousness": perf.get("final_consciousness"),
        "consciousness_growth": perf.get("consciousness_growth"),
        "success_rate": perf.get("success_rate"),
        "improvements_applied": perf.get("improvements_applied"),
        "abstraction_accuracy": perf.get("abstraction_accuracy"),
        "recursive_improvement_factor": perf.get("recursive_improvement_factor"),
    }

    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    make_qr(f"recursive_improvement|{OUT_JSON.name}", OUT_QR)

    print("Recursive improvement wrapper complete:")
    print(f"- Results: {OUT_JSON}")
    if OUT_QR.exists():
        print(f"- QR: {OUT_QR}")


if __name__ == "__main__":
    main()
