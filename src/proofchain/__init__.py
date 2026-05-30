"""PROOFCHAIN — cryptographic provenance layer для AI agent web fetches.

Drop-in MCP middleware that wraps Bright Data API calls with Ed25519 signed
evidence packets, providing tamper-evident audit trails для enterprise
AI compliance use cases.

Track 3 (Security & Compliance / Infrastructure) submission to the
Web Data UNLOCKED Hackathon (May 25-31, 2026).
"""

from proofchain.signing import ProofChainSigner

__version__ = "0.1.0"
__all__ = ["ProofChainSigner"]
