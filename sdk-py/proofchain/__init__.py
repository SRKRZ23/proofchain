"""proofchain-sdk — Python client for PROOFCHAIN verified web data.

Quick start:
    from proofchain import Client
    pc = Client(api_key="your-bright-data-key")
    result = pc.search("NVDA Q1 2026 revenue", num_results=5)
    for c in result.citations:
        print(c.title, c.url, c.verified)
"""
from .client import Client, ResearchResult, Citation
from .verify import verify_evidence_chain

__all__ = ["Client", "ResearchResult", "Citation", "verify_evidence_chain"]
__version__ = "0.1.0a1"
