#!/usr/bin/env python3
"""
Offline verifier for artifact integrity.
- Verifies SHA-256 and Ed25519 signatures (if public key is available) for given files.
- If no files are passed, auto-discovers *.json in project root and tools outputs.
"""
from __future__ import annotations
import argparse
import glob
from pathlib import Path
import json

from artifact_signer import verify_file, public_key_available, public_key_fingerprint

ROOT = Path(__file__).resolve().parent.parent


def discover_targets() -> list[Path]:
    patterns = [
        str(ROOT / "*.json"),
        str(ROOT / "*.md"),  # allow verifying markdown proofs too
        str(ROOT / "tools" / "*.json"),
    ]
    files = []
    for p in patterns:
        files.extend([Path(x) for x in glob.glob(p)])
    # keep only those with sidecars
    return [f for f in files if (f.with_suffix(f.suffix + ".sha256")).exists()]


def main():
    ap = argparse.ArgumentParser(description="Offline artifact verifier")
    ap.add_argument("paths", nargs="*", help="Files to verify. If empty, auto-discover.")
    ap.add_argument("--verbose", action="store_true", help="Print per-file PASS/FAIL and key info")
    ap.add_argument("--require-signature", action="store_true", help="Fail if signature is missing or invalid")
    args = ap.parse_args()

    targets = [Path(p) for p in args.paths] if args.paths else discover_targets()
    results = []
    passed = 0
    failed = 0
    for t in targets:
        try:
            r = verify_file(t)
            results.append(r)
            ok = bool(r.get("sha256_ok")) and (
                (r.get("signature_ok") is True) or (not args.require_signature and r.get("signature_ok") in (True, None))
            )
            if args.verbose:
                status = "PASS" if ok else "FAIL"
                sig_state = r.get("signature_ok")
                sig_msg = (
                    "sig:OK" if sig_state is True else ("sig:MISSING" if sig_state is None else "sig:BAD")
                )
                print(f"[{status}] {t.name} | sha256:{'OK' if r.get('sha256_ok') else 'BAD'} | {sig_msg}")
            passed += 1 if ok else 0
            failed += 0 if ok else 1
        except Exception as e:
            err = {"file": str(t), "error": str(e)}
            results.append(err)
            if args.verbose:
                print(f"[ERROR] {t.name} | {e}")
            failed += 1

    summary = {
        "count": len(targets),
        "passed": passed,
        "failed": failed,
        "require_signature": args.require_signature,
        "public_key_available": public_key_available(),
        "public_key_fingerprint_sha256": public_key_fingerprint(),
        "results": results,
    }

    if not args.verbose:
        print(json.dumps(summary, indent=2))
    else:
        # Verbose footer summary
        print("\nSummary:")
        print(f"- Total: {len(targets)} | Passed: {passed} | Failed: {failed}")
        pk_avail = public_key_available()
        print(f"- Ed25519 public key available: {pk_avail}")
        if pk_avail:
            print(f"- Public key fingerprint (SHA-256): {public_key_fingerprint()}")
        print(f"- Require signature: {args.require_signature}")


if __name__ == "__main__":
    main()
