"""POST /api/research — submit research question, get answer + signed evidence chain."""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from ...orchestrator import MultiAgentOrchestrator

router = APIRouter()

# Singleton orchestrator (in-memory chain — POST-KICKOFF: replace with per-user Supabase store)
_orchestrator = MultiAgentOrchestrator()


class ResearchRequest(BaseModel):
    question: str
    persona: str = "equity_analyst"
    num_sources: int = 5


class ResearchResponse(BaseModel):
    request_id: str
    question: str
    answer: str
    citations: list
    confidence: float
    latency_ms: float
    source_conflicts: list
    evidence_chain_length: int
    verify_url: str


@router.post("/", response_model=ResearchResponse)
def submit_research(req: ResearchRequest):
    response = _orchestrator.research(
        question=req.question,
        persona=req.persona,
        num_sources=req.num_sources,
    )
    return ResearchResponse(**response.to_dict())


@router.get("/orchestrator/stats")
def orchestrator_stats():
    """Internal: chain length, verify status."""
    chain = _orchestrator.evidence_trail._chain
    return {
        "total_records": len(chain.records()),
        "chain_valid": chain.verify_chain(),
        "verify_key_public": chain.verify_key_hex,
    }
