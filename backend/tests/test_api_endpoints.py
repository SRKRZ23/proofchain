"""FastAPI endpoint smoke tests via TestClient (no live server required)."""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND.parent))

import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


class TestHealthAndRoot:
    def test_health_endpoint(self):
        r = client.get("/health")
        assert r.status_code == 200

    def test_openapi_docs_available(self):
        r = client.get("/docs")
        assert r.status_code == 200


class TestResearchEndpoint:
    def test_submit_research_question(self):
        r = client.post("/api/research/", json={
            "question": "What is TSLA's customer concentration risk in Europe?",
            "persona": "equity_analyst",
            "num_sources": 3,
        })
        assert r.status_code == 200, r.text
        body = r.json()
        assert "request_id" in body
        assert "answer" in body
        assert "citations" in body
        assert "evidence_chain_length" in body
        assert "verify_url" in body
        assert body["evidence_chain_length"] > 0

    def test_orchestrator_stats(self):
        r = client.get("/api/research/orchestrator/stats")
        assert r.status_code == 200
        body = r.json()
        assert "total_records" in body
        assert "chain_valid" in body
        assert "verify_key_public" in body
        assert body["chain_valid"] is True


class TestVerifyEndpoint:
    def test_verify_after_research(self):
        # Submit a request first
        r = client.post("/api/research/", json={
            "question": "Test question for verify",
            "num_sources": 2,
        })
        rid = r.json()["request_id"]
        # Then verify it
        v = client.get(f"/api/verify/{rid}")
        assert v.status_code == 200, v.text
        body = v.json()
        assert body["verified"] is True
        assert body["request_id"] == rid
        assert body["record_count"] > 0
        assert "records" in body

    def test_verify_unknown_request_404(self):
        r = client.get("/api/verify/nonexistent_request_id_xyz")
        assert r.status_code == 404


class TestExportEndpoint:
    def test_full_chain_export(self):
        # Ensure at least 1 request has happened
        client.post("/api/research/", json={
            "question": "seed question for export",
            "num_sources": 2,
        })
        r = client.get("/api/export/full")
        assert r.status_code == 200, r.text
        body = r.json()
        assert "records" in body
        assert len(body["records"]) > 0

    def test_eu_ai_act_export(self):
        client.post("/api/research/", json={
            "question": "seed for eu-ai-act export",
            "num_sources": 2,
        })
        r = client.get("/api/export/eu-ai-act")
        assert r.status_code == 200
        body = r.json()
        assert "retention_months" in body
        assert "records" in body


class TestCORS:
    def test_cors_headers_present(self):
        r = client.options(
            "/api/research/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            },
        )
        # CORS preflight should succeed
        assert r.status_code in (200, 204), r.text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
