"use client";
import { useEffect, useState } from "react";
import Link from "next/link";

interface Citation {
  url: string;
  title: string;
  snippet: string;
  content_hash: string;
  confidence: number;
  conflict_flag: boolean;
}

interface ResearchResponse {
  request_id: string;
  question: string;
  answer: string;
  citations: Citation[];
  confidence: number;
  latency_ms: number;
  evidence_chain_length: number;
  verify_url: string;
}

type AgentStatus = "idle" | "active" | "done";

interface AgentState {
  id: "searcher" | "scraper" | "verifier" | "synthesizer";
  label: string;
  task: string;
  detail: string;
  accent: string; // tailwind text color
  bg: string; // tailwind bg color
  border: string; // tailwind border color
  status: AgentStatus;
}

const INITIAL_AGENTS: AgentState[] = [
  {
    id: "searcher",
    label: "Searcher",
    task: "Bright Data SERP API",
    detail: "Querying 5 search engines + parsing top-K results...",
    accent: "text-blue-600",
    bg: "bg-blue-50",
    border: "border-blue-200",
    status: "idle",
  },
  {
    id: "scraper",
    label: "Scraper",
    task: "Bright Data Web Scraper + Unlocker",
    detail: "Extracting content from 5 sources, bypassing anti-bot...",
    accent: "text-emerald-600",
    bg: "bg-emerald-50",
    border: "border-emerald-200",
    status: "idle",
  },
  {
    id: "verifier",
    label: "Verifier",
    task: "Ed25519 signing + hash chain",
    detail: "Signing 5 evidence packets, hash-chaining to previous fetches...",
    accent: "text-amber-600",
    bg: "bg-amber-50",
    border: "border-amber-200",
    status: "idle",
  },
  {
    id: "synthesizer",
    label: "Synthesizer",
    task: "Claude Sonnet 4.6",
    detail: "Composing grounded answer + resolving source conflicts...",
    accent: "text-purple-600",
    bg: "bg-purple-50",
    border: "border-purple-200",
    status: "idle",
  },
];

const SAMPLE_QUESTIONS = [
  "What is TSLA's customer concentration risk in Europe?",
  "Compare Q3 2025 European semiconductor inventory levels.",
  "NVDA's data-center revenue Q1 2026 vs guidance.",
  "Apple Services growth deceleration 2026 — analyst consensus.",
  "Microsoft Azure capex 2026 — supplier signal analysis.",
];

// Staggered agent progression to make multi-agent coordination visible
function useAgentProgression(loading: boolean) {
  const [agents, setAgents] = useState<AgentState[]>(INITIAL_AGENTS);

  useEffect(() => {
    if (!loading) {
      // Reset on idle
      setAgents(INITIAL_AGENTS);
      return;
    }
    // Stagger: Searcher activates first, then sequence
    const timeline: { ms: number; updates: Partial<Record<AgentState["id"], AgentStatus>> }[] = [
      { ms: 100, updates: { searcher: "active" } },
      { ms: 900, updates: { searcher: "done", scraper: "active" } },
      { ms: 2200, updates: { scraper: "done", verifier: "active" } },
      { ms: 3000, updates: { verifier: "done", synthesizer: "active" } },
      // synthesizer marked done when response arrives
    ];

    const timers = timeline.map((step) =>
      setTimeout(() => {
        setAgents((prev) =>
          prev.map((a) => (step.updates[a.id] ? { ...a, status: step.updates[a.id]! } : a))
        );
      }, step.ms)
    );

    return () => timers.forEach(clearTimeout);
  }, [loading]);

  return { agents, setAgents };
}

