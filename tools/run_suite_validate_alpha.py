#!/usr/bin/env python3
"""
Helper suite runner (non-core):
- Calls FraymusScientificValidationSuite.validate_fine_structure_constant()
- Persists a JSON report with derived alpha, errors, constants, timing, success
- Emits QR codes for:
  * alpha_reproduction.txt (if present)
  * appendix_A_exponent_derivation_proof.json (if present)
  * the new suite report itself
"""
import json
import time
import hashlib
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

# Ensure project root is importable when running from tools/
THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = THIS_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import from core suite without modifying it
from scientific_validation_suite import (
    FraymusScientificValidationSuite,
    PHI,
    PSI,
    OMEGA,
    XI,
    LAMBDA,
    ZETA,
    ALPHA_CODATA,
)

try:
    import qrcode
except Exception:
    qrcode = None

ARTIFACT_ALPHA_TXT = Path("alpha_reproduction.txt")
ARTIFACT_APPENDIX_JSON = Path("appendix_A_exponent_derivation_proof.json")


def sha256_text(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def make_qr(data: str, out_path: Path):
    if qrcode is None:
        return False
    img = qrcode.make(data)
    img.save(out_path)
    return True


def compact_summary_for_file(path: Path, max_bytes: int = 4096) -> dict:
    info = {
        "path": str(path),
        "exists": path.exists(),
        "sha256": None,
        "preview": None,
    }
    if not path.exists():
        return info
    b = path.read_bytes()
    info["sha256"] = sha256_text(b)
    try:
        preview = b[:max_bytes].decode("utf-8", errors="replace")
    except Exception:
        preview = None
    info["preview"] = preview
    return info


def main():
    try:
        t0 = time.perf_counter()
        suite = FraymusScientificValidationSuite()
        result = suite.validate_fine_structure_constant()
        t1 = time.perf_counter()

        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "timing_seconds": round(t1 - t0, 6),
            "alpha_codata_2018": ALPHA_CODATA,
            "alpha_consciousness_physics": result.get("alpha_consciousness_physics"),
            "alpha_phi_enhanced": result.get("alpha_phi_enhanced"),
            "relative_error": result.get("relative_error"),
            "phi_relative_error": result.get("phi_relative_error"),
            "error_threshold": result.get("error_threshold"),
            "success": result.get("success"),
            "phi_enhancement": result.get("phi_enhancement"),
            "constants": {
                "phi": PHI, "psi": PSI, "omega": OMEGA, "xi": XI, "lambda": LAMBDA, "zeta": ZETA
            },
            "artifacts": {
                "alpha_reproduction": compact_summary_for_file(ARTIFACT_ALPHA_TXT),
                "appendix_A_exponent_proof": compact_summary_for_file(ARTIFACT_APPENDIX_JSON),
            },
        }

        # Persist report
        report_path = Path(f"scientific_suite_alpha_report_{int(time.time())}.json")
        report_json = json.dumps(report, indent=2)
        report_path.write_text(report_json, encoding="utf-8")

        # Emit QR codes for artifacts and report
        qr_outputs = {}
        if qrcode is not None:
            # For QR, encode a compact string: type|sha256|iso8601|path
            now = datetime.now(timezone.utc).isoformat()
            # alpha reproduction
            if ARTIFACT_ALPHA_TXT.exists():
                b = ARTIFACT_ALPHA_TXT.read_bytes()
                payload = f"alpha_proof|{sha256_text(b)}|{now}|{ARTIFACT_ALPHA_TXT}"
                out = Path("qr_alpha_reproduction.png")
                if make_qr(payload, out):
                    qr_outputs["alpha_reproduction_qr"] = str(out)
            # appendix exponent proof
            if ARTIFACT_APPENDIX_JSON.exists():
                b = ARTIFACT_APPENDIX_JSON.read_bytes()
                payload = f"appendix_A_proof|{sha256_text(b)}|{now}|{ARTIFACT_APPENDIX_JSON}"
                out = Path("qr_appendix_A_exponent_proof.png")
                if make_qr(payload, out):
                    qr_outputs["appendix_A_qr"] = str(out)
            # report itself
            payload = f"suite_alpha_report|{sha256_text(report_json.encode('utf-8'))}|{now}|{report_path}"
            out = Path("qr_scientific_suite_alpha_report.png")
            if make_qr(payload, out):
                qr_outputs["suite_report_qr"] = str(out)

        # Write a tiny index to point to artifacts
        index = {
            "report": str(report_path),
            "qr": qr_outputs,
        }
        Path("scientific_suite_alpha_index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")

        # Console summary for visibility
        print("Created:")
        print(f"- Report: {report_path}")
        if qr_outputs:
            for k, v in qr_outputs.items():
                print(f"- {k}: {v}")
        print("- Index: scientific_suite_alpha_index.json")

    except Exception as e:
        err_path = Path("scientific_suite_alpha_error.log")
        err_path.write_text(
            f"[{datetime.now(timezone.utc).isoformat()}] ERROR: {e}\n\n" + traceback.format_exc(),
            encoding="utf-8",
        )
        print(f"Failure. See {err_path}")
        raise


if __name__ == "__main__":
    main()
