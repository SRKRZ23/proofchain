"""Ed25519 cryptographic signing layer для PROOFCHAIN.

Signs Bright Data API responses с tamper-evident evidence packets.
Every fetch returns content + Ed25519 signature + audit chain metadata
that can be independently verified by auditors.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass
from typing import Any

try:
    from nacl.signing import SigningKey, VerifyKey
    from nacl.encoding import HexEncoder
    from nacl.exceptions import BadSignatureError
except ImportError as e:
    raise ImportError(
        "PyNaCl required для Ed25519 signing. Install: pip install pynacl"
    ) from e


@dataclass
class EvidencePacket:
    """Tamper-evident metadata bundle accompanying a signed response."""

    content_hash: str
    bd_metadata: dict[str, Any]
    timestamp_ms: int
    audit_chain_id: str
    proofchain_version: str = "0.1.0"

    def to_canonical_json(self) -> bytes:
        """Serialize в canonical form для signing (sorted keys, no whitespace)."""
        return json.dumps(
            self.__dict__,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")


class ProofChainSigner:
    """Signs Bright Data API responses с Ed25519 evidence packets.

    Example:
        signer = ProofChainSigner()
        signed = signer.sign_response(
            content="<scraped HTML>",
            bd_metadata={"zone": "mcp_unlocker", "url": "https://example.com"},
        )
        # signed = {
        #     "content": "<scraped HTML>",
        #     "signature": "<hex>",
        #     "evidence_packet": {...},
        #     "public_key": "<hex>",
        # }
    """

    def __init__(self, private_key_hex: str | None = None) -> None:
        """Initialize signer. Provide private_key_hex для deterministic identity,
        omit для ephemeral key generation."""
        if private_key_hex:
            self.signing_key = SigningKey(
                private_key_hex.encode("ascii"),
                encoder=HexEncoder,
            )
        else:
            self.signing_key = SigningKey.generate()
        self.verify_key: VerifyKey = self.signing_key.verify_key

    @property
    def public_key_hex(self) -> str:
        """Hex-encoded public key (для distribution к verifiers)."""
        return self.verify_key.encode(encoder=HexEncoder).decode("ascii")

    @property
    def private_key_hex(self) -> str:
        """Hex-encoded private key — keep secret."""
        return self.signing_key.encode(encoder=HexEncoder).decode("ascii")

    def sign_response(
        self,
        content: str,
        bd_metadata: dict[str, Any],
    ) -> dict[str, Any]:
        """Sign a Bright Data API response с tamper-evident metadata.

        Args:
            content: The raw response body from Bright Data
                (HTML, JSON, etc.)
            bd_metadata: Bright Data fetch metadata
                (zone, url, timestamp, request_id, etc.)

        Returns:
            Dict с content + signature + evidence_packet + public_key.
        """
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        packet = EvidencePacket(
            content_hash=content_hash,
            bd_metadata=bd_metadata,
            timestamp_ms=int(time.time() * 1000),
            audit_chain_id=str(uuid.uuid4()),
        )

        signature = self.signing_key.sign(packet.to_canonical_json()).signature.hex()

        return {
            "content": content,
            "signature": signature,
            "evidence_packet": packet.__dict__,
            "public_key": self.public_key_hex,
        }


def verify_signed_response(signed_response: dict[str, Any]) -> bool:
    """Independently verify a PROOFCHAIN-signed response.

    Args:
        signed_response: Output of ProofChainSigner.sign_response()

    Returns:
        True if signature valid AND content hash matches AND public key
        successfully verifies — False otherwise.
    """
    content = signed_response["content"]
    signature_hex = signed_response["signature"]
    packet_dict = signed_response["evidence_packet"]
    public_key_hex = signed_response["public_key"]

    # Recompute content hash, verify it matches
    expected_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    if expected_hash != packet_dict["content_hash"]:
        return False

    # Reconstruct canonical payload
    packet = EvidencePacket(**packet_dict)
    payload = packet.to_canonical_json()

    # Verify signature
    verify_key = VerifyKey(public_key_hex.encode("ascii"), encoder=HexEncoder)
    try:
        verify_key.verify(payload, bytes.fromhex(signature_hex))
        return True
    except BadSignatureError:
        return False
