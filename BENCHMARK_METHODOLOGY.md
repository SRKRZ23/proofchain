# PROOFCHAIN — Benchmark Methodology

**Purpose:** Quantified comparison vs AlphaSense + Perplexity to surface PROOFCHAIN's edge in the pitch.

**Headline claim target:**
> *"24× faster than AlphaSense at zero per-seat cost. 100% verified citations vs Perplexity's 70%."*

---

## Test set — 10 equity research questions

These are real questions hedge fund + investment bank analysts ask. Each touches multiple sources, has time-sensitive data, and rewards source-conflict detection.

### Q1. **Customer concentration risk**
> What percentage of TSLA's Q1 2026 revenue came from European markets, and how does that compare to Q1 2025?

### Q2. **Inventory signal**
> Compare Q3 2025 European semiconductor inventory levels at TSMC, Infineon, and STMicroelectronics.

### Q3. **Earnings surprise prep**
> NVDA's data-center revenue Q1 2026 vs analyst consensus guidance — what's the over/under?

### Q4. **Services deceleration**
> Apple Services growth Q1 2026 — what's the analyst consensus and what's the bear case?

### Q5. **Capex signal**
> Microsoft Azure capex 2026 — which suppliers are flagging order growth vs flat orders?

### Q6. **Pre-earnings whisper**
> What are job-posting trends at Snowflake suggesting about Q4 2026 revenue?

### Q7. **Regulatory shock**
> EU Digital Markets Act enforcement actions in Q2 2026 against Meta, Apple, Google — what's been disclosed?

### Q8. **Supply chain risk**
> Tesla Cybertruck production rate Q2 2026 vs original guidance — what do tier-2 suppliers say?

### Q9. **M&A signal**
> Salesforce acquisition rumors Q2 2026 — what filings or executive moves correlate?

### Q10. **ESG bear case**
> ExxonMobil 2026 emissions disclosure — what does the audited report say vs activist filings?

---

## Comparison protocol

### Run 1: PROOFCHAIN
- Submit each question via `POST /api/research/`
- Record: total latency, citation count, source-conflict count, confidence score
- Manually verify citations: how many are correctly attributed vs hallucinated

### Run 2: Perplexity (Sonar API)
- Submit each question via Perplexity API
- Record: total latency, citation count
- Manually verify: how many citations match the actual claim made in the answer

### Run 3: AlphaSense (manual)
- Simulate analyst workflow: log into AlphaSense, search keywords, read top 5 results, synthesize answer
- Record: estimated wall-clock time (use median of 3 trials per question)
- Note: We don't have AlphaSense access for hackathon; use **published benchmarks** + analyst time estimates

---

## Metrics

| Metric | PROOFCHAIN | Perplexity | AlphaSense |
|--------|------------|------------|------------|
| Avg latency per query | _ s | _ s | _ min |
| Citation accuracy | _ % | _ % | _ % |
| Citations per query | _ | _ | _ |
| Cost per query | $0 (open-source) + Bright Data | $20/mo flat | $24K/seat/yr |
| Cryptographic provenance | ✓ Ed25519 | ✗ | ✗ |
| Source-conflict detection | ✓ flagged | ✗ | manual |
| EU AI Act Article 12 export | ✓ built-in | ✗ | ✗ |

---

## Run script

`benchmarks/run_benchmark.py`:

```python
import json, time, httpx
from pathlib import Path

QUESTIONS = json.loads(Path("benchmarks/questions.json").read_text())
RESULTS = []

PROOFCHAIN_URL = "https://api.proofchain.dev/api/research/"
PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"

for q in QUESTIONS:
    # PROOFCHAIN run
    t0 = time.time()
    r = httpx.post(PROOFCHAIN_URL, json={"question": q["text"], "persona": "equity_analyst"})
    pc_latency = (time.time() - t0) * 1000
    pc_data = r.json()

    # Perplexity run
    t0 = time.time()
    r = httpx.post(PERPLEXITY_URL,
        headers={"Authorization": f"Bearer {PERPLEXITY_API_KEY}"},
        json={"model": "sonar-pro", "messages": [{"role": "user", "content": q["text"]}]})
    px_latency = (time.time() - t0) * 1000
    px_data = r.json()

    RESULTS.append({
        "question_id": q["id"],
        "proofchain": {
            "latency_ms": pc_latency,
            "citation_count": len(pc_data["citations"]),
            "confidence": pc_data["confidence"],
            "evidence_chain_length": pc_data["evidence_chain_length"],
        },
        "perplexity": {
            "latency_ms": px_latency,
            "answer_text": px_data["choices"][0]["message"]["content"][:500],
            # manual citation accuracy scored after run
        },
    })

Path("benchmarks/results/run_2026-05-28.json").write_text(json.dumps(RESULTS, indent=2))
print(f"Wrote {len(RESULTS)} results")
```

---

## Chart generation

`benchmarks/generate_chart.py`:

```python
import json
import matplotlib.pyplot as plt
from pathlib import Path

results = json.loads(Path("benchmarks/results/run_2026-05-28.json").read_text())

# Average latency comparison
pc_latencies = [r["proofchain"]["latency_ms"] / 1000 for r in results]
px_latencies = [r["perplexity"]["latency_ms"] / 1000 for r in results]

fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
labels = ["PROOFCHAIN", "Perplexity", "AlphaSense*"]
values = [
    sum(pc_latencies) / len(pc_latencies),
    sum(px_latencies) / len(px_latencies),
    12 * 60,  # 12 min benchmark
]
colors = ["#10b981", "#a1a1aa", "#3f3f46"]

bars = ax.bar(labels, values, color=colors, width=0.5)
ax.set_ylabel("Seconds per query", fontsize=12)
ax.set_title("Average latency: equity research query (n=10)", fontsize=14, weight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for bar, value in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{int(value)}s",
        ha="center", va="bottom", fontsize=11, weight="bold",
    )

ax.text(0.99, 0.01, "*AlphaSense estimate from analyst workflow benchmark",
        transform=ax.transAxes, fontsize=8, ha="right", va="bottom", style="italic")

plt.tight_layout()
plt.savefig("benchmarks/results/latency_comparison.png", dpi=200, bbox_inches="tight")
print("Chart saved.")
```

---

## Honesty principles

When reporting:
- ✅ Say **"based on N=10 questions in benchmarks/questions.json"** — exact sample size
- ✅ Disclose **"AlphaSense estimate from published benchmarks + analyst workflow"** if we don't run live AlphaSense
- ✅ Show **raw JSON results** in repo so judges can verify
- ❌ Don't claim "100% accuracy" if 1 citation slipped — say "9/10 verified"
- ❌ Don't extrapolate to unrelated metrics
- ❌ Don't compare against retired products

If PROOFCHAIN is slower than Perplexity on any query — **acknowledge it in the chart caption**. Trust > spin.

---

## Pre-publication checklist

- [ ] Ran benchmark on May 28 with stable Bright Data API
- [ ] Manually verified citation accuracy (2 hours of manual checks)
- [ ] Generated PNG chart at 200dpi, white background, embedded fonts
- [ ] Wrote one-paragraph summary for video script + slide 7
- [ ] Saved raw JSON to repo for transparency
