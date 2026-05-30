# LinkedIn launch post — PROOFCHAIN

**Posting window:** Sun May 31 morning UZT (after submission)
**Length:** ~1,800 chars (LinkedIn sweet spot)
**Carousel images:** banner + architecture + evidence_packet + slide_4_results

---

🔐 **PROOFCHAIN — Cryptographic provenance for AI agents on the live web**

Why this matters in 2026: when code becomes free, ephemeral, and discardable (Karpathy at Sequoia AI Ascent), and 30% of Vercel deployments already come from agents (Guillermo Rauch), the only persistent artifact is **evidence of what your agent actually fetched**.

EU AI Act Article 12 enforcement begins August 2026 — €35M fines or 7% of turnover for high-risk AI systems without tamper-evident audit trails.

I built PROOFCHAIN for the Bright Data Web Data UNLOCKED hackathon to sit at the intersection of three converging forces: throwaway code, IETF web-bot-auth (Cloudflare + Google co-authored, March 2026), and EU AI Act compliance.

**What it does:**
PROOFCHAIN wraps every Bright Data fetch (SERP API, Web Scraper, Unlocker, Scraping Browser) with an Ed25519-signed, SHA-256 hash-chained evidence packet. Each packet commits to the previous one. Tamper any byte → whole chain breaks. Public verification with open key.

**Demo persona:** equity research analyst.
Question: "What is TSLA's customer concentration risk in Europe?"
4 named agents (Searcher / Scraper / Verifier / Synthesizer) activate in ~30 seconds. Hover any citation → SHA-256 hash + Ed25519 signature visible. Click "Verify Chain" → entire evidence trail validated.

**Verified, not claimed:**
✅ 51/51 tests passing (rANS round-trip, hash-chain integrity, 1000-record stress, tamper detection)
✅ 10/10 enterprise benchmark questions completed (TSLA, NVDA, MSFT, Apple, EU DMA, Snowflake, ExxonMobil, Salesforce, Tesla, EU semi)
✅ 40 evidence packets generated, chain verifies end-to-end
✅ MIT licensed, all open source

**Try it:** https://proofchain-sardorrazikov-s-projects.vercel.app/demo
**Repo:** https://github.com/SRKRZ23/PROOFCHAIN
**Pitch deck:** included in repo /assets/

Standards-aligned: IETF web-bot-auth draft-05, RFC 8785 JCS canonicalization, NIST AI RMF, OWASP LLM Top 10.

Built solo, MIT licensed, no Bright Data discount used — just real numbers and a working system.

Feedback welcome.

— Sardor Razikov

#AIagents #BrightData #cryptography #EUAIAct #compliance #opensource

---

## Strategic @-mention plan

3 strategic tags only (not 15). Add at end of post:
- @Pawel Czech (lablab.ai Founder / hackathon judge — public role, judges expect this)
- @Andrea Marazzi (NativelyAI / hackathon judge — same)
- @BrightData (sponsor, technical product reference)

**Do NOT tag:** Vinod Khosla, Sam Altman, Marc Andreessen, or any VCs not previously engaged. Cold-tag conversion rate is <0.1% AND signals "founder doesn't understand outreach" to observers.

---

## Cross-posting

After LinkedIn lands:
1. **X thread** (`marketing/01_x_thread.md`) — 6 tweets, copy banner.png + architecture.png + slide_4_results.png as images
2. **Hacker News Show HN:**
   - Title: `Show HN: PROOFCHAIN — Ed25519 signatures on every web fetch your AI agent makes`
   - URL: github.com/SRKRZ23/PROOFCHAIN
   - First comment: see template in marketing/03_hackernews_show_hn.md
3. **Reddit r/MachineLearning [P]:** same first-comment template, link to repo

Cross-posts NOT simultaneously — space ~2 hours between channels to avoid rate-limit penalties and keep each post fresh in its own algorithm.
