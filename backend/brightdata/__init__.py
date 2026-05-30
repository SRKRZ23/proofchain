"""Bright Data product clients — SERP API, Web Scraper API, Web Unlocker, Scraping Browser, MCP Server.

These are thin wrappers over Bright Data's public APIs. Each emits an EvidencePacket
event into the WebEvidenceTrail before returning content to the caller.

POST-KICKOFF: replace mock responses with real Bright Data API calls.
PRE-KICKOFF: structure is fixed so swap-in is mechanical (no architectural rework).
"""
from .serp_client import SerpClient
from .scraper_client import WebScraperClient
from .unlocker_client import WebUnlockerClient
from .browser_client import ScrapingBrowserClient
from .mcp_server import ProofchainMCPServer

__all__ = [
    "SerpClient",
    "WebScraperClient",
    "WebUnlockerClient",
    "ScrapingBrowserClient",
    "ProofchainMCPServer",
]
