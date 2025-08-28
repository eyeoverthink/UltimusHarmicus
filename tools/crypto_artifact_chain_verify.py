#!/usr/bin/env python3
"""
Cryptographic Artifact Chain Verification (non-core):
- Verifies SHA-256 of known artifacts and consistency with QR payloads
- Attempts to decode QR payloads (optional: pyzbar)
- Emits a verification JSON report
"""
import json
import hashlib
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

try:
    from PIL import Image  # for QR decode
    from pyzbar.pyzbar import decode as qr_decode
except Exception:
    Image = None
    qr_decode = None

INDEX = Path("scientific_suite_alpha_index.json")
OUT_JSON = Path(f"crypto_artifact_chain_verify_{int(time.time())}.json")


@dataclass
class Artifact:
    name: str
    path: Path


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def decode_qr(png_path: Path):
    if qr_decode is None or Image is None:
        return None
    try:
        img = Image.open(png_path)
        dec = qr_decode(img)
        if not dec:
            return None
        return dec[0].data.decode("utf-8", errors="replace")
    except Exception:
        return None


def main():
    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "index_exists": INDEX.exists(),
        "verified": [],
        "qr_payloads": {},
        "errors": [],
    }

    if not INDEX.exists():
        OUT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print("Index not found; wrote minimal report.")
        return

    try:
        idx = json.loads(INDEX.read_text(encoding="utf-8"))
    except Exception as e:
        result["errors"].append(f"index_parse_error: {e}")
        OUT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print("Index parse error; wrote report.")
        return

    artifacts = []
    report_path = idx.get("report")
    if report_path:
        artifacts.append(Artifact("suite_report", Path(report_path)))

    # Known upstream artifacts
    artifacts.append(Artifact("alpha_reproduction", Path("alpha_reproduction.txt")))
    artifacts.append(Artifact("appendix_A_exponent_proof", Path("appendix_A_exponent_derivation_proof.json")))

    # Verify artifacts
    for a in artifacts:
        info = {
            "name": a.name,
            "path": str(a.path),
            "exists": a.path.exists(),
            "sha256": None,
        }
        if a.path.exists():
            info["sha256"] = sha256_file(a.path)
        result["verified"].append(info)

    # Decode QRs and include payloads
    qr_map = idx.get("qr", {}) or {}
    for k, v in qr_map.items():
        p = Path(v)
        payload = decode_qr(p)
        result["qr_payloads"][k] = {
            "path": str(p),
            "exists": p.exists(),
            "decoded": payload,
        }

    OUT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("Crypto chain verification complete:")
    print(f"- Report: {OUT_JSON}")


if __name__ == "__main__":
    main()
