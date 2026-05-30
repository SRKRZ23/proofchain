"""PROOFCHAIN FastAPI app — public verification endpoints + research API.

Routes:
  POST /api/research       — submit equity research question, get answer + evidence
  GET  /api/verify/{req}   — verify evidence chain for a request_id (public)
  GET  /api/export         — full chain export (admin)
  GET  /api/export/eu-ai-act — EU AI Act Article 12 compliant export (6-month retention)
  GET  /health             — liveness probe

POST-KICKOFF: Supabase persistence layer + JWT auth + rate limiting.
PRE-KICKOFF: in-memory chain + open endpoints for local dev.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import research, verify, export

app = FastAPI(
    title="PROOFCHAIN API",
    version="0.1.0-alpha",
    description=(
        "Cryptographic audit trail for AI agents on the live web. "
        "Drop-in MCP provenance layer. Every fetch returns content + signed evidence packet."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://proofchain.dev",
        "https://proofchain.vercel.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(research.router, prefix="/api/research", tags=["research"])
app.include_router(verify.router, prefix="/api/verify", tags=["verify"])
app.include_router(export.router, prefix="/api/export", tags=["export"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "proofchain", "version": "0.1.0-alpha"}


@app.get("/")
def root():
    return {
        "service": "PROOFCHAIN",
        "tagline": "Cryptographic audit trail for AI agents on the live web",
        "docs": "/docs",
        "verify_example": "/api/verify/{request_id}",
    }
