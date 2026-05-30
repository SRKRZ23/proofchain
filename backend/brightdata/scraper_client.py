"""Bright Data Web Scraper API client — 660+ pre-built site scrapers (Amazon, LinkedIn, etc).

Docs: https://docs.brightdata.com/scraping-automation/web-scraper-api/overview

Returns structured JSON. Each scrape emits fetch_scraper evidence packet.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Optional

import httpx

from ..proofchain_core.evidence_chain import WebEvidenceTrail, sha256hex


@dataclass
class ScraperResponse:
    url: str
    scraper_id: str
    content: dict
    content_hash: str
    robots_status: str
    fetched_at: float


class WebScraperClient:
    BASE_URL = "https://api.brightdata.com/datasets/v3/scrape"

    def __init__(
        self,
        api_key: Optional[str] = None,
        evidence_trail: Optional[WebEvidenceTrail] = None,
        mock_mode: bool = False,
    ):
        self.api_key = api_key or os.getenv("BRIGHT_DATA_SCRAPER_API_KEY", "")
        self.evidence_trail = evidence_trail
        self.mock_mode = mock_mode or not self.api_key

    def scrape(
        self,
        url: str,
        scraper_id: str,
        request_id: str = "",
    ) -> ScraperResponse:
        t_start = time.time()

        if self.mock_mode:
            resp = self._mock_response(url, scraper_id)
        else:
            resp = self._real_scrape(url, scraper_id)

        latency_ms = (time.time() - t_start) * 1000

        if self.evidence_trail and request_id:
            self.evidence_trail.log_fetch_scraper(
                request_id=request_id,
                url=url,
                content_hash=resp.content_hash,
                scraper_id=scraper_id,
                robots_status=resp.robots_status,
                latency_ms=latency_ms,
            )

        return resp

    def _real_scrape(self, url: str, scraper_id: str) -> ScraperResponse:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"url": url, "scraper_id": scraper_id}
        with httpx.Client(timeout=60.0) as client:
            r = client.post(self.BASE_URL, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
        content = data.get("content", {})
        return ScraperResponse(
            url=url,
            scraper_id=scraper_id,
            content=content,
            content_hash=sha256hex(str(content).encode()),
            robots_status=data.get("robots_txt_status", "unknown"),
            fetched_at=time.time(),
        )

    def _mock_response(self, url: str, scraper_id: str) -> ScraperResponse:
        content = {
            "title": f"Mock scrape of {url}",
            "scraper": scraper_id,
            "extracted_at": time.time(),
            "fields": {"sample_field": "sample_value"},
        }
        return ScraperResponse(
            url=url,
            scraper_id=scraper_id,
            content=content,
            content_hash=sha256hex(str(content).encode()),
            robots_status="allowed",
            fetched_at=time.time(),
        )
