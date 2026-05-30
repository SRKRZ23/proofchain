"""Tests for Bright Data client wrappers in mock mode.

Mock mode enables offline development + deterministic CI. Real-mode tests
require BRIGHT_DATA_* env vars and live API access.
"""
from __future__ import annotations

import sys
import os
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND.parent))

import pytest
from backend.brightdata.serp_client import SerpClient, SerpResult
from backend.brightdata.scraper_client import WebScraperClient, ScraperResponse
from backend.brightdata.unlocker_client import WebUnlockerClient, UnlockerResponse
from backend.brightdata.mcp_server import ProofchainMCPServer
from backend.proofchain_core.evidence_chain import WebEvidenceTrail


# ============================================================================
# SerpClient (mock mode)
# ============================================================================
class TestSerpClient:
    def test_mock_returns_n_results(self):
        client = SerpClient(api_key="", mock_mode=True)
        results = client.search("TSLA Q3 revenue", num_results=5)
        assert len(results) == 5
        assert all(isinstance(r, SerpResult) for r in results)

    def test_mock_results_have_required_fields(self):
        client = SerpClient(mock_mode=True)
        results = client.search("test query", num_results=3)
        for r in results:
            assert r.title and r.url and r.snippet
            assert isinstance(r.rank, int)
            assert len(r.content_hash) == 64  # sha256 hex

    def test_mock_results_have_unique_hashes(self):
        client = SerpClient(mock_mode=True)
        results = client.search("test", num_results=10)
        hashes = [r.content_hash for r in results]
        assert len(set(hashes)) == len(hashes), "hashes should be unique per result"

    def test_search_emits_evidence_when_trail_present(self):
        trail = WebEvidenceTrail()
        client = SerpClient(mock_mode=True, evidence_trail=trail)
        client.search("test", num_results=3, request_id="req_serp_1")
        records = trail._chain.records()
        serp_records = [r for r in records if r.entry.get("event") == "fetch_serp"]
        assert len(serp_records) == 1
        assert serp_records[0].entry["request_id"] == "req_serp_1"
        assert serp_records[0].entry["result_count"] == 3

    def test_no_evidence_emitted_without_request_id(self):
        trail = WebEvidenceTrail()
        client = SerpClient(mock_mode=True, evidence_trail=trail)
        client.search("test", num_results=3, request_id="")
        assert len(trail._chain.records()) == 0


# ============================================================================
# WebScraperClient (mock mode)
# ============================================================================
class TestWebScraperClient:
    def test_mock_scrape_returns_response(self):
        client = WebScraperClient(mock_mode=True)
        resp = client.scrape(url="https://example.com", scraper_id="generic_page")
        assert isinstance(resp, ScraperResponse)
        assert resp.url == "https://example.com"
        assert resp.content_hash and len(resp.content_hash) == 64

    def test_scrape_emits_evidence(self):
        trail = WebEvidenceTrail()
        client = WebScraperClient(mock_mode=True, evidence_trail=trail)
        client.scrape(
            url="https://example.com/10k",
            scraper_id="sec_filing",
            request_id="req_scrape_1",
        )
        scraper_records = [
            r for r in trail._chain.records()
            if r.entry.get("event") == "fetch_scraper"
        ]
        assert len(scraper_records) == 1
        assert scraper_records[0].entry["scraper_id"] == "sec_filing"


# ============================================================================
# WebUnlockerClient (mock mode)
# ============================================================================
class TestWebUnlockerClient:
    def test_mock_fetch_returns_response(self):
        client = WebUnlockerClient(mock_mode=True)
        resp = client.fetch(url="https://example.com/blocked")
        assert isinstance(resp, UnlockerResponse)
        assert len(resp.content_hash) == 64

    def test_fetch_emits_evidence(self):
        trail = WebEvidenceTrail()
        client = WebUnlockerClient(mock_mode=True, evidence_trail=trail)
        client.fetch(url="https://news.site/article", request_id="req_unlock_1")
        unlocker_records = [
            r for r in trail._chain.records()
            if r.entry.get("event") == "fetch_unlocker"
        ]
        assert len(unlocker_records) == 1


# ============================================================================
# ProofchainMCPServer integration
# ============================================================================
class TestMCPServerIntegration:
    def test_server_starts_with_default_trail(self):
        server = ProofchainMCPServer()
        assert server.evidence_trail is not None
        assert server.serp is not None
        assert server.scraper is not None
        assert server.unlocker is not None

    def test_mcp_search_returns_results_and_evidence(self):
        server = ProofchainMCPServer()
        # Force mock mode (no env vars set in test)
        server.serp.mock_mode = True
        result = server.search("TSLA Q3", request_id="req_mcp_1", num_results=3)
        assert "results" in result
        assert len(result["results"]) == 3
        assert result["evidence_chain_length"] >= 1

    def test_mcp_scrape_returns_evidence(self):
        server = ProofchainMCPServer()
        server.scraper.mock_mode = True
        result = server.scrape(
            url="https://sec.gov/10k/TSLA",
            scraper_id="sec_filing",
            request_id="req_mcp_2",
        )
        assert "content_hash" in result
        assert len(result["content_hash"]) == 64

    def test_mcp_fetch_returns_evidence(self):
        server = ProofchainMCPServer()
        server.unlocker.mock_mode = True
        result = server.fetch(url="https://example.com", request_id="req_mcp_3")
        assert "content_hash" in result

    def test_mcp_export_chain(self):
        server = ProofchainMCPServer()
        server.serp.mock_mode = True
        server.search("test", request_id="req_e1", num_results=2)
        server.scraper.mock_mode = True
        server.scrape(url="https://example.com", scraper_id="generic", request_id="req_e2")
        export = server.export_chain()
        assert "records" in export
        assert len(export["records"]) >= 2

    def test_mcp_verify_chain(self):
        server = ProofchainMCPServer()
        server.serp.mock_mode = True
        for i in range(5):
            server.search(f"query {i}", request_id=f"req_{i}", num_results=2)
        assert server.verify_chain() is True


# ============================================================================
# End-to-end flow simulation
# ============================================================================
class TestEndToEndFlow:
    def test_equity_research_question_full_chain(self):
        """Simulate an equity research analyst asking a question.

        Expected event sequence per question (per PROOFCHAIN spec):
          agent_query → fetch_serp → fetch_scraper (× N sources) → agent_synthesis
        """
        server = ProofchainMCPServer()
        server.serp.mock_mode = True
        server.scraper.mock_mode = True
        server.unlocker.mock_mode = True

        rid = "req_equity_TSLA"
        server.evidence_trail.log_agent_query(
            request_id=rid,
            question="What is TSLA's customer concentration risk in Europe?",
            persona="equity_research_analyst",
        )
        serp_result = server.search("TSLA Europe customer concentration", request_id=rid, num_results=3)
        for r in serp_result["results"]:
            server.scrape(url=r["url"], scraper_id="generic_page", request_id=rid)
        server.evidence_trail.log_agent_synthesis(
            request_id=rid,
            model="claude-sonnet-4-6",
            answer_hash="abc123",
            citation_count=3,
            confidence=0.85,
            latency_ms=2500.0,
        )

        records = server.evidence_trail._chain.records()
        events = [r.entry["event"] for r in records]
        assert events[0] == "agent_query"
        assert "fetch_serp" in events
        assert events.count("fetch_scraper") == 3
        assert events[-1] == "agent_synthesis"

        # Verify chain integrity
        assert server.verify_chain() is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
