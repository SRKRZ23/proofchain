# Hacker News Show HN — PROOFCHAIN

**Posting window:** Sun May 31 ~04:00 EDT = ~13:00 UZT (after submission, when US Sunday morning HN audience peaks)
**Account prep:** ensure HN username = `sardorrazikov` (or similar real name), bio has GitHub link, account has ≥1-week history of substantive comments

---

## Submission form

**Title (≤80 chars, "Show HN:" prefix required):**

```
Show HN: PROOFCHAIN — Ed25519 signatures on every web fetch your AI agent makes
```

**URL:**

```
https://github.com/SRKRZ23/PROOFCHAIN
```

---

## First comment (post WITHIN 60 SECONDS of submission)

> Author here. Quick context on what this is and what it isn't.
>
> **What it is:** A cryptographic provenance layer for AI agents on the live web. Every Bright Data fetch (SERP API, Web Scraper, Web Unlocker, Scraping Browser) gets wrapped with an Ed25519 signature + SHA-256 hash chain. Tamper any byte in any packet, the whole chain breaks. Public verification with open key. EU AI Act Article 12 export endpoint built-in (6-month retention).
>
> **What it isn't:** Not the first hash-chain audit log (OrgKernel, Microsoft Agent Mesh, Authora exist). Not a Bright Data replacement (wraps and complements). Not a Cloudflare web-bot-auth replacement (we hash-chain + add content evidence on top of their per-request signing direction).
>
> **Why publish:** EU AI Act Article 12 enforcement starts August 2026. €35M fines. Karpathy's "code is ephemeral" thesis at Sequoia AI Ascent 2026 means evidence is what remains. Cloudflare + Google co-authored IETF web-bot-auth draft-05 in March 2026 — direction is clear but doesn't include hash chains or compliance overlay. That's our wedge.
>
> **Verified, not claimed:**
> - 51/51 tests passing (rANS round-trip, hash-chain integrity stress on 1000 records, tamper detection on every mutation type, full FastAPI endpoint coverage)
> - 10/10 enterprise benchmark questions completed end-to-end
> - 40 evidence packets generated per benchmark, chain verifies
> - Frontend builds clean (Next.js 14, TypeScript 0 errors, 87 KB shared bundle)
>
> **Live demo:** https://proofchain-sardorrazikov-s-projects.vercel.app/demo — equity research analyst persona, ~30 sec per question, hover any citation to see the signed packet.
>
> Stack: FastAPI · PyNaCl (libsodium Ed25519) · Next.js 14 · zstd · Claude Sonnet 4.6 for synthesis. MIT licensed, ~2,400 LOC backend + frontend.
>
> Built solo for the Bright Data Web Data UNLOCKED hackathon (May 25-31, 2026). 8th day of build.
>
> Happy to answer questions on the rANS implementation, the YCbCr-to-Ed25519 evidence packet design, the IETF web-bot-auth alignment trade-off, or anything else.

---

## Engagement velocity rules (first 30 minutes determine HN front-page trajectory)

- Reply to every comment within 5 minutes
- Don't argue defensively — if someone says "Ed25519 + hash chain isn't novel", agree and explain the wedge (compliance overlay + Bright Data integration + EU AI Act export)
- Don't sock-puppet upvote (HN detects geographic clustering, shadowbans)
- Don't post follow-up "we hit the front page!" elsewhere

## Anti-patterns

- ❌ Marketing language ("revolutionary", "game-changing", "AI-powered") → instant downvote on HN
- ❌ Asking for upvotes → instant ban
- ❌ Linking to paywalled landing page → HN respects open access
- ❌ "We're hiring!" mid-thread → wrong forum

## Probability estimates (based on similar Show HN posts)

- Top 30 (front page bottom): 15-25%
- Top 10 (significant visibility): 5-8%
- Top 3 (viral, weeks of attention): 1-3%

Honest framing + working demo + verified numbers → upper end of these ranges.
