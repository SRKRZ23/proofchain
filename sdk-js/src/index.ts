/**
 * @proofchain/sdk — JavaScript/TypeScript client for PROOFCHAIN verified web data.
 *
 * Drop-in provenance layer for AI agents on the live web.
 * Every search/fetch returns content + Ed25519-signed evidence packet.
 */

export interface Citation {
  rank: number;
  url: string;
  title: string;
  snippet: string;
  contentHash: string;
  confidence: number;
  verified: boolean;
  conflictFlag: boolean;
}

export interface ResearchResult {
  requestId: string;
  question: string;
  answer: string;
  citations: Citation[];
  confidence: number;
  latencyMs: number;
  evidenceChainLength: number;
  verifyUrl: string;
  sourceConflicts: Array<Record<string, unknown>>;
}

export interface ClientOptions {
  apiKey?: string;
  apiBase?: string;
  timeoutMs?: number;
}

export class Client {
  private apiKey: string;
  private apiBase: string;
  private timeoutMs: number;

  constructor(opts: ClientOptions = {}) {
    this.apiKey =
      opts.apiKey ||
      (typeof process !== "undefined" ? process.env.PROOFCHAIN_API_KEY || process.env.BRIGHT_DATA_API_KEY : "") ||
      "";
    this.apiBase = (opts.apiBase || "https://api.proofchain.dev").replace(/\/$/, "");
    this.timeoutMs = opts.timeoutMs ?? 60_000;
  }

  /**
   * Submit a research question, get answer + signed citation graph.
   */
  async search(
    question: string,
    options: { persona?: string; numResults?: number } = {}
  ): Promise<ResearchResult> {
    const { persona = "equity_analyst", numResults = 5 } = options;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const res = await fetch(`${this.apiBase}/api/research/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(this.apiKey ? { Authorization: `Bearer ${this.apiKey}` } : {}),
        },
        body: JSON.stringify({ question, persona, num_sources: numResults }),
        signal: controller.signal,
      });

      if (!res.ok) throw new Error(`PROOFCHAIN API ${res.status}: ${await res.text()}`);
      const data = await res.json();

      return {
        requestId: data.request_id,
        question: data.question,
        answer: data.answer,
        citations: data.citations.map((c: any, i: number) => ({
          rank: i + 1,
          url: c.url,
          title: c.title,
          snippet: c.snippet,
          contentHash: c.content_hash,
          confidence: c.confidence,
          verified: !c.conflict_flag,
          conflictFlag: c.conflict_flag,
        })),
        confidence: data.confidence,
        latencyMs: data.latency_ms,
        evidenceChainLength: data.evidence_chain_length,
        verifyUrl: data.verify_url,
        sourceConflicts: data.source_conflicts || [],
      };
    } finally {
      clearTimeout(timeoutId);
    }
  }

  /**
   * Verify the evidence chain for a request_id.
   */
  async verify(requestId: string): Promise<Record<string, unknown>> {
    const res = await fetch(`${this.apiBase}/api/verify/${requestId}`);
    if (!res.ok) throw new Error(`PROOFCHAIN verify ${res.status}`);
    return res.json();
  }

  /**
   * Export the full evidence chain or EU AI Act-compliant subset.
   */
  async exportChain(euAiActCompliant = false): Promise<Record<string, unknown>> {
    const endpoint = euAiActCompliant ? "/api/export/eu-ai-act" : "/api/export/full";
    const res = await fetch(`${this.apiBase}${endpoint}`);
    if (!res.ok) throw new Error(`PROOFCHAIN export ${res.status}`);
    return res.json();
  }
}

export default Client;
