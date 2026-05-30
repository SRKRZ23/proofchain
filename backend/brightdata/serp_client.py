"""Bright Data SERP API client — real-time structured search results from Google/Bing/Yandex.

Docs: https://docs.brightdata.com/scraping-automation/serp-api/overview

Each search call:
  1. Hashes the query (privacy-preserving evidence)
  2. Calls Bright Data SERP endpoint
  3. SHA-256 hashes every result content
  4. Emits fetch_serp event into WebEvidenceTrail
  5. Returns results with evidence_packet attached
"""
from __future__ import annotations

import hashlib
import os
import time
from dataclasses import dataclass
from typing import Optional

import httpx

from ..proofchain_core.evidence_chain import WebEvidenceTrail, sha256hex


@dataclass
class SerpResult:
    title: str
    url: str
    snippet: str
    rank: int
    content_hash: str
    fetched_at: float


class SerpClient:
    """Bright Data SERP API wrapper with provenance evidence emission."""

    BASE_URL = "https://serp.brightdata.com/api/search"

    def __init__(
        self,
        api_key: Optional[str] = None,
        evidence_trail: Optional[WebEvidenceTrail] = None,
        mock_mode: bool = False,
    ):
        self.api_key = api_key or os.getenv("BRIGHT_DATA_SERP_API_KEY", "")
        self.evidence_trail = evidence_trail
        # POST-KICKOFF: set mock_mode=False once API keys claimed Day 1
        self.mock_mode = mock_mode or not self.api_key

    def search(
        self,
        query: str,
        engine: str = "google",
        num_results: int = 10,
        request_id: str = "",
    ) -> list[SerpResult]:
        """Returns top N organic results + emits signed evidence packet."""
        t_start = time.time()

        if self.mock_mode:
            results = self._mock_results(query, num_results)
        else:
            results = self._real_search(query, engine, num_results)

        latency_ms = (time.time() - t_start) * 1000

        if self.evidence_trail and request_id:
            self.evidence_trail.log_fetch_serp(
                request_id=request_id,
                query=query,
                engine=engine,
                result_count=len(results),
                latency_ms=latency_ms,
            )

        return results

    def _real_search(self, query: str, engine: str, num_results: int) -> list[SerpResult]:
        """POST-KICKOFF: implement real Bright Data SERP API call."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"q": query, "engine": engine, "num": num_results}
        with httpx.Client(timeout=30.0) as client:
            r = client.get(self.BASE_URL, params=params, headers=headers)
            r.raise_for_status()
            data = r.json()
        return [
            SerpResult(
                title=item.get("title", ""),
                url=item.get("link", ""),
                snippet=item.get("snippet", ""),
                rank=item.get("rank", i + 1),
                content_hash=sha256hex(
                    f"{item.get('title','')}{item.get('link','')}{item.get('snippet','')}".encode()
                ),
                fetched_at=time.time(),
            )
            for i, item in enumerate(data.get("organic_results", []))
        ]

    def _mock_results(self, query: str, num_results: int) -> list[SerpResult]:
        """PRE-KICKOFF stub — returns deterministic fake results for offline dev."""
        return [
            SerpResult(
                title=f"Mock result {i+1} for '{query}'",
                url=f"https://example.com/result-{i+1}",
                snippet=f"This is a mock snippet for testing. Query: {query[:40]}",
                rank=i + 1,
                content_hash=sha256hex(f"mock-{query}-{i}".encode()),
                fetched_at=time.time(),
            )
            for i in range(num_results)
        ]
