"""GET /api/verify/{request_id} — public verification endpoint.

Anyone can verify that an evidence chain was produced by PROOFCHAIN.
Used by the frontend to show green checkmarks next to citations.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .research import _orchestrator

router = APIRouter()


@router.get("/{request_id}")
def verify_request(request_id: str):
    """Verify all evidence packets associated with a request_id."""
    chain = _orchestrator.evidence_trail._chain
    records_for_request = [
        r for r in chain.records()
        if r.entry.get("request_id") == request_id
    ]
    if not records_for_request:
        raise HTTPException(status_code=404, detail="request_id not found in chain")

    return {
        "request_id": request_id,
        "verified": chain.verify_chain(),
        "record_count": len(records_for_request),
        "verify_key_public": chain.verify_key_hex,
        "records": [r.to_dict() for r in records_for_request],
    }


@router.get("/")
def verify_status():
    """Whole-chain verification status."""
    chain = _orchestrator.evidence_trail._chain
    return {
        "service": "proofchain-verify",
        "chain_length": len(chain.records()),
        "chain_valid": chain.verify_chain(),
        "verify_key_public": chain.verify_key_hex,
    }
