# PROOFCHAIN — Submission Cheat Sheet

**Hackathon:** Bright Data Web Data UNLOCKED · May 25–31, 2026
**Submission deadline:** Sun May 31, 04:00 UZT (= Sat May 30, 23:00 UTC = Sat 19:00 EDT)
**Submit at:** https://lablab.ai/ai-hackathons/brightdata-ai-agents-web-data-hackathon/proofchain

---

## 📋 Lablab.ai submission form — copy/paste ready

| Field | Value |
|---|---|
| **Project Title** | `PROOFCHAIN` |
| **Tagline** | `Other AI agents claim citations. PROOFCHAIN signs every one.` |
| **Short Description (200 chars)** | `Cryptographic provenance for AI agents on the live web. Ed25519-signed, hash-chained evidence for every Bright Data fetch. EU AI Act Article 12 compliant. MIT licensed.` |
| **Long Description** | Paste full README.md |
| **Track (primary)** | `Finance & Market Intelligence` |
| **Track (secondary)** | `Security & Compliance` |
| **Tags** | `bright-data, ed25519, hash-chain, mcp, eu-ai-act, fastapi, nextjs, anthropic-claude, provenance, ai-agents` |
| **Cover Image** | Upload `assets/banner.png` (157 KB, 1920×1080) |
| **Demo URL** | `https://proofchain-sardorrazikov-s-projects.vercel.app/demo` |
| **GitHub Repository** | `https://github.com/SRKRZ23/PROOFCHAIN` |
| **Pitch Deck** | Upload `assets/PROOFCHAIN_pitch_deck.pdf` (287 KB, 5 slides) |
| **Video URL** | (insert your Loom / YouTube unlisted URL after recording) |

---

## ✅ Verified-status snapshot

| Aspect | Status | Evidence |
|---|---|---|
| Tests | **51/51 PASS** | `python3 -m pytest tests/ backend/tests/ -v` |
| Benchmark | **10/10 OK** | `benchmarks/results/benchmark_mock_*.json` |
| Evidence chain integrity | **32 packets · chain verifies · tamper detected** | `demos/evidence_chain_proof.json` (47 KB) |
| Frontend build | **clean, 5 pages, TypeScript 0 errors** | `cd frontend && npm run build` |
| Live demo URL | **HTTP 200, public, no auth gate** | `curl -sI https://proofchain-sardorrazikov-s-projects.vercel.app/demo` |
| GitHub repo | **public, MIT, 95 files** | https://github.com/SRKRZ23/PROOFCHAIN |
| Visual assets | **logo + banner + architecture + 5 slides + pitch_deck.pdf + full_deck.pdf + social_card** | `assets/` |
| Author attribution | **Sardor Razikov only (no co-authors)** | `git log -1 --format='%an <%ae>%n%(trailers)'` |
| Zero data leaks | **no Tashkent/Korea/Suh/ecosystem-cross-refs** | `grep -ri` audit script in this file below |

---

## 🚀 Live URLs

| Resource | URL |
|---|---|
| **Demo (live)** | https://proofchain-sardorrazikov-s-projects.vercel.app/demo |
| **Hero (live)** | https://proofchain-sardorrazikov-s-projects.vercel.app |
| **Repo (public)** | https://github.com/SRKRZ23/PROOFCHAIN |
| **Vercel project** | https://vercel.com/sardorrazikov-s-projects/proofchain |
| **Backend** | NOT YET DEPLOYED (Railway login required — see manual checklist) |

---

## 📦 Marketing/launch assets ready

| Channel | File | Action |
|---|---|---|
| X / Twitter thread | `marketing/01_x_thread.md` | 6 tweets, copy 4 images as you go |
| LinkedIn post | `marketing/02_linkedin_post.md` | ~1,800 chars, carousel with 4 images |
| Hacker News Show HN | `marketing/03_hackernews_show_hn.md` | Submit + first comment within 60s |
| Video script | `VIDEO_SCRIPT.md` | 5-minute outline, 6 blocks |

---

## 🔁 Reproducibility check (anyone can run)

```bash
git clone https://github.com/SRKRZ23/PROOFCHAIN.git
cd PROOFCHAIN

# Backend deps
pip install -r backend/requirements.txt pytest

# Run all tests (expected: 51 passed)
python3 -m pytest tests/ backend/tests/ -v

# Run benchmark (mock mode, no API keys needed)
python3 benchmarks/run_benchmark.py

# Generate fresh evidence chain proof
python3 demos/generate_evidence_chain_demo.py

# Build frontend
cd frontend && npm install && npm run build
```

---

## 🧹 Last verified leak audit

```bash
cd /Users/sardorrazikov1/Alish/proofchain
grep -ri -E "naechim|olimkhuja|k-grand|kickstarter|prof suh|stephen kimoi|drysdale|yichen|ben cera|emmanuel iriarte|tevin|szilvi|malini|UCAR|KUSE|KOICA|Soonchunhyang|tashkent|uzbekistan|REPOMIND|FORGE|CITADEL|SOUF AI|TRIAGEGUARD|TriageGuard|NAECHIM|\bATLAS\b" \
  --include="*.md" --include="*.py" --include="*.yaml" --include="*.tsx" --include="*.ts" --include="*.js" \
  --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=.next .
```
→ Expected output: **(empty)**.

---

## 🎯 Final submission timing

| Time (UZT) | Action |
|---|---|
| **NOW → 03:00** | Record + upload 5-minute video (use VIDEO_SCRIPT.md) |
| **02:30 → 03:00** | Open lablab.ai submission form, paste all fields above |
| **03:00 → 03:30** | Review form 2× before submit |
| **03:30** | **SUBMIT** on lablab.ai |
| **03:45** | Confirm submission visible at hackathon team page |
| **Post-submit** | Sleep 6+ hours before launch posts |
| **Sun 09:00 UZT** | LinkedIn post (marketing/02) |
| **Sun 11:00 UZT** | X thread (marketing/01) |
| **Sun 13:00 UZT (= US Sun 04:00 EDT)** | Hacker News Show HN (marketing/03) |

---

## ⚠️ DO NOT do

- ❌ Submit before 02:00 UZT (you lose polish window)
- ❌ Push `.env` (it has API keys — gitignored, safe)
- ❌ Tag VCs in launch posts (cold-tag conversion <0.1%)
- ❌ Force-push to main on GitHub (breaks judge git verification)
- ❌ Re-add NAECHIM/Olimkhuja/Korea/Suh mentions anywhere
