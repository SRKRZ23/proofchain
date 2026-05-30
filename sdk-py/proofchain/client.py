"""Client — primary entry point for proofchain-sdk."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

import httpx


@dataclass
class Citation:
    rank: int
    url: str
    title: str
    snippet: str
    content_hash: str
    confidence: float
    verified: bool = True
    conflict_flag: bool = False


@dataclass
class ResearchResult:
    request_id: str
    question: str
    answer: str
    citations: list[Citation]
    confidence: float
    latency_ms: float
    evidence_chain_length: int
    verify_url: str
    source_conflicts: list[dict] = field(default_factory=list)


class Client:
    """PROOFCHAIN Python client.

    Usage:
        from proofchain import Client
        pc = Client(api_key="...")
        result = pc.search("question", num_results=5)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: str = "https://api.proofchain.dev",
        timeout: float = 60.0,
    ):
        self.api_key = api_key or os.getenv("PROOFCHAIN_API_KEY") or os.getenv("BRIGHT_DATA_API_KEY", "")
        self.api_base = api_base.rstrip("/")
        self.timeout = timeout

    def search(
        self,
        question: str,
        persona: str = "equity_analyst",
        num_results: int = 5,
    ) -> ResearchResult:
        """Submit a research question, get answer + signed citation graph."""
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        with httpx.Client(timeout=self.timeout) as client:
            r = client.post(
                f"{self.api_base}/api/research/",
                json={"question": question, "persona": persona, "num_sources": num_results},
                headers=headers,
            )
            r.raise_for_status()
            data = r.json()

        citations = [
            Citation(
                rank=i + 1,
                url=c["url"],
                title=c["title"],
                snippet=c["snippet"],
                content_hash=c["content_hash"],
                confidence=c["confidence"],
                verified=not c.get("conflict_flag", False),
                conflict_flag=c.get("conflict_flag", False),
            )
            for i, c in enumerate(data["citations"])
        ]

        return ResearchResult(
            request_id=data["request_id"],
            question=data["question"],
            answer=data["answer"],
            citations=citations,
            confidence=data["confidence"],
            latency_ms=data["latency_ms"],
            evidence_chain_length=data["evidence_chain_length"],
            verify_url=data["verify_url"],
            source_conflicts=data.get("source_conflicts", []),
        )

    def verify(self, request_id: str) -> dict:
        """Verify the evidence chain for a given request_id."""
        with httpx.Client(timeout=self.timeout) as client:
            r = client.get(f"{self.api_base}/api/verify/{request_id}")
            r.raise_for_status()
            return r.json()

    def export_chain(self, eu_ai_act_compliant: bool = False) -> dict:
        """Export the full evidence chain (or EU AI Act-filtered subset)."""
        endpoint = "/api/export/eu-ai-act" if eu_ai_act_compliant else "/api/export/full"
        with httpx.Client(timeout=self.timeout) as client:
            r = client.get(f"{self.api_base}{endpoint}")
            r.raise_for_status()
            return r.json()
