# @proofchain/sdk

**Cryptographic audit trail for AI agents on the live web.**

JavaScript/TypeScript SDK for PROOFCHAIN.

```bash
npm install @proofchain/sdk
```

```typescript
import { Client } from "@proofchain/sdk";

const pc = new Client({ apiKey: process.env.BRIGHT_DATA_API_KEY });

const result = await pc.search("NVDA Q1 2026 data-center revenue", {
  numResults: 5,
});

result.citations.forEach((c) => {
  console.log(`[${c.rank}] ${c.title}`);
  console.log(`  verified: ${c.verified}`);
  console.log(`  hash: ${c.contentHash.slice(0, 16)}…`);
});
```

Full docs: https://proofchain.dev/docs

License: MIT
