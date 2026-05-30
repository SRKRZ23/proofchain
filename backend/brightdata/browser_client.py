"""Bright Data Scraping Browser — full browser automation for JS-heavy/interactive sites.

Docs: https://docs.brightdata.com/scraping-automation/scraping-browser/overview

Returns full page DOM + optional screenshot. Emits fetch_browser evidence.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Optional

import httpx

from ..proofchain_core.evidence_chain import WebEvidenceTrail, sha256hex


@dataclass
class BrowserResponse:
    url: str
    html: str
    content_hash: str
    screenshot_hash: Optional[str]
    final_url: str
    fetched_at: float


class ScrapingBrowserClient:
    BASE_URL = "wss://brd.superproxy.io:9223"  # CDP WebSocket endpoint

    def __init__(
        self,
        api_key: Optional[str] = None,
        evidence_trail: Optional[WebEvidenceTrail] = None,
        mock_mode: bool = False,
    ):
        self.api_key = api_key or os.getenv("BRIGHT_DATA_BROWSER_API_KEY", "")
        self.evidence_trail = evidence_trail
        self.mock_mode = mock_mode or not self.api_key

    def fetch(
        self,
        url: str,
        request_id: str = "",
        wait_for_selector: Optional[str] = None,
        screenshot: bool = False,
    ) -> BrowserResponse:
        t_start = time.time()

        if self.mock_mode:
            resp = self._mock_response(url, screenshot)
        else:
            resp = self._real_fetch(url, wait_for_selector, screenshot)

        latency_ms = (time.time() - t_start) * 1000

        if self.evidence_trail and request_id:
            self.evidence_trail.log_fetch_browser(
                request_id=request_id,
                url=url,
                content_hash=resp.content_hash,
                screenshot_hash=resp.screenshot_hash,
                latency_ms=latency_ms,
            )

        return resp

    def _real_fetch(
        self,
        url: str,
        wait_for_selector: Optional[str],
        screenshot: bool,
    ) -> BrowserResponse:
        """POST-KICKOFF: integrate Playwright + Bright Data CDP endpoint."""
        # Placeholder for Playwright CDP connection
        # from playwright.sync_api import sync_playwright
        # with sync_playwright() as p:
        #     browser = p.chromium.connect_over_cdp(self.BASE_URL, ...)
        #     page = browser.new_page()
        #     page.goto(url)
        #     if wait_for_selector: page.wait_for_selector(wait_for_selector)
        #     html = page.content()
        #     screenshot_bytes = page.screenshot() if screenshot else None
        raise NotImplementedError("Real CDP integration deferred to post-kickoff")

    def _mock_response(self, url: str, screenshot: bool) -> BrowserResponse:
        html = f"<html><head><title>Mock {url}</title></head><body><h1>Mock content</h1></body></html>"
        screenshot_hash = sha256hex(b"mock_screenshot_bytes") if screenshot else None
        return BrowserResponse(
            url=url,
            html=html,
            content_hash=sha256hex(html.encode()),
            screenshot_hash=screenshot_hash,
            final_url=url,
            fetched_at=time.time(),
        )
