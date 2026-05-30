"""Basic usage example for proofchain-sdk."""
from proofchain import Client, verify_evidence_chain

# 1. Initialize client (uses PROOFCHAIN_API_KEY env var if api_key omitted)
pc = Client(api_key="your-bright-data-key")

# 2. Submit a research question
result = pc.search(
    question="What was NVDA's data-center revenue Q1 2026 vs guidance?",
    persona="equity_analyst",
    num_results=5,
)

# 3. Print the answer + verified citations
print(f"Q: {result.question}")
print(f"A: {result.answer}\n")
print(f"Citations ({len(result.citations)}):")
for c in result.citations:
    status = "✓" if c.verified else "⚠️ conflict"
    print(f"  [{c.rank}] {status} {c.title}")
    print(f"        {c.url}")
    print(f"        hash {c.content_hash[:16]}… · conf {c.confidence:.0%}")

print(f"\nLatency: {result.latency_ms:.0f}ms")
print(f"Chain length: {result.evidence_chain_length}")
print(f"Verify URL: {result.verify_url}")

# 4. Independently verify (no API call — uses public key)
chain = pc.export_chain(eu_ai_act_compliant=True)
report = verify_evidence_chain(chain)
print(f"\nIndependent verification: {report}")
