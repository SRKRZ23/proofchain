# PROOFCHAIN — 5-Minute Submission Video Script

**Target:** ≤5 minutes, single take preferred, screen recording + voiceover.
**Tools:** Loom / QuickTime / OBS · `assets/PROOFCHAIN_pitch_deck.pdf` as slide source · `https://proofchain-sardorrazikov-s-projects.vercel.app/demo` for live demo

---

## Block 1 — Hook (0:00–0:25, 25 sec)

**Visual:** Slide 1 (hero slide from pitch deck)
**Voiceover:**
> "Karpathy at Sequoia AI Ascent 2026 said code is suddenly free, ephemeral, discardable after one use. Vercel's CEO said 30 percent of apps on their platform now come from agents.
>
> When code disappears, evidence is the only thing that remains. PROOFCHAIN signs every web fetch an AI agent makes, with Ed25519 and a hash chain. Tamper any byte, the chain breaks."

---

## Block 2 — Live demo (0:25–2:00, 95 sec)

**Visual:** Switch to browser, full screen on `https://proofchain-sardorrazikov-s-projects.vercel.app/demo`
**Voiceover:**
> "Equity research analyst persona. I ask: what is TSLA's customer concentration risk in Europe?
>
> Four named agents activate. Searcher hits Bright Data SERP API. Scraper extracts the top 5 sources via Web Unlocker — every fetch wrapped with SHA-256 hash and Ed25519 signature. Verifier cross-checks for conflicts. Synthesizer composes the answer with grounded citations.
>
> Thirty seconds end-to-end. Hover any citation — you see the content hash and signed timestamp. Click Verify Chain — every packet validated, public key shown."

**Screen action:**
1. Click "Try as equity research analyst" CTA
2. Wait for 4-agent animation to complete
3. Hover one citation card to show hash tooltip
4. Click "Verify Chain" button

---

## Block 3 — Architecture (2:00–3:00, 60 sec)

**Visual:** Slide 3 (architecture diagram from pitch deck)
**Voiceover:**
> "PROOFCHAIN wraps four Bright Data products: SERP API, Web Scraper, Web Unlocker, Scraping Browser. Every response becomes an evidence packet — content, URL, SHA-256 hash, timestamp, retrieval method, robots-txt status, Ed25519 signature, prev-hash, sequence number.
>
> Hash-chained — each commits to all previous. Tamper one byte, downstream verification fails. Export endpoint serves EU AI Act Article 12 compliance with six-month retention."

---

## Block 4 — Verified results (3:00–4:00, 60 sec)

**Visual:** Slide 4 (results KPIs from pitch deck)
**Voiceover:**
> "Fifty-one out of fifty-one tests passing. rANS round-trip on random bytes, hash-chain integrity stress test on a thousand records, tamper detection on every mutation type, full API endpoint coverage.
>
> Ten out of ten enterprise benchmark questions completed — TSLA, NVDA, MSFT, Apple, EU DMA, Snowflake. Five citations average per question, point eight two confidence, forty signed evidence packets generated.
>
> Frontend builds clean, zero TypeScript errors. SDKs in Python and JavaScript. MCP server for Claude Desktop and Cursor integration. All MIT licensed, all open source."

---

## Block 5 — Acquihire trajectory (4:00–4:45, 45 sec)

**Visual:** Slide 5 (5-vertical + acquirer landscape from pitch deck)
**Voiceover:**
> "Five verticals, one engine. Flagship is equity research — thirty billion dollar labor waste at AlphaSense scale, four billion comp. Adjacent: AML bank surveillance, regulatory monitoring, vendor risk, publisher provenance.
>
> Acquirer landscape: Bright Data as natural compliance layer for their hundred million daily agents. Cloudflare via IETF web-bot-auth co-authored architecture. AlphaSense or Bloomberg in equity research. Anthropic via MCP provenance gap. RegTech players forced by August 2026 EU AI Act enforcement."

---

## Block 6 — Close (4:45–5:00, 15 sec)

**Visual:** Final slide with CTA URLs
**Voiceover:**
> "PROOFCHAIN. Cryptographic provenance for AI agents on the live web. Demo at proofchain-sardorrazikov-s-projects.vercel.app. Repo at github.com slash SRKRZ23 slash PROOFCHAIN. Sardor Razikov. Thank you."

---

## Recording checklist

- [ ] Browser: Chrome incognito, 1920×1080, no extensions visible
- [ ] Screen recorder: 1080p source, 30fps min
- [ ] Mic: USB condenser if available, otherwise built-in but quiet room
- [ ] Pitch deck open in PDF viewer behind browser tab for fast switching
- [ ] Trial run once for timing
- [ ] Single take preferred — judges value confidence; minor stumbles are OK
- [ ] Export as MP4 H.264, max 100 MB (lablab.ai limit)
- [ ] Upload to Loom (instant share link) OR YouTube unlisted, OR direct upload to lablab.ai form

---

## Backup: 60-second cut (if 5-min feels long)

Drop Block 5 (acquihire) and shorten Block 3 (architecture) to 20 sec. Result: ~3 minutes 30 seconds.
