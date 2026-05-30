-- PROOFCHAIN Supabase schema — evidence packet persistence
-- POST-KICKOFF: run via `supabase db push` or paste into SQL editor

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ─────────────────────────────────────────────────────────────────────────────
-- evidence_chains — one chain per logical session (e.g. one API key, one tenant)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS evidence_chains (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id       UUID,
    verify_key_hex  TEXT NOT NULL,         -- public Ed25519 verify key
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_evidence_chains_tenant ON evidence_chains(tenant_id);

-- ─────────────────────────────────────────────────────────────────────────────
-- evidence_packets — individual signed records
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS evidence_packets (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chain_id        UUID NOT NULL REFERENCES evidence_chains(id) ON DELETE CASCADE,
    request_id      TEXT NOT NULL,
    seq             BIGINT NOT NULL,
    prev_hash       TEXT NOT NULL,
    record_hash     TEXT NOT NULL,
    signature_hex   TEXT NOT NULL,
    event_type      TEXT NOT NULL,         -- agent_query, fetch_serp, fetch_scraper, etc.
    entry_json      JSONB NOT NULL,        -- full event payload
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(chain_id, seq)
);

CREATE INDEX IF NOT EXISTS idx_evidence_packets_request ON evidence_packets(request_id);
CREATE INDEX IF NOT EXISTS idx_evidence_packets_chain_seq ON evidence_packets(chain_id, seq);
CREATE INDEX IF NOT EXISTS idx_evidence_packets_event ON evidence_packets(event_type);
CREATE INDEX IF NOT EXISTS idx_evidence_packets_created ON evidence_packets(created_at);

-- ─────────────────────────────────────────────────────────────────────────────
-- research_requests — analyst questions and their final answers
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS research_requests (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    request_id          TEXT NOT NULL UNIQUE,
    chain_id            UUID NOT NULL REFERENCES evidence_chains(id),
    question            TEXT NOT NULL,
    question_hash       TEXT NOT NULL,
    persona             TEXT,
    answer              TEXT,
    answer_hash         TEXT,
    confidence          REAL,
    latency_ms          REAL,
    citation_count      INTEGER DEFAULT 0,
    conflict_count      INTEGER DEFAULT 0,
    model               TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_research_requests_chain ON research_requests(chain_id);
CREATE INDEX IF NOT EXISTS idx_research_requests_created ON research_requests(created_at);

-- ─────────────────────────────────────────────────────────────────────────────
-- benchmark_runs — comparison runs vs Perplexity / AlphaSense
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS benchmark_runs (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id     TEXT NOT NULL,
    question_text   TEXT NOT NULL,
    tool            TEXT NOT NULL,         -- proofchain, perplexity, alphasense
    latency_ms      REAL,
    citation_count  INTEGER,
    citation_accuracy REAL,                -- 0.0–1.0
    notes           TEXT,
    run_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_benchmark_runs_question ON benchmark_runs(question_id);
CREATE INDEX IF NOT EXISTS idx_benchmark_runs_tool ON benchmark_runs(tool);

-- ─────────────────────────────────────────────────────────────────────────────
-- Row Level Security (POST-KICKOFF)
-- ─────────────────────────────────────────────────────────────────────────────
ALTER TABLE evidence_chains ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidence_packets ENABLE ROW LEVEL SECURITY;
ALTER TABLE research_requests ENABLE ROW LEVEL SECURITY;

-- Allow public reads of completed research (for verification)
CREATE POLICY "Public can verify completed research"
    ON research_requests FOR SELECT
    USING (answer IS NOT NULL);

CREATE POLICY "Public can read evidence packets for verification"
    ON evidence_packets FOR SELECT
    USING (TRUE);

-- ─────────────────────────────────────────────────────────────────────────────
-- updated_at trigger
-- ─────────────────────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION update_updated_at() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at_chains
    BEFORE UPDATE ON evidence_chains
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
