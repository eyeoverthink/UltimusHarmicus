# uqcb_chain.py
# Helper: verifiable, epochal, PoW-protected memory chain for benchmarking and apps

import json, os, time, hashlib
from typing import List, Dict, Any, Optional, Callable, Tuple

DEFAULT_CHAIN_PATH = ".uqcb_chain.json"

# --------------------
# Hashing / Difficulty
# --------------------

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))

def leading_zero_bits(hex_hash: str) -> int:
    # Count leading zero bits in hex string
    bits = 0
    for ch in hex_hash:
        v = int(ch, 16)
        if v == 0:
            bits += 4
        else:
            # count leading zeros in this nibble
            for i in (8, 4, 2, 1):
                if v & i:
                    break
                bits += 1
            break
    return bits

def meets_difficulty(hex_hash: str, difficulty_bits: int) -> bool:
    return leading_zero_bits(hex_hash) >= difficulty_bits

# --------------------
# Chain I/O and verification
# --------------------

def load_chain(path: str = DEFAULT_CHAIN_PATH) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def find_block_by_payload(chain: List[Dict[str, Any]], predicate: Callable[[Dict[str, Any]], bool]) -> Optional[Dict[str, Any]]:
    """Finds the first block whose payload satisfies the predicate."""
    for block in reversed(chain): # Search backwards from the head
        if predicate(block['payload']):
            return block
    return None

def save_chain(chain: List[Dict[str, Any]], path: str = DEFAULT_CHAIN_PATH) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(chain, f, indent=2)
    os.replace(tmp, path)


def compute_block_hash(block_no_hash: Dict[str, Any]) -> str:
    # Expects all fields except 'hash' present
    s = canonical_json(block_no_hash).encode()
    return sha256_hex(s)


def verify_chain(chain: List[Dict[str, Any]], difficulty_bits: int) -> Tuple[bool, Optional[str]]:
    prev_hash = "GENESIS"
    for i, b in enumerate(chain):
        # Build a no-hash copy
        b_no_hash = {k: v for k, v in b.items() if k != "hash"}
        h = compute_block_hash(b_no_hash)
        if h != b.get("hash"):
            return False, f"hash mismatch at index {i}"
        if b.get("prevHash") != prev_hash:
            return False, f"broken link at index {i}"
        if not meets_difficulty(b.get("hash", ""), b.get("difficulty", difficulty_bits)):
            return False, f"difficulty not met at index {i}"
        prev_hash = b["hash"]
    return True, None


def latest_block(chain: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    return chain[-1] if chain else None


def latest_hash(chain: List[Dict[str, Any]]) -> Optional[str]:
    lb = latest_block(chain)
    return lb.get("hash") if lb else None

# --------------------
# Mining / Appending
# --------------------

def mine_block(prev_hash: str, epoch: int, index: int, payload: Dict[str, Any], difficulty_bits: int) -> Dict[str, Any]:
    block = {
        "index": index,
        "epoch": epoch,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "prevHash": prev_hash,
        "difficulty": difficulty_bits,
        "nonce": 0,
        "payload": payload,
    }
    # Simple linear nonce search
    nonce = 0
    while True:
        block["nonce"] = nonce
        h = compute_block_hash({k: v for k, v in block.items() if k != "hash"})
        if meets_difficulty(h, difficulty_bits):
            block["hash"] = h
            return block
        nonce += 1


def append_block(chain: List[Dict[str, Any]], payload: Dict[str, Any], difficulty_bits: int) -> List[Dict[str, Any]]:
    prev = latest_block(chain)
    prev_hash = prev["hash"] if prev else "GENESIS"
    epoch = (prev.get("epoch", -1) + 1) if prev else 0
    index = len(chain)
    block = mine_block(prev_hash, epoch, index, payload, difficulty_bits)
    new_chain = chain + [block]
    return new_chain
