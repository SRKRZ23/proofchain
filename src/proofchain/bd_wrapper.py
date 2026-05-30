"""Bright Data wrapper for PROOFCHAIN.

Wraps Bright Data API calls (MCP Server, Web Unlocker, SERP API) with
PROOFCHAIN cryptographic signing. Every fetch returns content + signed
evidence packet.

Reference: github.com/brightdata/skills (Apache 2.0, used as integration baseline).
Hackathon: Web Data UNLOCKED, Track 3 Security & Compliance / Infrastructure.

NOTE: Account approval pending as of 2026-05-25 23:30 UZT. This module is
written defensively к work с both real BD API (once token approved) AND
mock responses (для local testing before approval).
"""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import quote

try:
    import requests
except ImportError as e:
    raise ImportError("requests required. Install: pip install requests") from e

from proofchain.signing import ProofChainSigner


BD_ENDPOINT = "https://api.brightdata.com/request"
DEFAULT_TIMEOUT_SECONDS = 60


class BrightDataProofChainClient:
    """High-level client that wraps Bright Data API calls с PROOFCHAIN signing.

    Example:
        client = BrightDataProofChainClient(
            api_token=os.environ["BRIGHT_DATA_API_KEY"],
            serp_zone="serp_api1",
            unlocker_zone="web_unlocker1",
        )
        signed = client.search_web("OpenAI funding history")
        # signed contains content + signature + evidence_packet + public_key
    """

    def __init__(
        self,
        api_token: str | None = None,
        serp_zone: str | None = None,
        unlocker_zone: str | None = None,
        signer: ProofChainSigner | None = None,
        mock_mode: bool = False,
    ) -> None:
        """Initialize client.

        Args:
            api_token: Bright Data API token. Defaults к BRIGHT_DATA_API_KEY env var.
            serp_zone: SERP API zone name.
            unlocker_zone: Web Unlocker zone name.
            signer: ProofChain signer instance. Defaults к ephemeral generated key.
            mock_mode: If True, returns synthetic responses без hitting BD API.
                Useful для local testing before account approval.
        """
        self.api_token = api_token or os.environ.get("BRIGHT_DATA_API_KEY", "")
        self.serp_zone = serp_zone or os.environ.get("BD_SERP_ZONE", "serp_api1")
        self.unlocker_zone = unlocker_zone or os.environ.get(
            "BD_UNLOCKER_ZONE", "web_unlocker1"
        )
        self.signer = signer or ProofChainSigner()
        self.mock_mode = mock_mode or not self.api_token

    def _bd_request(
        self,
        zone: str,
        url: str,
        response_format: str = "raw",
    ) -> tuple[str, dict[str, Any]]:
        """Internal: POST к Bright Data, return (content, metadata)."""
        if self.mock_mode:
            return self._mock_response(zone, url, response_format)

        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "zone": zone,
            "url": url,
            "format": response_format,
        }
        resp = requests.post(
            BD_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        metadata = {
            "zone": zone,
            "url": url,
            "response_format": response_format,
            "status_code": resp.status_code,
            "request_id": resp.headers.get("x-request-id"),
        }
        return resp.text, metadata

    def _mock_response(
        self,
        zone: str,
        url: str,
        response_format: str,
    ) -> tuple[str, dict[str, Any]]:
        """Synthetic response для local development before BD approval."""
        mock_content = (
            f"[MOCK BD RESPONSE] zone={zone} url={url} format={response_format}\n"
            "This is a synthetic fixture for local testing.\n"
            "Real Bright Data integration activates when account approved."
        )
        return mock_content, {
            "zone": zone,
            "url": url,
            "response_format": response_format,
            "mock": True,
        }

    def search_web(self, query: str) -> dict[str, Any]:
        """SERP API: structured Google search results + cryptographic signature."""
        search_url = (
            f"https://www.google.com/search?q={quote(query)}&hl=en&gl=us"
        )
        content, metadata = self._bd_request(
            zone=self.serp_zone,
            url=search_url,
            response_format="json",
        )
        return self.signer.sign_response(content=content, bd_metadata=metadata)

    def scrape_url(self, url: str) -> dict[str, Any]:
        """Web Unlocker: raw HTML/JSON + cryptographic signature."""
        content, metadata = self._bd_request(
            zone=self.unlocker_zone,
            url=url,
            response_format="raw",
        )
        return self.signer.sign_response(content=content, bd_metadata=metadata)
