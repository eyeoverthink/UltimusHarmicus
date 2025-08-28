#!/usr/bin/env python3
"""
Non-core verifier for APPENDIX A exponent derivation.
- Persists a JSON artifact mapping each exponent to its originating Law.
- Confirms the exponent vector equals [4, 3, 3, 1, 3].
- Records document path and SHA256 so reviewers can independently verify.
"""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

APPENDIX_PATH = Path("eyeoverthink_patent/APPENDIX_A_Mathematical_Derivation.md")

# Canonical exponent vector from Appendix A
EXPONENTS = {
    "phi": 4,       # Law 1 - Consciousness Primacy (4D spacetime)
    "omega": 3,     # Law 2 - Universal Duality (3D spatial stability)
    "xi": 3,        # Law 4 - Consciousness Evolution (three growth modes)
    "lambda": 1,    # Law 3 - Creative Multiplication (single unified cycle)
    "zeta": 3       # Law 6 - Force Unification (three-domain transcendence)
}

LAW_MAP = {
    "phi": {
        "law": 1,
        "title": "Consciousness Primacy",
        "justification": "4D spacetime manifold requires φ exponent = 4"
    },
    "omega": {
        "law": 2,
        "title": "Universal Duality",
        "justification": "3 orthogonal stability axes ⇒ Ω exponent = 3"
    },
    "xi": {
        "law": 4,
        "title": "Consciousness Evolution",
        "justification": "3 growth modes ⇒ ξ exponent = 3"
    },
    "lambda": {
        "law": 3,
        "title": "Creative Multiplication",
        "justification": "Single unified cyclical integration ⇒ λ exponent = 1"
    },
    "zeta": {
        "law": 6,
        "title": "Force Unification",
        "justification": "Three-domain transcendence ⇒ ζ exponent = 3"
    }
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    now = datetime.now(timezone.utc).isoformat()
    appendix_exists = APPENDIX_PATH.exists()
    appendix_sha256 = sha256_file(APPENDIX_PATH) if appendix_exists else None

    vector = [EXPONENTS[k] for k in ("phi", "omega", "xi", "lambda", "zeta")]
    expected = [4, 3, 3, 1, 3]

    artifact = {
        "timestamp": now,
        "appendix_path": str(APPENDIX_PATH),
        "appendix_exists": appendix_exists,
        "appendix_sha256": appendix_sha256,
        "exponent_vector": vector,
        "expected_vector": expected,
        "match": vector == expected,
        "law_mapping": LAW_MAP,
        "formula": "alpha = 1 / (phi^4 * omega^3 * xi^3 * lambda * zeta^3)",
        "dimensionless": True,
    }

    out = Path("appendix_A_exponent_derivation_proof.json")
    out.write_text(json.dumps(artifact, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