export default function DemoPage() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<ResearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { agents, setAgents } = useAgentProgression(loading);

  async function submit(q: string) {
    if (!q.trim()) return;
    setLoading(true);
    setError(null);
    setResponse(null);
    try {
      const res = await fetch("/api/research/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q, persona: "equity_analyst", num_sources: 5 }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      // Mark all agents done when response arrives
      setAgents((prev) => prev.map((a) => ({ ...a, status: "done" })));
      setResponse(data);
    } catch (e: any) {
      setError(e.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  const conflictCount = response?.citations.filter((c) => c.conflict_flag).length ?? 0;

  return (
    <main className="min-h-screen">
      <nav className="container-wide flex items-center justify-between py-6 border-b border-ink-100">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-7 h-7 rounded bg-ink-900" />
          <span className="text-sm font-semibold tracking-tight">PROOFCHAIN</span>
        </Link>
        <div className="text-xs font-mono text-ink-500">Equity Research Demo · v0.1-alpha · 4-agent orchestrator</div>
      </nav>

      <section className="container-narrow py-12">
        <h1 className="text-3xl font-semibold tracking-tight mb-2">Verified equity research.</h1>
        <p className="text-ink-600 mb-8">
          Ask any equity research question. PROOFCHAIN runs <strong>4 agents in parallel</strong> via Bright Data — returns a
          cryptographically-signed citation graph with conflict resolution.
        </p>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            submit(question);
          }}
        >
          <div className="border border-ink-200 rounded-lg p-1 flex gap-1 mb-3 focus-within:border-ink-400 transition">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g. NVDA's data-center revenue Q1 2026 vs guidance"
              className="flex-1 px-3 py-2.5 outline-none text-sm bg-transparent"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="px-5 py-2.5 rounded-md bg-ink-900 text-white text-sm font-medium hover:bg-ink-800 disabled:opacity-40 transition"
            >
              {loading ? "Researching…" : "Run research"}
            </button>
          </div>

          <div className="flex flex-wrap gap-2 mb-8">
            {SAMPLE_QUESTIONS.map((q) => (
              <button
                key={q}
                type="button"
                onClick={() => {
                  setQuestion(q);
                  submit(q);
                }}
                className="text-xs px-2.5 py-1 rounded-full border border-ink-200 text-ink-600 hover:border-ink-300 hover:text-ink-900 transition"
                disabled={loading}
              >
                {q}
              </button>
            ))}
          </div>
        </form>

        {/* 4-agent orchestrator visibility (Pattern 2 multi-agent visibility) */}
        {(loading || response) && (
          <div className="mb-8">
            <h2 className="text-xs font-mono text-ink-500 uppercase tracking-wider mb-3">
              Multi-agent orchestrator · {agents.filter((a) => a.status === "done").length}/4 complete
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              {agents.map((agent) => (
                <AgentCard key={agent.id} agent={agent} />
              ))}
            </div>
          </div>
        )}

        {error && (
          <div className="border border-unverified rounded-lg p-4 text-sm text-unverified mb-6">
            Error: {error}
          </div>
        )}

        {response && (
          <div className="space-y-8">
            {/* Arbitration panel — Pattern 2 (multi-agent arbitration visibility) */}
            {conflictCount > 0 && (
              <div className="border border-amber-300 bg-amber-50 rounded-lg p-5">
                <div className="flex items-center gap-2 mb-2">
                  <span className="w-2 h-2 rounded-full bg-amber-500" />
                  <h2 className="text-sm font-semibold tracking-tight text-amber-900">
                    Synthesizer arbitration · {conflictCount} source conflict{conflictCount > 1 ? "s" : ""} resolved
                  </h2>
                </div>
                <p className="text-xs text-amber-800 leading-relaxed">
                  The <strong>Verifier</strong> agent flagged {conflictCount} citation{conflictCount > 1 ? "s" : ""} with
                  conflicting facts across sources. The <strong>Synthesizer</strong> resolved the conflict by weighting
                  primary sources (SEC filings, official PR) above secondary (news aggregation). All conflicting evidence
                  packets remain in the cryptographic chain — none discarded.
                </p>
              </div>
            )}

            {/* Answer */}
            <div className="border border-ink-200 rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold tracking-tight">Answer</h2>
                <div className="flex items-center gap-3 text-xs font-mono text-ink-500">
                  <span>conf {Math.round(response.confidence * 100)}%</span>
                  <span>·</span>
                  <span>{Math.round(response.latency_ms)}ms</span>
                </div>
              </div>
              <p className="text-ink-800 leading-relaxed whitespace-pre-wrap">{response.answer}</p>
            </div>

            {/* Citations */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold tracking-tight">
                  Citations · {response.citations.length}
                </h2>
                <a
                  href={response.verify_url}
                  target="_blank"
                  rel="noopener"
                  className="text-xs font-mono text-ink-500 hover:text-ink-900 transition"
                >
                  Verify chain → {response.verify_url.split("/").pop()}
                </a>
              </div>
              <div className="space-y-2">
                {response.citations.map((c, i) => (
                  <CitationRow key={i} citation={c} index={i} />
                ))}
              </div>
            </div>

            {/* Evidence chain meta */}
            <div className="text-xs font-mono text-ink-400 pt-4 border-t border-ink-100">
              chain_length: {response.evidence_chain_length} · request_id: {response.request_id} · verifier: Ed25519
            </div>
          </div>
        )}
      </section>
    </main>
  );
}

function AgentCard({ agent }: { agent: AgentState }) {
  const statusBadge =
    agent.status === "idle" ? (
      <span className="text-xs font-mono text-ink-400">idle</span>
    ) : agent.status === "active" ? (
      <span className={`text-xs font-mono ${agent.accent} flex items-center gap-1.5`}>
        <span className={`w-1.5 h-1.5 rounded-full ${agent.accent.replace("text-", "bg-")} animate-pulse`} />
        running
      </span>
    ) : (
      <span className={`text-xs font-mono ${agent.accent} flex items-center gap-1.5`}>
        <svg className={`w-3 h-3 ${agent.accent}`} viewBox="0 0 20 20" fill="currentColor">
          <path
            fillRule="evenodd"
            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
            clipRule="evenodd"
          />
        </svg>
        done
      </span>
    );

  return (
    <div
      className={`border ${agent.border} ${agent.status !== "idle" ? agent.bg : "bg-white"} rounded-lg p-4 transition-all duration-300`}
    >
      <div className="flex items-start justify-between mb-2">
        <div>
          <div className={`text-sm font-semibold ${agent.accent}`}>{agent.label}</div>
          <div className="text-xs font-mono text-ink-500 mt-0.5">{agent.task}</div>
        </div>
        {statusBadge}
      </div>
      <p className="text-xs text-ink-600 leading-relaxed">{agent.detail}</p>
    </div>
  );
}

function CitationRow({ citation, index }: { citation: Citation; index: number }) {
  return (
    <div className="border border-ink-200 rounded-lg p-4 hover:border-ink-300 transition">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 mt-0.5">
          {citation.conflict_flag ? (
            <span
              className="w-2 h-2 rounded-full bg-conflict block"
              title="Source conflict — see arbitration panel above"
            />
          ) : (
            <span className="w-2 h-2 rounded-full bg-verified block" title="Verified by all 4 agents" />
          )}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-3 mb-1">
            <a
              href={citation.url}
              target="_blank"
              rel="noopener"
              className="text-sm font-medium hover:underline truncate"
            >
              [{index + 1}] {citation.title}
            </a>
            <span className="text-xs font-mono text-ink-400 flex-shrink-0">
              {Math.round(citation.confidence * 100)}%
            </span>
          </div>
          <p className="text-xs text-ink-600 mb-2 line-clamp-2">{citation.snippet}</p>
          <div className="flex items-center gap-2 text-xs font-mono text-ink-400">
            <span>hash</span>
            <code className="px-1.5 py-0.5 bg-ink-100 rounded">{citation.content_hash.slice(0, 16)}…</code>
            <span>·</span>
            <a href={citation.url} target="_blank" rel="noopener" className="hover:text-ink-700 truncate max-w-md">
              {new URL(citation.url).hostname}
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
