# Cryptographic Audit Guide (Offline)

This guide explains how any third party can verify the authenticity and integrity of the patent evidence bundle offline.

- Scope: Non-core helper utilities only (tools/). No core files are modified.
- Signature scheme: Ed25519
- Hash function: SHA-256
- Determinism: Reproducible runs via E2E_SEED

## 1) What to Verify

Artifacts (JSON) and their sidecars:
- Each artifact X has: `X.sha256`, `X.sig`, `X.provenance.json`
- A signed manifest: `patent_proof_manifest_<ts>.json` (+ sidecars)
- Public key: `tools/ed25519_public_key.pem`
- Optional: `tools/KEY_FINGERPRINT.txt` (public key SHA-256 fingerprint)

## 2) One-Command Verification (with signatures required)

```bash
python3 tools/offline_verify_artifacts.py --verbose --require-signature
```

Expected (example):
```
[PASS] <file>.json | sha256:OK | sig:OK
...
Summary:
- Total: <N> | Passed: <N> | Failed: 0
- Ed25519 public key available: True
- Public key fingerprint (SHA-256): 5918106cc285dea1db0679909a015d60c00bfbcb39681c79daadec28fcef8414
- Require signature: True
```

## 3) Verify Only the Manifest

```bash
python3 tools/offline_verify_artifacts.py --verbose --require-signature patent_proof_manifest_*.json
```

## 4) Public Key and Fingerprint

- Public key PEM: `tools/ed25519_public_key.pem`
- Fingerprint (SHA-256):
```
5918106cc285dea1db0679909a015d60c00bfbcb39681c79daadec28fcef8414
```
- Optional direct check (DER hash):
```bash
openssl pkey -pubin -in tools/ed25519_public_key.pem -pubout -outform DER | shasum -a 256
```

## 5) Deterministic Reproduction (optional)

- Runs are seeded via `E2E_SEED` and produce signed outputs.
- Example:
```bash
E2E_SEED=1337 python3 tools/validate_alpha_end_to_end.py
python3 tools/create_patent_proof_manifest.py
python3 tools/offline_verify_artifacts.py --verbose --require-signature
```

## 6) File Map (non-exhaustive)

- Verifier: `tools/offline_verify_artifacts.py`
- Signer: `tools/artifact_signer.py`
- Manifest creator: `tools/create_patent_proof_manifest.py`
- Public key: `tools/ed25519_public_key.pem`
- Fingerprint: `tools/KEY_FINGERPRINT.txt`

## 7) Notes

- All cryptographic utilities are non-core helpers under `tools/`.
- Passing verification proves integrity and authenticity. It does not by itself prove scientific truth claims.
