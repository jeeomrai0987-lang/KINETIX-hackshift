import json
import hashlib
from typing import Any, Dict

def compute_canonical_hash(payload: Dict[str, Any]) -> str:
    """
    Computes a deterministic SHA-256 hash with a '0x' prefix from the canonical JSON
    representation of the payload (keys sorted, compact separators).
    Meets Section 6 Rule 2 of docs/SHARED_CONTRACT.md.
    """
    canonical_json = json.dumps(payload, sort_keys=True, separators=(',', ':'), default=str)
    sha256_hex = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
    return f"0x{sha256_hex}"
