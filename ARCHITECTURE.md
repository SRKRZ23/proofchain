# PROOFCHAIN Architecture

## System overview

```mermaid
graph TB
    subgraph AGENT["AI Agent Layer"]
        Claude[Claude Desktop / Cursor]
        GPT[OpenAI / GPT]
        Gemini[Google Gemini]
        LC[LangChain / CrewAI]
    end

    subgraph MCP["PROOFCHAIN MCP Server"]
        Tools["MCP Tools:<br/>search · scrape · fetch · verify · export"]
        Orch["Multi-Agent Orchestrator<br/>(Searcher · Scraper · Verifier · Synthesizer)"]
    end

    subgraph CORE["Evidence Core"]
        Chain["EvidenceChain<br/>(hash-chained log)"]
        Sign["Ed25519 Signer<br/>(PyNaCl)"]
        JCS["JCS Canonicalizer<br/>(RFC 8785)"]
    end

    subgraph BD["Bright Data Infrastructure"]
        SERP[SERP API]
        Scraper[Web Scraper API]
        Unlocker[Web Unlocker]
        Browser[Scraping Browser]
    end

    subgraph STORE["Persistence"]
        Supa[(Supabase<br/>evidence_packets)]
        Pub["Public Verify Endpoint"]
    end

    Claude & GPT & Gemini & LC -->|MCP protocol| Tools
    Tools --> Orch
    Orch --> SERP & Scraper & Unlocker & Browser
    SERP & Scraper & Unlocker & Browser -->|response| Chain
    Chain --> JCS --> Sign --> Chain
    Chain --> Supa
    Supa --> Pub
```

## Data flow — single research query

```mermaid
sequenceDiagram
    participant User as Analyst
    participant Agent as AI Agent
    participant PC as PROOFCHAIN MCP
    participant BD as Bright Data
    participant Chain as EvidenceChain
    participant Supa as Supabase

    User->>Agent: "TSLA EU customer concentration risk?"
    Agent->>PC: search(query)
    PC->>Chain: log_agent_query(req_id, hash)
    PC->>BD: SERP API search
    BD-->>PC: top 5 results
    PC->>Chain: log_fetch_serp(req_id, query_hash, count)
    Chain->>Chain: Ed25519 sign + hash-chain
    Chain->>Supa: persist evidence packet
    
    loop for each top result
        PC->>BD: Web Scraper or Unlocker
        BD-->>PC: structured content
        PC->>Chain: log_fetch_scraper(req_id, url, hash)
    end
    
    PC->>PC: Verifier cross-checks sources
    PC->>Chain: log_source_conflict (if found)
    PC->>Agent: Claude synthesis (with citations)
    PC->>Chain: log_agent_synthesis(req_id, answer_hash)
    
    PC-->>Agent: answer + citation graph + verify_url
    Agent-->>User: rendered response
    
    Note over User,Supa: Later: anyone can GET /api/verify/{req_id}<br/>to verify chain integrity
```

## Evidence packet schema

```mermaid
classDiagram
    class EvidencePacket {
        +int seq
        +string prev_hash
        +string record_hash
        +bytes signature
        +dict entry
        +bool verify(verify_key)
        +bytes payload_bytes()
        +dict to_dict()
    }

    class EvidenceChain {
        +SigningKey signing_key
        +string verify_key_hex
        +list~EvidencePacket~ records
        +EvidencePacket append(entry)
        +bool verify_chain()
        +dict export()
    }

    class WebEvidenceTrail {
        +EvidenceChain chain
        +log_agent_query(...)
        +log_fetch_serp(...)
        +log_fetch_scraper(...)
        +log_fetch_unlocker(...)
        +log_fetch_browser(...)
        +log_source_conflict(...)
        +log_agent_synthesis(...)
        +log_human_review(...)
        +dict export_for_eu_ai_act(months)
    }

    WebEvidenceTrail "1" --> "1" EvidenceChain
    EvidenceChain "1" --> "*" EvidencePacket
```

## Cryptographic properties (invariants)

| Property | Description | Guarantee |
|----------|-------------|-----------|
| **P1 — JCS determinism** | `canonical(X) == canonical(X)` always | RFC 8785 |
| **P2 — Sign+verify roundtrip** | `verify(sign(X), X) == OK` | Ed25519 / PyNaCl |
| **P3 — Tamper-decision** | Mutate `entry.content` → verify fails | SHA-256 hash + Ed25519 signature |
| **P4 — Hash-chain** | Each record commits to all previous | Linked via `prev_hash` |
| **P5 — EU AI Act Article 12** | 6-month retention export endpoint | Built-in |

## Deployment topology

```mermaid
graph LR
    subgraph Edge["Cloudflare / Vercel Edge"]
        Static["Next.js static + ISR"]
    end

    subgraph App["Vercel"]
        Demo["proofchain.dev<br/>+ /demo"]
    end

    subgraph API["Railway"]
        Fast["FastAPI<br/>main.py"]
        MCP["MCP server"]
    end

    subgraph DB["Supabase"]
        Pg[(PostgreSQL)]
        Auth[Auth]
    end

    User[User] --> Static
    Static --> Demo
    Demo -->|/api/*| Fast
    Fast --> MCP
    Fast --> Pg
    Demo --> Auth
```

## Security model

- **Signing keys are server-side** — never exposed to client. Generated on first deploy via PyNaCl `SigningKey.generate()`.
- **Verify keys are public** — anyone can verify a chain via `GET /api/verify/{request_id}`.
- **Robots.txt status is recorded** in every packet — proves we respected (or noted) crawler etiquette.
- **JWT auth** on `POST /api/research/` (post-kickoff Supabase Auth).
- **Rate limiting** on `POST /api/research/` — 10 req/min/IP free tier.

## Why hash-chained + Ed25519 (not just SHA-256)?

| Property | Plain SHA-256 | Ed25519 + chain |
|----------|---------------|-----------------|
| Detects tampering | ✓ | ✓ |
| Proves WHO produced it | ✗ | ✓ (public key) |
| Proves WHEN (relative) | ✗ | ✓ (chain order) |
| Court-admissible | partial | ✓ (with public verify key registry) |
| Reorderable | ✓ | ✗ (chain breaks) |

For legal-grade evidence (TD Bank fines, NYT v Perplexity), the chain + signature combination is the difference between "data you stored" and "data we will testify in court was produced at time T by entity E".
