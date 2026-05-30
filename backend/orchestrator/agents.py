"""Individual agent implementations.

POST-KICKOFF: each agent gets real LLM calls + Bright Data tool integration.
PRE-KICKOFF: skeleton + interface contracts ready.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class AgentTask:
    task_id: str
    task_type: str
    payload: dict


class SearcherAgent:
    """Uses SERP API to find relevant sources for a question."""
    name = "searcher"

    def __init__(self, serp_client):
        self.serp = serp_client

    def search(self, query: str, num_results: int = 10, request_id: str = ""):
        return self.serp.search(query=query, num_results=num_results, request_id=request_id)


class ScraperAgent:
    """Uses Web Scraper API to extract structured content from top URLs."""
    name = "scraper"

    def __init__(self, scraper_client):
        self.scraper = scraper_client

    def scrape_url(self, url: str, scraper_id: str = "generic_page", request_id: str = ""):
        return self.scraper.scrape(url=url, scraper_id=scraper_id, request_id=request_id)


class VerifierAgent:
    """Cross-source consistency check + conflict detection.

    POST-KICKOFF: embedding-based semantic similarity + LLM-as-judge for
    materially conflicting claims (e.g., '$25B revenue' vs '$30B revenue').
    """
    name = "verifier"

    def cross_check(self, sources: list[dict]) -> list[dict]:
        """Returns list of detected conflicts. Stub for now."""
        return []


class SynthesizerAgent:
    """Final-answer synthesis using Claude Sonnet 4.6.

    POST-KICKOFF: real Anthropic API call with citation grounding prompt.
    Output format: answer + per-claim citation map.
    """
    name = "synthesizer"

    def __init__(self, model: str = "claude-sonnet-4-6"):
        self.model = model

    def synthesize(self, question: str, citations: list[dict]) -> tuple[str, float]:
        """Returns (answer, confidence)."""
        # POST-KICKOFF: real Claude call
        return f"[MOCK] Answer to '{question}' based on {len(citations)} citations.", 0.82
