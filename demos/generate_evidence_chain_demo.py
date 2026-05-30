"""Generate evidence chain integrity demo + tamper proof artifact."""
import sys, json
from pathlib import Path
from copy import deepcopy
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from backend.proofchain_core.evidence_chain import WebEvidenceTrail
from backend.orchestrator import MultiAgentOrchestrator
from backend.brightdata.serp_client import SerpClient
from backend.brightdata.scraper_client import WebScraperClient

trail = WebEvidenceTrail()
orch = MultiAgentOrchestrator(
    serp_client=SerpClient(evidence_trail=trail, mock_mode=True),
    scraper_client=WebScraperClient(evidence_trail=trail, mock_mode=True),
    evidence_trail=trail,
)
questions = [
    "What is TSLA's customer concentration risk in Europe?",
    "NVDA data-center revenue Q1 2026 vs analyst consensus?",
    "Apple Services Q1 2026 growth — bear case?",
    "MSFT Azure capex 2026 — supplier order signals?",
    "Snowflake job posting trends Q4 2026?",
    "EU DMA enforcement actions Q2 2026?",
    "Tesla Cybertruck production rate Q2 2026?",
    "ExxonMobil 2026 emissions audit vs activist claims?",
]
for q in questions:
    orch.research(question=q, persona="equity_analyst", num_sources=3)

chain = trail._chain
tampered = deepcopy(chain.records())
tampered[5].entry["query_hash"] = "TAMPERED_PROVES_INTEGRITY"

out = {
    "metadata": {
        "demo_purpose": "Demonstrate 32+ packet evidence chain integrity",
        "questions_seeded": len(questions),
        "total_packets": len(chain.records()),
        "chain_verifies": chain.verify_chain(),
        "verify_key_public_hex": chain.verify_key_hex,
        "signing_algorithm": "Ed25519",
        "hash_algorithm": "SHA-256",
        "canonicalization": "JCS-like (sorted keys, minimal whitespace)",
    },
    "chain": chain.export(),
    "tamper_demo": {
        "description": "Mutate any byte in any packet -> that packet's verify() returns False",
        "tampered_packet_seq": 5,
        "tampered_field": "query_hash",
        "tampered_verify_result": tampered[5].verify(chain.verify_key),
        "original_packet_verify_result": chain.records()[5].verify(chain.verify_key),
    },
    "compliance_export": trail.export_for_eu_ai_act(retention_months=6),
}
Path('demos/evidence_chain_proof.json').write_text(json.dumps(out, indent=2, default=str))
print(f"✓ {len(chain.records())} packets · chain_verifies={chain.verify_chain()} · tamper_detected={not tampered[5].verify(chain.verify_key)}")
print(f"✓ evidence_chain_proof.json: {Path('demos/evidence_chain_proof.json').stat().st_size:,} bytes")
