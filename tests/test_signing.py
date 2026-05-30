"""Tests for PROOFCHAIN Ed25519 signing module."""

from __future__ import annotations

import sys
from pathlib import Path

# Add src/ to sys.path so tests can import proofchain without install.
SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from proofchain.signing import ProofChainSigner, verify_signed_response


def test_sign_and_verify_roundtrip() -> None:
    """Signed response verifies successfully on roundtrip."""
    signer = ProofChainSigner()
    signed = signer.sign_response(
        content="hello world",
        bd_metadata={"zone": "mcp_unlocker", "url": "https://example.com"},
    )
    assert verify_signed_response(signed) is True


def test_tampered_content_fails_verification() -> None:
    """Modifying content invalidates the signature."""
    signer = ProofChainSigner()
    signed = signer.sign_response(
        content="original content",
        bd_metadata={"zone": "mcp_unlocker"},
    )
    signed["content"] = "tampered content"
    assert verify_signed_response(signed) is False


def test_tampered_signature_fails_verification() -> None:
    """Modifying signature invalidates verification."""
    signer = ProofChainSigner()
    signed = signer.sign_response(
        content="content",
        bd_metadata={"zone": "mcp_unlocker"},
    )
    # Flip one hex character in signature
    sig = signed["signature"]
    signed["signature"] = ("0" if sig[0] != "0" else "1") + sig[1:]
    assert verify_signed_response(signed) is False


def test_deterministic_signer_from_private_key() -> None:
    """Same private key produces same public key across instances."""
    s1 = ProofChainSigner()
    private_hex = s1.private_key_hex
    s2 = ProofChainSigner(private_key_hex=private_hex)
    assert s1.public_key_hex == s2.public_key_hex


def test_evidence_packet_contains_required_fields() -> None:
    """Evidence packet structure includes all metadata fields."""
    signer = ProofChainSigner()
    signed = signer.sign_response(
        content="test",
        bd_metadata={"zone": "x"},
    )
    packet = signed["evidence_packet"]
    for required_field in (
        "content_hash",
        "bd_metadata",
        "timestamp_ms",
        "audit_chain_id",
        "proofchain_version",
    ):
        assert required_field in packet, f"Missing: {required_field}"


def test_audit_chain_ids_unique() -> None:
    """Each signed response has a unique audit_chain_id."""
    signer = ProofChainSigner()
    ids = {
        signer.sign_response(
            content=f"content {i}",
            bd_metadata={"i": i},
        )["evidence_packet"]["audit_chain_id"]
        for i in range(20)
    }
    assert len(ids) == 20


if __name__ == "__main__":
    test_sign_and_verify_roundtrip()
    test_tampered_content_fails_verification()
    test_tampered_signature_fails_verification()
    test_deterministic_signer_from_private_key()
    test_evidence_packet_contains_required_fields()
    test_audit_chain_ids_unique()
    print("All tests passed")
