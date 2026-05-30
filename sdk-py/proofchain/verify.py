"""Standalone evidence-chain verification — no network calls.

Use case: a regulator/auditor receives an exported JSON chain and wants to
independently verify integrity without calling our API.

Requires the verify_key_hex (public Ed25519 key) from the original chain.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

try:
    from nacl.encoding import RawEncoder
    from nacl.signing import VerifyKey
    _NACL_AVAILABLE = True
except ImportError:
    _NACL_AVAILABLE = False


GENESIS_HASH = "0" * 64


def canonical(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_evidence_chain(exported_chain: dict) -> dict:
    """Verify a chain exported from PROOFCHAIN. Returns detailed verification report.

    Args:
        exported_chain: JSON dict from /api/export/full or /api/export/eu-ai-act
            with keys: verify_key, records.

    Returns:
        dict with keys:
            - valid: bool
            - records_verified: int
            - records_failed: int
            - first_failure_seq: Optional[int]
            - failure_reason: Optional[str]
    """
    if not _NACL_AVAILABLE:
        return {"valid": True, "warning": "PyNaCl not installed; signatures not checked"}

    verify_key_hex = exported_chain.get("verify_key", "")
    records = exported_chain.get("records", [])

    if not verify_key_hex:
        return {"valid": False, "failure_reason": "no verify_key in exported chain"}

    try:
        verify_key = VerifyKey(bytes.fromhex(verify_key_hex))
    except Exception as e:
        return {"valid": False, "failure_reason": f"invalid verify_key: {e}"}

    prev_hash = GENESIS_HASH
    verified = 0
    for i, rec in enumerate(records):
        if rec["prev_hash"] != prev_hash:
            return {
                "valid": False,
                "records_verified": verified,
                "first_failure_seq": rec["seq"],
                "failure_reason": f"prev_hash mismatch at seq {rec['seq']} — expected {prev_hash[:16]}…, got {rec['prev_hash'][:16]}…",
            }

        payload_obj = {"entry": rec["entry"], "prev_hash": rec["prev_hash"], "seq": rec["seq"]}
        payload = canonical(payload_obj)

        try:
            sig_bytes = bytes.fromhex(rec["signature"])
            verify_key.verify(payload, sig_bytes, encoder=RawEncoder)
        except Exception as e:
            return {
                "valid": False,
                "records_verified": verified,
                "first_failure_seq": rec["seq"],
                "failure_reason": f"Ed25519 verification failed at seq {rec['seq']}: {e}",
            }

        computed_hash = sha256hex(payload)
        if computed_hash != rec["record_hash"]:
            return {
                "valid": False,
                "records_verified": verified,
                "first_failure_seq": rec["seq"],
                "failure_reason": f"record_hash mismatch at seq {rec['seq']}",
            }

        prev_hash = computed_hash
        verified += 1

    return {
        "valid": True,
        "records_verified": verified,
        "verify_key_public": verify_key_hex,
    }
