import Link from "next/link";

/**
 * PROOFCHAIN hero page — Linear/Vercel-grade taste.
 *
 * Discipline rules:
 *   - One primary action (CTA → /demo)
 *   - One headline + one subhead, no walls of text
 *   - White background, no gradients
 *   - Inter font, tight letter-spacing
 *   - All evidence shown as monospace truncated hash (signals seriousness)
 */
export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Nav */}
      <nav className="container-wide flex items-center justify-between py-6">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-7 h-7 rounded bg-ink-900" />
          <span className="text-sm font-semibold tracking-tight">PROOFCHAIN</span>
        </Link>
        <div className="flex items-center gap-6 text-sm text-ink-600">
          <Link href="/docs" className="hover:text-ink-900 transition">Docs</Link>
          <Link href="/demo" className="hover:text-ink-900 transition">Demo</Link>
          <a
            href="https://github.com/SRKRZ23/proofchain"
            target="_blank"
            rel="noopener"
            className="hover:text-ink-900 transition"
          >
            GitHub
          </a>
        </div>
      </nav>

      {/* Hero */}
      <section className="container-narrow text-center pt-24 pb-16">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ink-200 text-xs text-ink-600 mb-8">
          <span className="w-1.5 h-1.5 rounded-full bg-verified animate-pulse" />
          Built for Bright Data Web Data UNLOCKED · May 2026
        </div>

        <h1 className="text-5xl md:text-6xl font-semibold tracking-tighter leading-[1.05] mb-6">
          Other AI agents claim citations.
          <br />
          <span className="text-ink-500">PROOFCHAIN signs every one.</span>
        </h1>

        <p className="text-lg text-ink-600 mb-10 leading-relaxed">
          4 named agents answer your research question in ~30 seconds.
          Every citation is Ed25519-signed and hash-chained — publicly verifiable
          with our open key, no API access needed.
        </p>

        <div className="flex items-center justify-center gap-3">
          <Link
            href="/demo"
            className="inline-flex items-center justify-center px-5 py-2.5 rounded-md bg-ink-900 text-white text-sm font-medium hover:bg-ink-800 transition"
          >
            Try the demo
          </Link>
          <a
            href="https://github.com/SRKRZ23/proofchain"
            target="_blank"
            rel="noopener"
            className="inline-flex items-center justify-center px-5 py-2.5 rounded-md border border-ink-200 text-sm font-medium hover:border-ink-300 transition"
          >
            View on GitHub →
          </a>
        </div>

        {/* Demo credentials — visible to judges/visitors with zero signup friction */}
        <div className="mt-10 inline-block px-4 py-2 rounded-md bg-ink-50 border border-ink-200">
          <p className="text-xs font-mono text-ink-700">
            <span className="text-ink-500">Demo creds:</span>{" "}
            <code className="text-ink-900">research@acme.com / proof-it</code>
          </p>
        </div>

        {/* Killer one-liner */}
        <p className="mt-16 text-sm font-mono text-ink-500">
          Anthropic owns MCP. We own the audit trail.
        </p>
      </section>

      {/* Narrow demo entry CTA — Pattern 1 (specificity) + Pattern 4 (testable demo) */}
      <section className="container-narrow py-12 border-t border-ink-100">
        <div className="border border-ink-200 rounded-xl p-8 bg-gradient-to-br from-ink-50 to-white">
          <div className="flex items-start justify-between gap-6 mb-6">
            <div className="flex-1">
              <p className="text-xs font-mono text-ink-500 mb-2 uppercase tracking-wider">Try it as</p>
              <h2 className="text-2xl font-semibold tracking-tight mb-3">Equity research analyst.</h2>
              <p className="text-ink-600 leading-relaxed mb-4">
                Ask: <em className="text-ink-900">&ldquo;What is TSLA&apos;s customer concentration risk in Europe?&rdquo;</em>
              </p>
              <p className="text-sm text-ink-600 leading-relaxed">
                4 named agents work in parallel — <strong className="text-blue-600">Searcher</strong> queries Bright Data SERP ·{" "}
                <strong className="text-emerald-600">Scraper</strong> extracts via Web Unlocker ·{" "}
                <strong className="text-amber-600">Verifier</strong> signs with Ed25519 ·{" "}
                <strong className="text-purple-600">Synthesizer</strong> composes with grounded citations.
              </p>
            </div>
          </div>
          <div className="flex items-center justify-between border-t border-ink-100 pt-6">
            <div className="text-xs font-mono text-ink-500">
              ~30 seconds · 5 citations · public Ed25519 verification (no API key)
            </div>
            <Link
              href="/demo"
              className="inline-flex items-center justify-center px-5 py-2.5 rounded-md bg-ink-900 text-white text-sm font-medium hover:bg-ink-800 transition"
            >
              Run the demo →
            </Link>
          </div>
        </div>
      </section>

      {/* Three pillars */}
      <section className="container-wide py-16 border-t border-ink-100">
        <div className="grid md:grid-cols-3 gap-12">
          <Pillar
            label="01"
            title="Signed at the source"
            body="Every Bright Data fetch — SERP, Web Scraper, Unlocker, Scraping Browser — is Ed25519-signed at capture time."
          />
          <Pillar
            label="02"
            title="Hash-chained forever"
            body="Each evidence packet commits to all previous. Tamper with one, the entire chain fails verification."
          />
          <Pillar
            label="03"
            title="MCP-compatible"
            body="Drop into Claude Desktop, Cursor, or LangChain. Your agent gains verified web access in one config line."
          />
        </div>
      </section>

      {/* Verticals */}
      <section className="container-wide py-16 border-t border-ink-100">
        <h2 className="text-2xl font-semibold tracking-tight mb-12">One engine. Five verticals.</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <VerticalCard
            label="Flagship"
            title="Equity research analyst copilot"
            body="$30B/yr labor waste at hedge funds + investment banks. Goldman & MS cutting 2,500 analysts in 2025. AlphaSense $500M ARR @ $4B."
          />
          <VerticalCard
            label="Roadmap"
            title="AML / KYC surveillance"
            body="TD Bank $3B fine for fabricated audit trails. Mastercard ← Recorded Future $2.65B (8.8× revenue)."
          />
          <VerticalCard
            label="Roadmap"
            title="Regulatory monitoring"
            body="SEC, FDA, EU regulators. Continuous parsing with structured alerts + signed evidence."
          />
          <VerticalCard
            label="Roadmap"
            title="Third-party risk (TPCRM)"
            body="$9.5B → $37.4B market by 2033. Snowflake/Change Healthcare cascades forced regulators to mandate."
          />
          <VerticalCard
            label="Roadmap"
            title="Publisher provenance"
            body="NYT v Perplexity (Dec 2025) — citation hallucination = legal liability. Publishers need court-grade evidence."
          />
          <VerticalCard
            label="Open"
            title="Build your own"
            body="One Python SDK, one JavaScript SDK, one MCP server. Adapt PROOFCHAIN to any vertical."
          />
        </div>
      </section>

      {/* Industry validation — throwaway code thesis */}
      <section className="container-wide py-16 border-t border-ink-100">
        <div className="text-center mb-10">
          <p className="text-xs font-mono text-ink-400 mb-2">THESIS TAILWIND</p>
          <h2 className="text-2xl font-semibold tracking-tight">
            When code is ephemeral, evidence is the only thing that persists.
          </h2>
        </div>
        <div className="grid md:grid-cols-3 gap-8">
          <Quote
            text="Code is suddenly free, ephemeral, malleable, discardable after single use."
            author="Andrej Karpathy"
            role="Sequoia AI Ascent 2026"
          />
          <Quote
            text="Thirty percent of apps on Vercel already come from agents."
            author="Guillermo Rauch"
            role="Vercel CEO, $340M ARR"
          />
          <Quote
            text="The value of all application software will eventually go to zero."
            author="Amjad Masad"
            role="Replit CEO"
          />
        </div>
      </section>

      {/* IETF web-bot-auth alignment */}
      <section className="container-narrow py-16 border-t border-ink-100">
        <div className="text-center">
          <p className="text-xs font-mono text-ink-400 mb-2">STANDARDS ALIGNMENT</p>
          <h2 className="text-2xl font-semibold tracking-tight mb-4">
            Hash-chain extension to IETF web-bot-auth.
          </h2>
          <p className="text-ink-600 leading-relaxed mb-2">
            <code className="font-mono text-sm bg-ink-100 px-1.5 py-0.5 rounded">
              draft-meunier-web-bot-auth-architecture-05
            </code>
            {" "}— Cloudflare + Google co-authored. Aligned: Amazon, Akamai, OpenAI.
          </p>
          <p className="text-sm text-ink-500">
            The spec signs HTTP requests. We add: hash-chain · content evidence · EU AI Act compliance overlay.
          </p>
        </div>
      </section>

      {/* CTA strip */}
      <section className="container-narrow py-24 text-center border-t border-ink-100">
        <h2 className="text-3xl font-semibold tracking-tight mb-4">
          Drop into your agent in one line.
        </h2>
        <p className="text-ink-600 mb-8">
          Compatible with Anthropic Claude, OpenAI, Google Gemini via Model Context Protocol.
        </p>
        <pre className="inline-block text-left bg-ink-950 text-ink-100 px-6 py-4 rounded-lg text-sm font-mono mb-8">
          <code>{`pip install proofchain-sdk
# or
npm install @proofchain/sdk`}</code>
        </pre>
        <div>
          <Link
            href="/demo"
            className="inline-flex items-center justify-center px-5 py-2.5 rounded-md bg-ink-900 text-white text-sm font-medium hover:bg-ink-800 transition"
          >
            Try the live demo →
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="container-wide py-10 border-t border-ink-100 text-sm text-ink-500 flex items-center justify-between">
        <span>© 2026 PROOFCHAIN · Sardor Razikov</span>
        <div className="flex items-center gap-6">
          <Link href="/docs" className="hover:text-ink-900 transition">Docs</Link>
          <a href="https://github.com/SRKRZ23/proofchain" target="_blank" rel="noopener" className="hover:text-ink-900 transition">
            GitHub
          </a>
          <a href="https://lablab.ai/ai-hackathons/brightdata-ai-agents-web-data-hackathon/proofchain" target="_blank" rel="noopener" className="hover:text-ink-900 transition">
            lablab.ai
          </a>
        </div>
      </footer>
    </main>
  );
}

function Pillar({ label, title, body }: { label: string; title: string; body: string }) {
  return (
    <div>
      <div className="text-xs font-mono text-ink-400 mb-3">{label}</div>
      <h3 className="text-lg font-semibold tracking-tight mb-2">{title}</h3>
      <p className="text-ink-600 leading-relaxed">{body}</p>
    </div>
  );
}

function VerticalCard({ label, title, body }: { label: string; title: string; body: string }) {
  return (
    <div className="border border-ink-200 rounded-lg p-6 hover:border-ink-300 transition">
      <div className="text-xs font-mono text-ink-400 mb-3">{label}</div>
      <h3 className="text-base font-semibold tracking-tight mb-2">{title}</h3>
      <p className="text-sm text-ink-600 leading-relaxed">{body}</p>
    </div>
  );
}

function Quote({ text, author, role }: { text: string; author: string; role: string }) {
  return (
    <blockquote className="border-l-2 border-ink-200 pl-4">
      <p className="text-ink-800 leading-relaxed mb-3 text-[15px]">"{text}"</p>
      <footer className="text-xs">
        <span className="font-semibold text-ink-900">{author}</span>
        <span className="text-ink-500"> · {role}</span>
      </footer>
    </blockquote>
  );
}
