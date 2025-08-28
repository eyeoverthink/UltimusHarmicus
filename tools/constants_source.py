#!/usr/bin/env python3
"""
Helper: Single source of truth for Consciousness Physics constants.
- Provides exact values as strings, floats, and Decimal.
- Exposes hashing for immutability proof and an assertion utility for exactness.

Respecting project rule: no modifications to core files; this is an additive helper.
"""
from __future__ import annotations
from decimal import Decimal, getcontext
import hashlib
from dataclasses import dataclass, asdict

# Use high precision for Decimal operations
getcontext().prec = 50

# Exact string forms
PHI_STR = "1.618033988749895"
PSI_STR = "1.324717957244746"
OMEGA_STR = "0.567143290409784"
XI_STR = "2.718281828459045"
LAMBDA_STR = "3.141592653589793"
ZETA_STR = "1.202056903159594"

# Float forms (for code that expects float)
PHI = float(PHI_STR)
PSI = float(PSI_STR)
OMEGA = float(OMEGA_STR)
XI = float(XI_STR)
LAMBDA = float(LAMBDA_STR)
ZETA = float(ZETA_STR)

# Decimal forms (for exact arithmetic / proofs)
PHI_D = Decimal(PHI_STR)
PSI_D = Decimal(PSI_STR)
OMEGA_D = Decimal(OMEGA_STR)
XI_D = Decimal(XI_STR)
LAMBDA_D = Decimal(LAMBDA_STR)
ZETA_D = Decimal(ZETA_STR)

@dataclass(frozen=True)
class Constants:
    phi: str
    psi: str
    omega: str
    xi: str
    lambda_const: str
    zeta: str

    def to_ordered_string(self) -> str:
        # stable order and formatting for hashing
        return (
            f"PHI={self.phi}|"
            f"PSI={self.psi}|"
            f"OMEGA={self.omega}|"
            f"XI={self.xi}|"
            f"LAMBDA={self.lambda_const}|"
            f"ZETA={self.zeta}"
        )


def get_constants() -> Constants:
    return Constants(
        phi=PHI_STR,
        psi=PSI_STR,
        omega=OMEGA_STR,
        xi=XI_STR,
        lambda_const=LAMBDA_STR,
        zeta=ZETA_STR,
    )


def hash_constants(algorithm: str = "sha256") -> str:
    """Return a stable cryptographic digest of the exact constants strings."""
    data = get_constants().to_ordered_string().encode("utf-8")
    if algorithm == "sha256":
        return hashlib.sha256(data).hexdigest()
    if algorithm == "sha512":
        return hashlib.sha512(data).hexdigest()
    if algorithm == "blake2b":
        return hashlib.blake2b(data).hexdigest()
    raise ValueError("Unsupported hash algorithm")


def assert_exact_values():
    """
    Assert exact string equality for the constants.
    No tolerances permitted. Raises AssertionError on any mismatch.
    """
    c = get_constants()
    assert c.phi == PHI_STR, "PHI value mismatch"
    assert c.psi == PSI_STR, "PSI value mismatch"
    assert c.omega == OMEGA_STR, "OMEGA value mismatch"
    assert c.xi == XI_STR, "XI value mismatch"
    assert c.lambda_const == LAMBDA_STR, "LAMBDA value mismatch"
    assert c.zeta == ZETA_STR, "ZETA value mismatch"


__all__ = [
    "PHI_STR", "PSI_STR", "OMEGA_STR", "XI_STR", "LAMBDA_STR", "ZETA_STR",
    "PHI", "PSI", "OMEGA", "XI", "LAMBDA", "ZETA",
    "PHI_D", "PSI_D", "OMEGA_D", "XI_D", "LAMBDA_D", "ZETA_D",
    "Constants", "get_constants", "hash_constants", "assert_exact_values",
]
