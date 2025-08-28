#!/usr/bin/env python3
"""
Non-core artifact signer utility.
- Signs files with Ed25519 if 'cryptography' is available and a private key exists.
- Always writes a SHA-256 checksum sidecar.
- Emits a provenance JSON with metadata.

Files created per target <file>:
- <file>.sha256
- <file>.sig            (if Ed25519 available + key found)
- <file>.provenance.json

Keys (optional):
- tools/ed25519_private_key.pem
- tools/ed25519_public_key.pem
"""
from __future__ import annotations
import base64
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

# Optional Ed25519 via cryptography
try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
    from cryptography.hazmat.primitives import serialization
except Exception:
    Ed25519PrivateKey = None
    Ed25519PublicKey = None
    serialization = None

TOOLS_DIR = Path(__file__).resolve().parent
PRIV_KEY = TOOLS_DIR / "ed25519_private_key.pem"
PUB_KEY = TOOLS_DIR / "ed25519_public_key.pem"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_private_key() -> Ed25519PrivateKey | None:
    if Ed25519PrivateKey is None or serialization is None:
        return None
    if not PRIV_KEY.exists():
        return None
    data = PRIV_KEY.read_bytes()
    return serialization.load_pem_private_key(data, password=None)


def _load_public_key() -> Ed25519PublicKey | None:
    if Ed25519PublicKey is None or serialization is None:
        return None
    if not PUB_KEY.exists():
        return None
    data = PUB_KEY.read_bytes()
    return serialization.load_pem_public_key(data)


def sign_file(target: str | Path) -> dict:
    """Sign target file. Returns dict with signature metadata."""
    target = Path(target)
    sha = sha256_file(target)
    (target.with_suffix(target.suffix + ".sha256")).write_text(sha + "\n", encoding="utf-8")

    signature_b64 = None
    pub_pem = None

    pk = _load_private_key()
    if pk is not None:
        sig = pk.sign(target.read_bytes())
        signature_b64 = base64.b64encode(sig).decode("ascii")
        # try to load public key pem for recording
        try:
            if PUB_KEY.exists():
                pub_pem = PUB_KEY.read_text(encoding="utf-8")
        except Exception:
            pub_pem = None
        (target.with_suffix(target.suffix + ".sig")).write_text(signature_b64 + "\n", encoding="utf-8")

    prov = {
        "file": str(target),
        "sha256": sha,
        "ed25519_signature_b64": signature_b64,
        "ed25519_public_key_pem": pub_pem,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": "artifact_signer.py",
    }
    (target.with_suffix(target.suffix + ".provenance.json")).write_text(json.dumps(prov, indent=2), encoding="utf-8")
    return prov


def verify_file(target: str | Path) -> dict:
    """Verify SHA-256 and Ed25519 signature (if present)."""
    target = Path(target)
    result = {"file": str(target), "sha256_ok": False, "signature_ok": None}

    # verify sha256
    sha_path = target.with_suffix(target.suffix + ".sha256")
    if sha_path.exists():
        recorded = sha_path.read_text(encoding="utf-8").strip()
        result["sha256_ok"] = recorded == sha256_file(target)

    # verify signature if possible
    sig_path = target.with_suffix(target.suffix + ".sig")
    pub = _load_public_key()
    if sig_path.exists() and pub is not None:
        try:
            sig = base64.b64decode(sig_path.read_text(encoding="utf-8").strip())
            pub.verify(sig, target.read_bytes())
            result["signature_ok"] = True
        except Exception:
            result["signature_ok"] = False
    return result


def public_key_available() -> bool:
    """Return True if Ed25519 public key is available and loadable."""
    return _load_public_key() is not None


def public_key_fingerprint() -> str | None:
    """Return SHA-256 fingerprint (hex) of the public key in SubjectPublicKeyInfo format, if available."""
    pub = _load_public_key()
    if pub is None or serialization is None:
        return None
    try:
        der = pub.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return hashlib.sha256(der).hexdigest()
    except Exception:
        return None


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Sign or verify artifacts")
    ap.add_argument("mode", choices=["sign", "verify"], help="operation")
    ap.add_argument("paths", nargs="+", help="file paths")
    args = ap.parse_args()

    if args.mode == "sign":
        for p in args.paths:
            meta = sign_file(p)
            print(json.dumps(meta, indent=2))
    else:
        for p in args.paths:
            meta = verify_file(p)
            print(json.dumps(meta, indent=2))
