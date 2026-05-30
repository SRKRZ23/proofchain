"""Multi-agent orchestrator for PROOFCHAIN equity research demo.

Four named agents coordinate to answer a research question:
  - Searcher    — uses SerpClient to find sources
  - Scraper     — uses WebScraperClient for structured data
  - Verifier    — checks source quality + cross-source consistency
  - Synthesizer — calls Claude to produce final answer with citation graph

All agent actions emit signed evidence packets into WebEvidenceTrail.
"""
from .multi_agent import MultiAgentOrchestrator, AgentResponse
from .agents import SearcherAgent, ScraperAgent, VerifierAgent, SynthesizerAgent

__all__ = [
    "MultiAgentOrchestrator",
    "AgentResponse",
    "SearcherAgent",
    "ScraperAgent",
    "VerifierAgent",
    "SynthesizerAgent",
]
