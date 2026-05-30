# proofchain-sdk

**Cryptographic audit trail for AI agents on the live web.**

Drop-in Python SDK for Bright Data with Ed25519-signed evidence packets.

```bash
pip install proofchain-sdk
```

```python
from proofchain import Client

pc = Client(api_key="your-bright-data-key")

result = pc.search("NVDA Q1 2026 data-center revenue", num_results=5)

for citation in result.citations:
    print(f"[{citation.rank}] {citation.title}")
    print(f"  url:   {citation.url}")
    print(f"  hash:  {citation.content_hash[:16]}…")
    print(f"  sig:   verified ✓")
```

Full docs: https://proofchain.dev/docs

License: MIT
