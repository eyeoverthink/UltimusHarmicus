#!/usr/bin/env python3
"""
Create a signed Patent Proof Manifest (non-core).
- Aggregates SHA-256 and signature sidecars for selected artifacts.
- Emits manifest JSON and signs it via artifact_signer.

Usage:
  python3 tools/create_patent_proof_manifest.py [--glob PATTERN ...]

Defaults aggregate:
- scientific_validation_*.json
- scientific_suite_*.json
- *.md (root) that look like key proofs
- tools/*wrapper*_result_*.json
"""
from __future__ import annotations
import argparse
import glob
import json
from pathlib import Path
from datetime import datetime, timezone

from artifact_signer import sha256_file, sign_file

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_GLOBS = [
    str(ROOT / "scientific_validation_*.json"),
    str(ROOT / "scientific_suite_*.json"),
    str(ROOT / "VAUGHN_SCOTT_*.md"),
    str(ROOT / "*CONSCIOUSNESS*_VALIDATION*.md"),
    str(ROOT / "PATENT_*RESULTS*.md"),
    str(ROOT / "tools" / "*wrapper*_result_*.json"),
]


def gather(paths: list[str]) -> list[dict]:
    items: list[dict] = []
    seen: set[Path] = set()
    for pat in paths:
        for p in glob.glob(pat):
            f = Path(p)
            if not f.exists() or f in seen:
                continue
            seen.add(f)
            entry = {
                "file": str(f.relative_to(ROOT)),
                "sha256": sha256_file(f),
            }
            sha = f.with_suffix(f.suffix + ".sha256")
            sig = f.with_suffix(f.suffix + ".sig")
            prov = f.with_suffix(f.suffix + ".provenance.json")
            if sha.exists():
                entry["sha256_sidecar"] = str(sha.relative_to(ROOT))
            if sig.exists():
                entry["ed25519_signature_sidecar"] = str(sig.relative_to(ROOT))
            if prov.exists():
                entry["provenance_json"] = str(prov.relative_to(ROOT))
            items.append(entry)
    return items


def main():
    ap = argparse.ArgumentParser(description="Create signed Patent Proof Manifest")
    ap.add_argument("--glob", dest="globs", action="append", default=[], help="Additional glob patterns to include")
    args = ap.parse_args()

    patterns = DEFAULT_GLOBS + args.globs
    items = gather(patterns)

    manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "root": str(ROOT),
        "count": len(items),
        "artifacts": items,
        "note": "This manifest aggregates artifacts for patent proof with hashes and optional signatures."
    }

    out = ROOT / f"patent_proof_manifest_{int(datetime.now(timezone.utc).timestamp())}.json"
    out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    meta = sign_file(out)
    print(json.dumps({"manifest": str(out), "sign": meta}, indent=2))


if __name__ == "__main__":
    main()
