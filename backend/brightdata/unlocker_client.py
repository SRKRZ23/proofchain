"""Bright Data Web Unlocker — bypass bot detection, CAPTCHAs, geo-blocks.

Docs: https://docs.brightdata.com/scraping-automation/web-unlocker/overview

Returns raw HTML/JSON from blocked/protected sites. Emits fetch_unlocker evidence.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Optional

import httpx

from ..proofchain_core.evidence_chain import WebEvidenceTrail, sha256hex


@dataclass
class UnlockerResponse:
    url: str
    content: str
    content_type: str
    content_hash: str
    bypass_method: str
    status_code: int
    fetched_at: float


class WebUnlockerClient:
    BASE_URL = "https://api.brightdata.com/unlocker"

    def __init__(
        self,
        api_key: Optional[str] = None,
        evidence_trail: Optional[WebEvidenceTrail] = None,
        mock_mode: bool = False,
    ):
        self.api_key = api_key or os.getenv("BRIGHT_DATA_UNLOCKER_API_KEY", "")
        self.evidence_trail = evidence_trail
        self.mock_mode = mock_mode or not self.api_key

    def fetch(
        self,
        url: str,
        request_id: str = "",
        method: str = "GET",
    ) -> UnlockerResponse:
        t_start = time.time()

        if self.mock_mode:
            resp = self._mock_response(url)
        else:
            resp = self._real_fetch(url, method)

        latency_ms = (time.time() - t_start) * 1000

        if self.evidence_trail and request_id:
            self.evidence_trail.log_fetch_unlocker(
                request_id=request_id,
                url=url,
                content_hash=resp.content_hash,
                bypass_method=resp.bypass_method,
                latency_ms=latency_ms,
            )

        return resp

    def _real_fetch(self, url: str, method: str) -> UnlockerResponse:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"url": url, "method": method}
        with httpx.Client(timeout=60.0) as client:
            r = client.post(self.BASE_URL, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
        content = data.get("body", "")
        return UnlockerResponse(
            url=url,
            content=content,
            content_type=data.get("content_type", "text/html"),
            content_hash=sha256hex(content.encode()),
            bypass_method=data.get("bypass_method", "residential_proxy"),
            status_code=data.get("status_code", 200),
            fetched_at=time.time(),
        )

    def _mock_response(self, url: str) -> UnlockerResponse:
        content = f"<html><body>Mock unlocked content from {url}</body></html>"
        return UnlockerResponse(
            url=url,
            content=content,
            content_type="text/html",
            content_hash=sha256hex(content.encode()),
            bypass_method="mock",
            status_code=200,
            fetched_at=time.time(),
        )
