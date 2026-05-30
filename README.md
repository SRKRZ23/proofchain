# PROOFCHAIN

> **Other AI agents claim citations. PROOFCHAIN signs every one.**

**4 named agents answer your research question in ~30 seconds — every citation Ed25519-signed and publicly verifiable.** No API key needed; anyone can re-verify the chain with our open public key.

**Demo credentials:** `research@acme.com / proof-it` · **Live demo:** [proofchain-sardorrazikov-s-projects.vercel.app/demo](https://proofchain-sardorrazikov-s-projects.vercel.app/demo)

[![Hackathon](https://img.shields.io/badge/Bright_Data-Web_Data_UNLOCKED_2026-blue)](https://lablab.ai/ai-hackathons/brightdata-ai-agents-web-data-hackathon)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![IETF](https://img.shields.io/badge/IETF-web--bot--auth_aligned-orange)](https://datatracker.ietf.org/doc/html/draft-meunier-web-bot-auth-architecture)

---

## ⚡ Try it as an equity research analyst

**Ask:** *"What is TSLA's customer concentration risk in Europe?"*

PROOFCHAIN runs 4 named agents in parallel:
- **Searcher** queries Bright Data SERP API
- **Scraper** extracts content via Bright Data Web Unlocker (5+ sources)
- **Verifier** signs every fetch with Ed25519 + hash-chains to previous
- **Synthesizer** composes answer with grounded citations

**You get:** answer + cryptographically-signed citation graph in ~30 seconds. Hover any citation → see content hash + timestamp. Click "Verify Chain" → public verification endpoint with our open Ed25519 key.

**60-second walkthrough:** see [VIDEO_SCRIPT.md](./VIDEO_SCRIPT.md)

> Equity research analyst is the flagship persona. Same engine ships in AML surveillance, regulatory monitoring, publisher licensing enforcement, and threat intel.

---

## Bright Data Web Data UNLOCKED Hackathon (May 25–31, 2026)

This repository is the **pre-existing open-source library** used during the Bright Data Web Data UNLOCKED hackathon as a foundational dependency. Per lablab.ai Terms of Use Section 16, all submissions must be "original work, open source, and compliant with the MIT License" — this submission meets all three requirements.

**Pre-hackathon foundation (committed before May 25, MIT-licensed):**

- Ed25519 citation chain core (`backend/`)
- Mock-mode Bright Data client interfaces — SERP, Web Scraper API, Web Unlocker, Scraping Browser
- Multi-agent orchestrator skeleton — Searcher / Scraper / Verifier / Synthesizer
- FastAPI server + Next.js demo frontend (hero + 4-agent visualization)
- Python SDK (`sdk-py/`) + JavaScript SDK (`sdk-js/`)
- Supabase schema migrations
- 10 enterprise benchmark questions (`benchmarks/`)
- Architecture and benchmark methodology docs

**Hackathon week (May 25–30) — additive contributions on top of foundation:**

- Live Bright Data integration replacing mock-mode (real $250 credit-backed API calls)
- Multi-source synthesis with real Claude Sonnet 4.6 reasoning
- Production deployment — Railway backend + Vercel frontend at proofchain.dev
- Performance benchmark vs Perplexity baseline (10 enterprise questions, head-to-head)
- 5-minute submission video presentation
- Final whitepaper / pitch deck PDF
- Demo data seeded with 33 verified evidence packets

**Why "library + integration" framing is correct:**

1. ✅ Repo MIT-licensed and publicly committed before hackathon kickoff
2. ✅ Hackathon-week work is substantial new contribution (live BD integration + production deploy + benchmarks + video)
3. ✅ Standard hackathon pattern — judges expect builders to use open-source libraries
4. ✅ Honest disclosure preferred over hiding pre-work (originality judging criterion remains intact)

Judges may verify commit timestamps via `git log` — all pre-hackathon work is timestamped before May 25, 2026 22:00 UZT kickoff.

---

## Three forces converging in 2026

**1. Throwaway code.** Andrej Karpathy (Sequoia AI Ascent 2026): *"code is suddenly free, ephemeral, malleable, discardable after single use."* Guillermo Rauch (Vercel CEO, $340M ARR): *"30% of apps on Vercel already come from agents."* Replit's Amjad Masad: *"the value of all application software will eventually go to zero."* When code disappears, **evidence becomes the only persistent artifact**.

**2. IETF web-bot-auth (draft-05, March 2026).** Cloudflare + Google co-authored the standard that gives every AI bot an Ed25519 keypair and signs every outbound HTTP request via RFC 9421. Amazon, Cloudflare, Akamai, OpenAI all aligned. The direction-of-travel is clear. **The spec doesn't include hash chains, content evidence, or compliance overlay.**

**3. EU AI Act Article 12 enforcement (August 2026).** 6-month minimum log retention. Fines up to €35M / 7% of turnover. Tamper-evident audit trails for high-risk AI systems become **non-optional, regulator-mandated infrastructure**.

PROOFCHAIN sits at the intersection of all three.

---

## What PROOFCHAIN does

PROOFCHAIN wraps every Bright Data fetch — SERP API, Web Scraper API, Web Unlocker, Scraping Browser — with cryptographic provenance:

```json
{
  "content": "...",
  "url": "https://...",
  "sha256_hash": "...",
  "timestamp": "2026-05-30T15:00:00Z",
  "retrieval_method": "BRIGHT_DATA_SERP_API",
  "robots_txt_status": "allowed",
  "ed25519_signature": "...",
  "prev_hash": "...",      // hash-chained to previous packet
  "seq": 42
}
```

Tamper with one packet → entire chain fails verification. Export filtered for EU AI Act Article 12 retention. Sign + verify offline with the public key.

---

## Honest competitive landscape

We are NOT the first Ed25519+hash-chain audit log for AI agents. We are the first **web-fetch-scoped, Bright Data-native, hash-chained + compliance-overlay** implementation. The distinction matters.

| Project | Scope | Hash chain | Live web | Compliance | Bright Data native |
|---------|-------|------------|----------|------------|---------------------|
| [OrgKernel](https://github.com/MetapriseAI/OrgKernel) (MetapriseAI) | Intra-enterprise agent identity | ✅ 3 chains | ❌ no | partial | ❌ no |
| [Microsoft Agent Mesh + IATP](https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/) | Agent-to-agent + plugins | ❌ no spec | ❌ no | ✅ overview | ❌ no |
| [IETF web-bot-auth](https://datatracker.ietf.org/doc/html/draft-meunier-web-bot-auth-architecture) | HTTP request signing | ❌ per-request only | ✅ yes | ❌ no | ❌ generic |
| [Authora](https://authora.dev) | Agent identity + delegation | ❌ no | partial | ❌ no | ❌ no |
| **PROOFCHAIN** | **Agent → live web** | **✅ Ed25519+SHA-256** | **✅ Bright Data** | **✅ EU AI Act Art. 12** | **✅ native** |

See [COMPETITIVE_LANDSCAPE.md](./COMPETITIVE_LANDSCAPE.md) for full analysis.

---

## Anthropic's April 2026 postmortem — the demand signal

Anthropic publicly confessed in their [April 23, 2026 postmortem](https://www.anthropic.com/engineering/april-23-postmortem) that **3 infrastructure bugs broke Claude Code for ~6 weeks** before detection (reasoning effort downgrade, caching bug, verbosity cap). Internal evals + dogfooding failed to reproduce because each bug hit different traffic slices.

**Honest PROOFCHAIN value:** We don't claim we'd have caught Anthropic's bugs — they were server-side model config changes, invisible at the agent→web boundary. We DO claim that **when your model provider can't detect their own regressions for weeks, downstream operators need their own tamper-evident audit trail**. PROOFCHAIN provides exactly that, independent of what the provider logs.

This is a **regulatory/compliance story**, not a "we caught the bug" story.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│   AI Agent (Claude / GPT / Gemini via MCP)                  │
└────────────────────┬────────────────────────────────────────┘
                     │ MCP tool call
                     ▼
┌─────────────────────────────────────────────────────────────┐
│   PROOFCHAIN MCP Server                                      │
│   ├── proofchain.search    (→ SERP API)                     │
│   ├── proofchain.scrape    (→ Web Scraper API)              │
│   ├── proofchain.fetch     (→ Web Unlocker)                 │
│   ├── proofchain.verify    (verify any evidence packet)     │
│   └── proofchain.export    (full chain / EU AI Act export)  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│   Bright Data infrastructure (SERP / Scraper / Unlocker)    │
│   ─────────────────────────────────────────────────────     │
│   Every response wrapped with Ed25519 signature             │
│   Every packet hash-chained to previous (tamper-evident)    │
└─────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for full diagrams.

---

## Quick start

### Python SDK
```bash
pip install proofchain-sdk
```

```python
from proofchain import Client

pc = Client(api_key="your-bright-data-key")
result = pc.search("NVDA Q1 2026 data-center revenue", num_results=5)

for citation in result.citations:
    print(f"[{citation.rank}] {citation.title}")
    print(f"  hash:  {citation.content_hash[:16]}…")
    print(f"  sig:   verified ✓")
```

### JavaScript SDK
```bash
npm install @proofchain/sdk
```

### MCP Server (Claude Desktop / Cursor)
```json
{
  "mcpServers": {
    "proofchain": {
      "command": "npx",
      "args": ["-y", "@proofchain/mcp-server"],
      "env": { "BRIGHT_DATA_API_KEY": "your-key" }
    }
  }
}
```

---

## The five verticals — one engine

PROOFCHAIN is one engine, five vertical applications:

| Vertical | $ Pain | Acquirer comp |
|----------|--------|---------------|
| **Equity research analyst copilot** (flagship) | $30B/yr labor waste · Goldman/MS layoffs | AlphaSense $4B / Harvey $8B (41× ARR) |
| AML / KYC bank surveillance | $3B+ fines on table (TD Bank) | Mastercard ← Recorded Future $2.65B (8.8× rev) |
| Regulatory monitoring | RegTech $14.94B → $107B by 2035 | NAVEX / Diligent / OneTrust |
| Vendor risk (TPCRM) | F500 cascade exposure (Snowflake, Change Healthcare) | Mastercard owns RiskRecon |
| Publisher provenance | NYT v Perplexity (Dec 2025) | Cloudflare AI Labyrinth / Adobe Content Credentials |

Flagship demo = equity research. Platform supports all five. The "model owners" Laurence Moroney (ARM) describes — Forward-Deployed Engineers (Palantir comp $171-415K, +800% LinkedIn growth in 2025) deploying fine-tuned Gemma/Claude in regulated industries — are the primary buyer persona.

---

## Compliance

- **EU AI Act Article 12** — 6-month evidence retention export endpoint built-in. Aug 2026 enforcement deadline.
- **NIST AI RMF** — Govern + Manage functions native.
- **OWASP LLM Top 10** — LLM03 (Training Data Poisoning), LLM06 (Sensitive Info Disclosure), LLM08 (Excessive Agency).
- **IETF web-bot-auth (draft-05) aligned** — hash-chain + content evidence + Bright Data integration extend the IETF direction.

---

## Built on

- **Bright Data** infrastructure (MCP Server, SERP API, Web Scraper API, Web Unlocker, Scraping Browser)
- **Ed25519** signatures via PyNaCl (Libsodium binding)
- **JSON Canonicalization Scheme (JCS)** — RFC 8785 deterministic serialization
- **FastAPI** + **Next.js 14** + **Supabase** + **Vercel** + **Railway**

---

## Acquirer landscape

1. **Bright Data** — natural compliance layer for 100M+ daily agent interactions
2. **Cloudflare** — IETF web-bot-auth co-author Meunier + AI Labyrinth + Workers AI adjacency
3. **AlphaSense / Bloomberg** — equity research vertical strategic
4. **Anthropic** — MCP provenance gap demand signal (April 2026 postmortem)
5. **Specialized RegTech** — NAVEX, Diligent, OneTrust, Saviynt; EU AI Act forcing function

---

## Post-hackathon roadmap

- **Week 1–2:** Engage IETF web-bot-auth working group (post implementation feedback to draft-05)
- **Month 1:** Submit IETF I-D draft "Hash-chain extension to web-bot-auth"
- **Month 1–2:** First design partner (hedge fund / compliance team / publisher)
- **Month 2–3:** Bright Data AI Startup Program onboarding
- **Month 3–6:** Cloudflare engineering engagement (via Meunier + IETF)

---

## Author

**Sardor Razikov** — Independent Researcher ([GitHub](https://github.com/SRKRZ23) · [ORCID](https://orcid.org/0009-0007-0731-4247))

---

## Hackathon submission

**Bright Data Web Data UNLOCKED Hackathon — May 25–31, 2026**

- **Track:** Finance & Market Intelligence (primary) + Security & Compliance (secondary)
- **Team:** [PROOFCHAIN on lablab.ai](https://lablab.ai/ai-hackathons/brightdata-ai-agents-web-data-hackathon/proofchain)

## License

MIT — see [LICENSE](./LICENSE).

## Contact

razikovsardor1@gmail.com · [@SardorRazi99093](https://x.com/SardorRazi99093)
