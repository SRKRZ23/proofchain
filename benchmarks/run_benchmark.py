"""PROOFCHAIN benchmark runner — 10 enterprise questions end-to-end.

Measures:
  - Total latency per question (search + scrape + verify + synthesize)
  - Evidence packets generated per question
  - Chain integrity (whole-chain Ed25519 verification)
  - Citation coverage (sources cited per answer)
  - Cryptographic provenance: every citation has SHA-256 + Ed25519 signature

Runs in mock mode by default (no live API calls). For live BD mode set
BRIGHT_DATA_API_KEY env var and pass --live.

Output: benchmarks/results/benchmark_<timestamp>.json + summary table on stdout.
"""
from __future__ import annotations

import json
import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from backend.orchestrator import MultiAgentOrchestrator
from backend.brightdata.serp_client import SerpClient
from backend.brightdata.scraper_client import WebScraperClient
from backend.proofchain_core.evidence_chain import WebEvidenceTrail


def load_questions(path: Path) -> list[dict]:
    with open(path) as f:
        return json.load(f)


def run_benchmark(questions: list[dict], live: bool = False) -> dict:
    """Run all questions through orchestrator. Returns aggregate metrics."""
    trail = WebEvidenceTrail()
    serp = SerpClient(evidence_trail=trail, mock_mode=not live)
    scraper = WebScraperClient(evidence_trail=trail, mock_mode=not live)
    orch = MultiAgentOrchestrator(
        serp_client=serp,
        scraper_client=scraper,
        evidence_trail=trail,
    )

    per_question = []
    t_global_start = time.perf_counter()

    for i, q in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] {q['id']}")
        print(f"  Category: {q['category']}")
        print(f"  Question: {q['text'][:80]}...")

        t0 = time.perf_counter()
        try:
            response = orch.research(
                question=q["text"],
                persona="equity_analyst",
                num_sources=5,
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000
            d = response.to_dict()
            per_question.append({
                "question_id": q["id"],
                "category": q["category"],
                "latency_ms": round(elapsed_ms, 2),
                "request_id": d["request_id"],
                "citations_count": len(d["citations"]),
                "confidence": d["confidence"],
                "answer_length_chars": len(d["answer"]),
                "evidence_chain_length_after": d["evidence_chain_length"],
                "source_conflicts": len(d["source_conflicts"]),
                "verify_url": d["verify_url"],
                "status": "OK",
            })
            print(f"  → {len(d['citations'])} citations, {elapsed_ms:.0f}ms, "
                  f"chain_len={d['evidence_chain_length']}, conf={d['confidence']:.2f}")
        except Exception as e:
            per_question.append({
                "question_id": q["id"],
                "category": q["category"],
                "status": "ERROR",
                "error": str(e),
            })
            print(f"  → ERROR: {e}")

    t_global = (time.perf_counter() - t_global_start) * 1000

    # Aggregate metrics
    ok = [r for r in per_question if r["status"] == "OK"]
    chain_records = trail._chain.records()
    chain_verifies = trail.verify()

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "live" if live else "mock",
        "total_questions": len(questions),
        "successful": len(ok),
        "failed": len(per_question) - len(ok),
        "total_runtime_ms": round(t_global, 2),
        "avg_question_latency_ms": round(sum(r["latency_ms"] for r in ok) / max(1, len(ok)), 2),
        "avg_citations_per_question": round(sum(r["citations_count"] for r in ok) / max(1, len(ok)), 2),
        "avg_confidence": round(sum(r["confidence"] for r in ok) / max(1, len(ok)), 3),
        "total_evidence_packets_generated": len(chain_records),
        "chain_integrity_verified": chain_verifies,
        "verify_key_public_hex": trail._chain.verify_key_hex,
        "per_question": per_question,
    }
    return summary


def print_summary_table(summary: dict) -> None:
    print()
    print("=" * 75)
    print("PROOFCHAIN Benchmark — Summary")
    print("=" * 75)
    print(f"Mode:                              {summary['mode']}")
    print(f"Timestamp:                         {summary['timestamp']}")
    print(f"Questions attempted:               {summary['total_questions']}")
    print(f"Successful:                        {summary['successful']}")
    print(f"Failed:                            {summary['failed']}")
    print(f"Total runtime:                     {summary['total_runtime_ms']:.0f} ms "
          f"({summary['total_runtime_ms']/1000:.1f} s)")
    print(f"Avg per-question latency:          {summary['avg_question_latency_ms']:.0f} ms")
    print(f"Avg citations per question:        {summary['avg_citations_per_question']:.1f}")
    print(f"Avg synthesizer confidence:        {summary['avg_confidence']:.3f}")
    print(f"Total evidence packets generated:  {summary['total_evidence_packets_generated']}")
    print(f"Chain integrity verified:          {'✓ YES' if summary['chain_integrity_verified'] else '✗ NO'}")
    print(f"Verify key (public, Ed25519 hex):  {summary['verify_key_public_hex'][:32]}...")
    print()
    print("Per-question breakdown:")
    print(f"{'#':<3} {'ID':<35} {'Latency':>10} {'Cites':>6} {'Conf':>6} {'Status':>8}")
    print("-" * 75)
    for i, r in enumerate(summary["per_question"], 1):
        if r["status"] == "OK":
            print(f"{i:<3} {r['question_id']:<35} {r['latency_ms']:>9.0f}ms "
                  f"{r['citations_count']:>6} {r['confidence']:>6.2f} {r['status']:>8}")
        else:
            print(f"{i:<3} {r['question_id']:<35} {'N/A':>10} {'-':>6} {'-':>6} {r['status']:>8}")
    print("=" * 75)
    print()


def main():
    parser = argparse.ArgumentParser(description="PROOFCHAIN benchmark runner")
    parser.add_argument("--live", action="store_true", help="Run against live Bright Data API (requires keys)")
    parser.add_argument("--questions-file", default="benchmarks/questions.json",
                        help="Path to questions JSON")
    args = parser.parse_args()

    questions_path = ROOT / args.questions_file
    print(f"Loading questions from: {questions_path}")
    questions = load_questions(questions_path)
    print(f"Loaded {len(questions)} questions.")

    summary = run_benchmark(questions, live=args.live)
    print_summary_table(summary)

    # Save results
    results_dir = ROOT / "benchmarks" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = results_dir / f"benchmark_{summary['mode']}_{ts}.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to: {out_path}")


if __name__ == "__main__":
    main()
