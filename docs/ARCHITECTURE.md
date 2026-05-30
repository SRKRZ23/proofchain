# PROOFCHAIN Architecture

**Hackathon:** Web Data UNLOCKED — Bright Data AI Agents Hackathon
**Track:** 3 (Security & Compliance / Infrastructure)
**Submission window:** May 25 – May 31, 2026 (Sun 05:00 UZT deadline)
**License:** Apache 2.0
**Position:** Cryptographic provenance layer wrapping Bright Data API calls.

---

## The problem

AI agents fetch real-time web data through Bright Data and other infrastructure providers. The fetched content flows into LLM context, business decisions, regulatory reports, and customer-facing outputs — but there is no tamper-evident audit trail. Enterprise compliance teams cannot prove:

- What URL was fetched
- When it was fetched
- What zone / proxy / configuration was used
- That the content arriving in the AI agent matches what Bright Data actually returned

In a regulated environment (GDPR data sourcing, SEC reporting, FDA compliance, internal SOX controls), undocumented AI fetches are a quietly mounting risk.

## The solution

PROOFCHAIN wraps every Bright Data API call with a deterministic Ed25519 signing step. Each fetch returns the original content **plus** a signed evidence packet that downstream auditors can verify with a published public key.

```
┌─────────────────┐        ┌──────────────────┐
│  AI Agent /     │        │  Bright Data     │
│  Orchestrator   │        │  MCP / SERP /    │
│  (Claude,       │        │  Web Unlocker /  │
│   Featherless,  │        │  Scraping Browser│
│   gpt-oss, …)   │        └────────┬─────────┘
└────────┬────────┘                 │
         │                          │
         ▼                          │
┌──────────────────┐                │
│   PROOFCHAIN     │◄───────────────┘
│   wrapper        │   raw content +
│  (this repo)     │   BD metadata
└────────┬─────────┘
         │
         │   { content,
         │     signature (Ed25519),
         │     evidence_packet {
         │       content_hash,
         │       bd_metadata { zone, url, request_id, ts },
         │       timestamp_ms,
         │       audit_chain_id,
         │       proofchain_version,
         │     },
         │     public_key }
         ▼
┌──────────────────┐
│  Auditor /       │
│  Compliance      │
│  Replay & verify │
└──────────────────┘
```

## Components

### 1. `proofchain.signing` — Ed25519 layer
- Wraps libsodium (PyNaCl) Ed25519 primitives
- `ProofChainSigner` accepts ephemeral or persistent private key
- Signs a canonical JSON serialization of the evidence packet
- `verify_signed_response()` is a stateless function — any party with the public key can independently verify

### 2. `proofchain.bd_wrapper` — Bright Data integration
- `BrightDataProofChainClient` exposes `search_web()` and `scrape_url()`
- Routes to Bright Data REST endpoint (`api.brightdata.com/request`)
- Supports SERP API and Web Unlocker zones
- Auto-attaches PROOFCHAIN signatures to every response
- Mock mode (`mock_mode=True`) returns synthetic responses for local development before account approval

### 3. `proofchain.audit_chain` — chained provenance (planned Day 2)
- Hash-chains successive fetches so that an entire research session can be verified end-to-end
- Each new fetch references the previous audit_chain_id via Merkle-style linking

### 4. MCP server (planned Day 3)
- Exposes PROOFCHAIN as drop-in MCP server
- Compatible with Claude Desktop / Cursor / Continue.dev / Zed
- Tools: `search_web`, `scrape_url`, `verify_audit_packet`

## Evidence packet schema

```json
{
  "content_hash": "<sha256(content) hex>",
  "bd_metadata": {
    "zone": "mcp_unlocker",
    "url": "https://example.com",
    "request_id": "...",
    "response_format": "raw"
  },
  "timestamp_ms": 1779730000123,
  "audit_chain_id": "<uuid v4>",
  "proofchain_version": "0.1.0"
}
```

Canonical serialization (sorted keys, no whitespace) is the byte sequence actually signed.

## Verification flow

1. Auditor receives `{ content, signature, evidence_packet, public_key }`.
2. Recomputes `sha256(content)` → compares to `evidence_packet.content_hash`. If mismatch → reject.
3. Reconstructs canonical JSON of `evidence_packet` → bytes.
4. Verifies Ed25519 signature against bytes using `public_key`. If valid → accept.

Both checks must pass for the packet to be considered authentic.

## Day-by-day build plan

| Day | Date | Deliverable |
|-----|------|-------------|
| 0.5 | Mon May 25 evening | Scaffold + Ed25519 signing module + BD wrapper skeleton + mock mode |
| 1 | Tue May 26 | Real Bright Data API integration (pending account approval), end-to-end demo |
| 2 | Wed May 27 | Audit chain (Merkle-style linking), `verify_audit_packet` API |
| 3 | Thu May 28 | MCP server interface, deploy to Vercel/Railway |
| 4 | Fri May 29 | Video script + first take + README polish |
| 5 | Sat May 30 | Final video, end-to-end demo run, integration tests |
| Submit | Sun May 31 05:00 UZT | Submit to lablab.ai form (description + video + GitHub link) |

## Non-goals

- Not a Bright Data replacement — it wraps and complements
- Not a Track 1 research agent — it's the infrastructure layer underneath
- Not a managed service — it's a self-hosted middleware library

## License & attribution

Apache 2.0. Built using Bright Data's open-source `brightdata/skills` repository as the integration baseline reference. All Bright Data trademarks belong to Bright Data Ltd.

## Hackathon disclosure

PROOFCHAIN existed as an MIT open-source library before May 25, 2026. During the Web Data UNLOCKED hackathon (May 25 – May 31, 2026), the Bright Data integration layer (`bd_wrapper.py`), the MCP server interface, and the demo video are being newly authored. See README disclosure section for full chronology.
