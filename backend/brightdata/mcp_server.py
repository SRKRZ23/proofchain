"""PROOFCHAIN MCP Server — exposes verified-evidence web access as MCP tool.

Compatible with: Anthropic Claude Desktop, Cursor, LangChain, CrewAI.

When an AI agent calls our MCP tool, it receives:
  - content (the actual web data)
  - evidence_packet (Ed25519-signed metadata: URL, hash, timestamp, source, etc.)
  - verify_url (link to public verification endpoint)

This is the killer differentiator: Anthropic's MCP standard but with cryptographic provenance.

POST-KICKOFF: install fastmcp + register tools via decorator.
PRE-KICKOFF: skeleton + tool definitions ready.
"""
from __future__ import annotations

from typing import Optional

from ..proofchain_core.evidence_chain import WebEvidenceTrail
from .serp_client import SerpClient
from .scraper_client import WebScraperClient
from .unlocker_client import WebUnlockerClient


class ProofchainMCPServer:
    """MCP-compatible server exposing PROOFCHAIN evidence-collection tools.

    Tools exposed:
      - proofchain.search(query, engine, num_results) → results + evidence
      - proofchain.scrape(url, scraper_id) → structured data + evidence
      - proofchain.fetch(url) → raw content + evidence
      - proofchain.verify(evidence_packet) → signature verified bool
      - proofchain.export_chain() → full audit trail (EU AI Act compliant)
    """

    def __init__(self, evidence_trail: Optional[WebEvidenceTrail] = None):
        self.evidence_trail = evidence_trail or WebEvidenceTrail()
        self.serp = SerpClient(evidence_trail=self.evidence_trail)
        self.scraper = WebScraperClient(evidence_trail=self.evidence_trail)
        self.unlocker = WebUnlockerClient(evidence_trail=self.evidence_trail)

    # POST-KICKOFF: decorate these with @mcp.tool()
    def search(self, query: str, engine: str = "google", num_results: int = 10, request_id: str = "") -> dict:
        results = self.serp.search(query, engine, num_results, request_id)
        return {
            "results": [
                {
                    "title": r.title,
                    "url": r.url,
                    "snippet": r.snippet,
                    "rank": r.rank,
                    "content_hash": r.content_hash,
                }
                for r in results
            ],
            "evidence_chain_length": len(self.evidence_trail._chain.records()),
        }

    def scrape(self, url: str, scraper_id: str, request_id: str = "") -> dict:
        resp = self.scraper.scrape(url, scraper_id, request_id)
        return {
            "url": resp.url,
            "content": resp.content,
            "content_hash": resp.content_hash,
            "robots_status": resp.robots_status,
        }

    def fetch(self, url: str, request_id: str = "") -> dict:
        resp = self.unlocker.fetch(url, request_id)
        return {
            "url": resp.url,
            "content": resp.content,
            "content_hash": resp.content_hash,
            "bypass_method": resp.bypass_method,
            "status_code": resp.status_code,
        }

    def export_chain(self, eu_ai_act_compliant: bool = False) -> dict:
        if eu_ai_act_compliant:
            return self.evidence_trail.export_for_eu_ai_act()
        return self.evidence_trail.export()

    def verify_chain(self) -> bool:
        return self.evidence_trail.verify()
