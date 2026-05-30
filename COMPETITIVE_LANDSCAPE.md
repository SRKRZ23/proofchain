# Competitive Landscape — PROOFCHAIN

**Honest read of every player in the agent-provenance + AI governance space.**

PROOFCHAIN's wedge: **web-fetch-scoped + Bright Data-native + hash-chain + EU AI Act compliance overlay**.

We claim to be FIRST on this specific intersection — not on Ed25519 + agents generally (multiple ship that). The distinction matters when judges or technical reviewers probe.

---

## Direct architectural lookalikes (signing primitives shared, scope different)

### OrgKernel (MetapriseAI) · open-source

- **Repo:** github.com/MetapriseAI/OrgKernel
- **Status:** 965 stars · Apache 2.0 · Phase 1 of 5 complete (80% unbuilt)
- **Scope:** Intra-enterprise agent identity (Org CA → agent certs)
- **Three SHA-256 chains:** Business / Execution / Compliance
- **Stack:** Python 3.10 / FastAPI / SQLAlchemy / PostgreSQL
- **Company:** Metaprise NYC, CEO Richard Swang, ~43 headcount, NO disclosed VC rounds
- **Commercial:** Closed-source AURA platform, Mission-based pricing

**Overlap with PROOFCHAIN:** Ed25519 PKI primitive + hash-chained log.
**Non-overlap:**
- ❌ No live web fetch signing
- ❌ No Bright Data integration
- ❌ MCP gateway planned Phase 3+ (not built)
- ❌ Mission lifecycle Phase 2 (not built)

**Verdict:** Strongest architectural lookalike but **non-substitutable** — different markets.

---

### Microsoft Agent Governance Toolkit (Agent Mesh + IATP) · open-source

- **Released:** April 2, 2026
- **License:** Open source (multi-package: Python/TS/Rust/Go/.NET)
- **Scope:** Agent-to-agent communication + plugin lifecycle
- **Ed25519:** Yes, but bound to agent identity (DIDs), NOT individual web fetches
- **Performance claim:** sub-0.1ms p99
- **Coverage:** All 10 OWASP agentic risks
- **Compliance:** EU AI Act / HIPAA / SOC2 grading
- **MCP:** "Security gateway" mentioned, low detail

**Overlap with PROOFCHAIN:** Ed25519, compliance framing, MCP touch.
**Non-overlap:**
- ❌ No hash chain spec disclosed
- ❌ No outbound HTTP signing (per official architecture deep dive)
- ❌ No web-scraping/Bright Data integration
- ❌ No audit log primitives documented

**Verdict:** Owns agent-to-agent + plugin supply chain. PROOFCHAIN sits **one layer outside** — between agent and live web. **Complementary, not competing.**

---

### Authora Identity · early-stage commercial

- **Site:** authora.dev (currently restricted to scrapers)
- **Stack:** Ed25519 + RBAC + RFC 8693 token-exchange delegation chains
- **SDKs:** TS / Python / Rust / Go
- **Focus:** Agent identity & authorization plane
- **Funding:** No public funding info (bootstrap/early)

**Overlap:** Ed25519 primitive.
**Non-overlap:**
- ❌ No web-fetch provenance
- ❌ No hash chain
- ❌ No live web focus

**Verdict:** Adjacent — identity layer, not evidence layer.

---

## Standards-level direction (NOT a competitor, the direction we ride)

### IETF web-bot-auth — `draft-meunier-web-bot-auth-architecture-05`

- **Released:** March 2026 (current revision 05)
- **Authors:** Thibault Meunier (Cloudflare) + Sandor Major (Google)
- **Aligned:** Amazon, Cloudflare, Akamai, OpenAI
- **Working group:** Chartered early 2026, IETF process ongoing
- **Spec:** Every bot has Ed25519 keypair, publishes JWKS at `/.well-known/http-message-signatures-directory`, signs every outbound HTTP request via RFC 9421 HTTP Message Signatures

