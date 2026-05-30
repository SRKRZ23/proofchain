"""Multi-agent orchestrator — coordinates Searcher, Scraper, Verifier, Synthesizer.

Flow:
  1. analyst_query → log_agent_query
  2. Searcher.search(query) → SERP results
  3. Scraper.scrape(top URLs) → structured content
  4. Verifier.cross_check(sources) → detect conflicts, log them
  5. Synthesizer.answer(question, sources) → final answer + citation graph
  6. Return AgentResponse with answer + signed evidence chain

Each step is logged into WebEvidenceTrail. Final response includes verify_url.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Optional

from ..proofchain_core.evidence_chain import WebEvidenceTrail, sha256hex
from ..brightdata.serp_client import SerpClient, SerpResult
from ..brightdata.scraper_client import WebScraperClient


@dataclass
class Citation:
    url: str
    title: str
    snippet: str
    content_hash: str
    confidence: float
    conflict_flag: bool = False


@dataclass
class AgentResponse:
    request_id: str
    question: str
    answer: str
    citations: list[Citation]
    confidence: float
    latency_ms: float
    source_conflicts: list[dict] = field(default_factory=list)
    evidence_chain_length: int = 0
    verify_url: str = ""

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "question": self.question,
            "answer": self.answer,
            "citations": [
                {
                    "url": c.url,
                    "title": c.title,
                    "snippet": c.snippet,
                    "content_hash": c.content_hash,
                    "confidence": c.confidence,
                    "conflict_flag": c.conflict_flag,
                }
                for c in self.citations
            ],
            "confidence": self.confidence,
            "latency_ms": self.latency_ms,
            "source_conflicts": self.source_conflicts,
            "evidence_chain_length": self.evidence_chain_length,
            "verify_url": self.verify_url,
        }


class MultiAgentOrchestrator:
    def __init__(
        self,
        serp_client: Optional[SerpClient] = None,
        scraper_client: Optional[WebScraperClient] = None,
        evidence_trail: Optional[WebEvidenceTrail] = None,
        verify_base_url: str = "https://proofchain.dev/verify",
    ):
        self.evidence_trail = evidence_trail or WebEvidenceTrail()
        self.serp = serp_client or SerpClient(evidence_trail=self.evidence_trail)
        self.scraper = scraper_client or WebScraperClient(evidence_trail=self.evidence_trail)
        self.verify_base_url = verify_base_url

    def research(
        self,
        question: str,
        persona: str = "equity_analyst",
        num_sources: int = 5,
    ) -> AgentResponse:
        request_id = f"req_{uuid.uuid4().hex[:12]}"
        t_start = time.time()

        # Step 1: log analyst query
        self.evidence_trail.log_agent_query(
            request_id=request_id,
            question=question,
            persona=persona,
        )

        # Step 2: search
        results = self.serp.search(query=question, num_results=num_sources, request_id=request_id)

        # Step 3: synthesize citations (POST-KICKOFF: add real scraper + Claude calls)
        citations = self._build_citations(results)

        # Step 4: detect conflicts (placeholder — full Verifier post-kickoff)
        source_conflicts = self._detect_conflicts(citations, request_id)

        # Step 5: synthesize answer (placeholder — real Claude call post-kickoff)
        answer, confidence = self._synthesize_answer(question, citations)

        # Step 6: log synthesis
        self.evidence_trail.log_agent_synthesis(
            request_id=request_id,
            model="claude-sonnet-4-6",
            answer_hash=sha256hex(answer.encode()),
            citation_count=len(citations),
            confidence=confidence,
            latency_ms=(time.time() - t_start) * 1000,
        )

        return AgentResponse(
            request_id=request_id,
            question=question,
            answer=answer,
            citations=citations,
            confidence=confidence,
            latency_ms=(time.time() - t_start) * 1000,
            source_conflicts=source_conflicts,
            evidence_chain_length=len(self.evidence_trail._chain.records()),
            verify_url=f"{self.verify_base_url}/{request_id}",
        )

    def _build_citations(self, results: list[SerpResult]) -> list[Citation]:
        return [
            Citation(
                url=r.url,
                title=r.title,
                snippet=r.snippet,
                content_hash=r.content_hash,
                confidence=0.75 + (5 - r.rank) * 0.05,  # placeholder confidence
                conflict_flag=False,
            )
            for r in results
        ]

    def _detect_conflicts(self, citations: list[Citation], request_id: str) -> list[dict]:
        """POST-KICKOFF: real cross-source consistency check via embedding distance."""
        conflicts = []
        if len(citations) >= 2:
            self.evidence_trail.log_source_conflict(
                request_id=request_id,
                topic="placeholder_topic",
                source_a_hash=citations[0].content_hash,
                source_b_hash=citations[1].content_hash,
                disagreement_type="placeholder",
            )
        return conflicts

    def _synthesize_answer(self, question: str, citations: list[Citation]) -> tuple[str, float]:
        """POST-KICKOFF: real Claude call with citation grounding.

        For now returns mock answer with citation references.
        """
        answer = (
            f"[MOCK ANSWER for: {question}]\n\n"
            f"Based on {len(citations)} verified sources, here is a synthesized response. "
            f"Each citation includes cryptographic provenance. Confidence interval: high.\n\n"
            f"This is a placeholder. Post-kickoff this will be a real Claude synthesis "
            f"with verified citation grounding from {len(citations)} Bright Data sources."
        )
        return answer, 0.82  # placeholder confidence
