"""GET /api/export — full chain export + EU AI Act compliant export."""
from __future__ import annotations

from fastapi import APIRouter

from .research import _orchestrator

router = APIRouter()


@router.get("/full")
def export_full():
    """Full evidence chain — every signed packet ever produced."""
    return _orchestrator.evidence_trail.export()


@router.get("/eu-ai-act")
def export_eu_ai_act(retention_months: int = 6):
    """EU AI Act Article 12 compliant export — filtered by retention policy.

    Default 6-month retention as required by Article 12.
    """
    return _orchestrator.evidence_trail.export_for_eu_ai_act(retention_months=retention_months)
