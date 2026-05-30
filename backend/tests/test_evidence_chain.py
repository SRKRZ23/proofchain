"""Comprehensive tests for EvidenceChain hash-chaining + Ed25519 signing.

Covers the 5 stated properties (P1-P5) from evidence_chain.py docstring:
  P1  JCS determinism    — canonical(X) == canonical(X) always
  P2  Sign+verify RT     — sign(packet) → verify(sig, packet) == OK
  P3  Tamper-decision    — mutate packet.content → verify fails
  P4  Hash-chaining      — each record commits to all previous
  P5  EU AI Act Article 12 — retention export endpoint compliant
"""
from __future__ import annotations

import sys
import json
from pathlib import Path

# Make backend importable
BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND.parent))

import pytest
from backend.proofchain_core.evidence_chain import (
    EvidenceChain,
    EvidencePacket,
    WebEvidenceTrail,
    canonical,
    sha256hex,
    GENESIS_HASH,
)


# ============================================================================
# P1 — JCS determinism
# ============================================================================
class TestCanonicalDeterminism:
    def test_canonical_is_deterministic_simple(self):
        obj = {"b": 1, "a": 2}
        assert canonical(obj) == canonical({"a": 2, "b": 1})

    def test_canonical_handles_nested(self):
        obj = {"outer": {"z": 1, "a": 2}, "key": "val"}
        result = canonical(obj)
        # Re-encode with reversed insertion order — should match
        obj2 = {"key": "val", "outer": {"a": 2, "z": 1}}
        assert canonical(obj2) == result

    def test_canonical_no_whitespace(self):
        b = canonical({"a": 1, "b": 2})
        assert b" " not in b
        assert b == b'{"a":1,"b":2}'

    def test_canonical_unicode_preserved(self):
        b = canonical({"name": "Уолтер"})
        # ensure_ascii=False → Cyrillic should pass through
        assert "Уолтер".encode("utf-8") in b


# ============================================================================
# P2 — Sign + verify round-trip
# ============================================================================
class TestSignVerifyRoundtrip:
    def test_append_then_verify(self):
        chain = EvidenceChain()
        rec = chain.append({"action": "fetch", "url": "https://example.com"})
        assert rec.verify(chain.verify_key) is True

    def test_verify_with_wrong_key_fails(self):
        chain1 = EvidenceChain()
        chain2 = EvidenceChain()
        rec = chain1.append({"action": "fetch"})
        # rec was signed by chain1's key; verifying with chain2's key must fail
        assert rec.verify(chain2.verify_key) is False

    def test_verify_chain_all_records(self):
        chain = EvidenceChain()
        for i in range(10):
            chain.append({"action": f"step_{i}", "n": i})
        assert chain.verify_chain() is True


# ============================================================================
# P3 — Tamper decision
# ============================================================================
class TestTamperDetection:
    def test_tampered_entry_fails(self):
        chain = EvidenceChain()
        rec = chain.append({"url": "https://example.com", "amount": 100})
        # Tamper with entry after signing
        rec.entry["amount"] = 1_000_000
        assert rec.verify(chain.verify_key) is False

    def test_tampered_seq_fails(self):
        chain = EvidenceChain()
        rec = chain.append({"x": 1})
        rec.seq = 999  # change seq
        assert rec.verify(chain.verify_key) is False

    def test_tampered_prev_hash_fails(self):
        chain = EvidenceChain()
        rec = chain.append({"x": 1})
        rec.prev_hash = "0" * 64  # fake genesis
        # Note: only fails if prev_hash was non-genesis to start; first record IS genesis
        chain.append({"x": 2})  # make a 2nd record
        rec2 = chain._records[1]
        original_prev = rec2.prev_hash
        rec2.prev_hash = "1" * 64
        assert rec2.verify(chain.verify_key) is False
        rec2.prev_hash = original_prev  # restore

    def test_chain_detects_tamper_via_verify_chain(self):
        chain = EvidenceChain()
        chain.append({"x": 1})
        chain.append({"x": 2})
        chain.append({"x": 3})
        # Tamper one record
        chain._records[1].entry["x"] = 999
        assert chain.verify_chain() is False


# ============================================================================
# P4 — Hash-chaining commitment
# ============================================================================
class TestHashChaining:
    def test_first_record_uses_genesis(self):
        chain = EvidenceChain()
        rec = chain.append({"x": 1})
        assert rec.prev_hash == GENESIS_HASH

    def test_second_record_commits_to_first(self):
        chain = EvidenceChain()
        rec1 = chain.append({"x": 1})
        rec2 = chain.append({"x": 2})
        assert rec2.prev_hash == rec1.record_hash

    def test_seq_is_monotonic(self):
        chain = EvidenceChain()
        seqs = [chain.append({"i": i}).seq for i in range(5)]
        assert seqs == [0, 1, 2, 3, 4]

    def test_chain_break_by_inserting_record_fails(self):
        """If you splice in a record, hash chain breaks."""
        chain = EvidenceChain()
        chain.append({"x": 1})
        chain.append({"x": 2})
        # Forge a 3rd record claiming to be index 2 but with wrong prev_hash
        chain._records.insert(2, EvidencePacket(
            entry={"x": "FORGED"},
            prev_hash="bad",
            seq=2,
            signature=b"\x00" * 64,
            record_hash="bad_hash",
        ))
        assert chain.verify_chain() is False


# ============================================================================
# P5 — EU AI Act Article 12 export
# ============================================================================
class TestEUAIActExport:
    def test_export_returns_structured_dict(self):
        chain = EvidenceChain()
        for i in range(3):
            chain.append({"step": i})
        exported = chain.export()
        assert isinstance(exported, dict)
        assert "records" in exported
        assert "verify_key" in exported
        assert len(exported["records"]) == 3

    def test_web_evidence_trail_full_lifecycle(self):
        trail = WebEvidenceTrail()
        rid = "req_test_123"
        trail.log_agent_query(rid, "test question", "analyst")
        trail.log_fetch_serp(
            request_id=rid, query="test", engine="google",
            result_count=5, latency_ms=150.0,
        )
        trail.log_fetch_unlocker(
            request_id=rid, url="https://example.com",
            content_hash="def", bypass_method="residential_proxy", latency_ms=850.0,
        )
        trail.log_agent_synthesis(
            request_id=rid, model="claude-sonnet-4-6", answer_hash="789",
            citation_count=5, confidence=0.92, latency_ms=2400.0,
        )
        export = trail.export_for_eu_ai_act(retention_months=6)
        assert "retention_months" in export
        assert "records" in export
        # Confirm chain still verifies
        assert trail.verify() is True


# ============================================================================
# Stress tests
# ============================================================================
class TestStress:
    def test_1000_records(self):
        chain = EvidenceChain()
        for i in range(1000):
            chain.append({"i": i, "data": f"record_{i}"})
        assert len(chain.records()) == 1000
        assert chain.verify_chain() is True

    def test_signing_keys_distinct_across_chains(self):
        chain1 = EvidenceChain()
        chain2 = EvidenceChain()
        assert chain1.verify_key_hex != chain2.verify_key_hex

    def test_record_hash_unique_per_entry(self):
        chain = EvidenceChain()
        r1 = chain.append({"x": 1})
        r2 = chain.append({"x": 1})  # same entry, but seq differs → different hash
        assert r1.record_hash != r2.record_hash


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
