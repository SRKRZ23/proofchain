"""PROOFCHAIN core — Ed25519-signed, hash-chained evidence trail for AI agents on the live web.

Public API:
  - EvidenceChain        — append-only hash-chained log of evidence packets
  - EvidencePacket       — single Ed25519-signed record
  - WebEvidenceTrail     — high-level wrapper with Bright Data event types
  - sha256hex            — canonical hashing helper
"""
from .evidence_chain import (
    EvidenceChain,
    EvidencePacket,
    WebEvidenceTrail,
    sha256hex,
    canonical,
    GENESIS_HASH,
)

__all__ = [
    "EvidenceChain",
    "EvidencePacket",
    "WebEvidenceTrail",
    "sha256hex",
    "canonical",
    "GENESIS_HASH",
]

__version__ = "0.1.0-alpha"