**Where PROOFCHAIN extends:**
1. ✅ Hash-chained evidence log (spec only signs per-request)
2. ✅ Response content hashing (spec only signs requests)
3. ✅ EU AI Act Article 12 retention (spec doesn't address compliance)
4. ✅ Source-conflict scoring (multi-fetch synthesis layer)
5. ✅ Bright Data integration (spec is HTTP-generic)

**Strategic implication:**
- The IETF working group is the **right room to be in** post-hackathon
- Submit our own I-D extension draft: "Hash-Chain Extension to web-bot-auth"
- This is **credentialing**, $0 cost, high signal
- Cloudflare (Meunier) = realistic acquirer path

---

## Academic / research projects

### OpenKedge / IEEC (arxiv 2604.08601)

- **Paper:** "Intent-to-Execution Evidence Chain" — Jun He et al., April 2026
- **Status:** Academic protocol paper, no commercial entity visible
- **Scope:** Inside agent reasoning loop (intent / context / policy / execution bounds / outcome)

**Verdict:** Adjacent — inside-agent evidence, not agent→web. Useful as ecosystem-map slide ("they solve intent-reasoning; we solve web-execution").

---

## Vertical / enterprise competitors

### AlphaSense

- **ARR:** $500M (Oct 2025), $4B valuation
- **Pricing:** $24K/seat/year for analysts
- **Recent M&A:** Acquired Tegus $930M (Jul 2024), Carousel (Oct 2025)
- **Differentiator:** Premium content licensing (paywalled financial sources)

**How PROOFCHAIN positions vs AlphaSense:**
- ✅ Open-source SDK at $0 per-seat
- ✅ Cryptographic citations (AlphaSense has source attribution but no signatures)
- ✅ EU AI Act Article 12 export (AlphaSense not native)
- ❌ Premium content access (AlphaSense has licensing deals we don't replicate)

**Verdict:** Not head-on competition for equity research seats. PROOFCHAIN is the **trustless layer** — analysts use both: AlphaSense for premium licensed content, PROOFCHAIN for verified open-web synthesis.

### Tavily

- **Acquired:** Nebius $275M (Feb 2026)
- **Scope:** Agent-native search
- **No provenance layer**

### Exa.ai

- **Valuation:** $2.2B (May 2026)
- **Scope:** Agent search
- **No provenance layer**

### Parallel Web Systems

- **Valuation:** $2B (Apr 2026, Sequoia)
- **Scope:** Web infrastructure for AI agents
- **Founder:** Parag Agrawal
- **No provenance layer**

**Verdict for Tavily/Exa/Parallel:** All compete in **agent search/web infra**. PROOFCHAIN is **provenance layer ABOVE search**. Could integrate into any of them.

---

## Threat intelligence / compliance comparables

### Recorded Future

- **Acquired:** Mastercard $2.65B (Sept 2024, 8.8× revenue)
- **Scope:** Threat intel aggregation
- **No cryptographic provenance**

### BlackKite / RiskRecon / UpGuard

- **Scope:** Third-party risk management
- **Recent M&A:** Mastercard owns RiskRecon

### NAVEX / Diligent / OneTrust

- **Scope:** Compliance / governance / RegTech
- **Mature category, PE rollups**

**Verdict:** PROOFCHAIN doesn't compete with these directly — they're enterprise sales motion. PROOFCHAIN is **infrastructure THEY would integrate** for cryptographic evidence.

---

## PROOFCHAIN's claimed wedge (must defend in pitch)

**1st of its kind on this specific intersection:**

```
                    Live web actions
                          ▲
                          │
        OrgKernel ──────┼────── IETF web-bot-auth
       (intra-enterprise)│       (signs requests, no chain)
                          │
                          │ ◄── PROOFCHAIN
       Microsoft IATP ───┤      (web + chain + Bright Data + compliance)
       (agent-to-agent)   │
                          ▼
                    Intra-enterprise actions
```

**Defensible claims:**
- ✅ First hash-chained provenance on live web fetches
- ✅ First Bright Data-native MCP provenance layer
- ✅ First EU AI Act Article 12 export endpoint for web evidence

**Indefensible claims (we DON'T make):**
- ❌ "First Ed25519+chain for AI agents" (OrgKernel ships this)
- ❌ "Replaces Anthropic's audit infrastructure" (we extend downstream)
- ❌ "Solves AI hallucination" (we provide source verification, not factual truth)
- ❌ "End of citation lawsuits" (we provide evidence, courts decide)

---

## Risk register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| OrgKernel claims they cover our space | Medium | Medium | Explicit scope diff in deck slide |
| Microsoft expands IATP to web signing | Medium | High | Move fast on IETF working group |
| Cloudflare/Google build PROOFCHAIN internally | High | High | First-mover + open source community |
| Bright Data ships own audit layer | Medium | High | Acquihire conversation early (Startup Program) |
| AlphaSense launches free tier | Low | Medium | We're not direct competitor |
| EU AI Act Article 12 extended/weakened | Low | High | Hedge with NIST AI RMF + OWASP framings |

---

## Bottom line

PROOFCHAIN is **NOT a unique invention**. PROOFCHAIN is **the right composition of proven primitives at the right time on the right platform (Bright Data) for the right regulatory moment (EU AI Act Aug 2026)**.

Composition wins. Components don't.

This is the honest, defensible pitch.
