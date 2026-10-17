import json
import logging
from typing import Dict, Any, List
from backend.app.config import settings

logger = logging.getLogger(__name__)

DETERMINISTIC_BLUEPRINTS = {
    "default": {
        "constraints": {
            "latency": "< 2.0ms p99",
            "compliance": "SOC2 / FedRAMP ready",
            "squadSize": "4 core nodes",
            "compute": "H100 NVLink Cluster",
            "architecture": "Event-driven decentralized mesh"
        },
        "blueprint": [
            {
                "title": "Co-Founder & CTO",
                "description": "Architects high-throughput consensus mechanisms and memory-safe verifiable kernels.",
                "equityPct": 25.0,
                "requirements": ["Distributed Systems", "Rust", "Consensus Algorithms"]
            },
            {
                "title": "Head of Enterprise Growth",
                "description": "Drives strategic pilot deployments, enterprise customer discovery, and compliance partnership pipelines.",
                "equityPct": 15.0,
                "requirements": ["Enterprise GTM", "B2B SaaS", "Security Compliance"]
            },
            {
                "title": "Founding Distributed Systems Engineer",
                "description": "Builds zero-copy asynchronous networking engines, deterministic Raft clusters, and telemetry pipelines.",
                "equityPct": 15.0,
                "requirements": ["Distributed Systems", "Rust", "Go", "p99 Latency Optimization"]
            },
            {
                "title": "Lead Inference Systems Engineer",
                "description": "Implements GPU kernel optimizations, CUDA kernels, vLLM parallel serving, and memory tiering.",
                "equityPct": 10.0,
                "requirements": ["CUDA", "PyTorch", "vLLM", "C++"]
            }
        ]
    },
    "crypto": {
        "constraints": {
            "finality": "< 500ms deterministic",
            "security": "Zero-Knowledge SNARK verifiable",
            "squadSize": "4 core nodes",
            "audit": "OpenZeppelin / Trail of Bits tier"
        },
        "blueprint": [
            {
                "title": "Co-Founder & Chief Cryptographer",
                "description": "Designs circuit architecture, polynomial commitment schemes, and recursive proof generation.",
                "equityPct": 25.0,
                "requirements": ["Cryptography", "ZK-SNARKs", "Rust", "Mathematics"]
            },
            {
                "title": "Protocol Engineering Lead",
                "description": "Builds peer-to-peer gossip network, state machine replication, and EVM/WASM bridging.",
                "equityPct": 15.0,
                "requirements": ["Solidity", "Rust", "libp2p", "MEV Protection"]
            },
            {
                "title": "Head of Ecosystem & Liquidity",
                "description": "Manages foundation grants, validator onboarding, and institutional staking partnerships.",
                "equityPct": 15.0,
                "requirements": ["DeFi", "Tokenomics", "Community Governance"]
            },
            {
                "title": "Smart Contract Security Auditor",
                "description": "Performs formal verification, invariant testing, and audit harness integration.",
                "equityPct": 10.0,
                "requirements": ["Certora", "Foundry", "Formal Verification"]
            }
        ]
    }
}

async def decompose_thesis(thesis: str) -> Dict[str, Any]:
    """
    Decomposes a venture thesis into engineering constraints and a target squad blueprint.
    Uses Anthropic Claude if ANTHROPIC_API_KEY is configured; otherwise uses deterministic fallback.
    """
    thesis_lower = thesis.lower()

    if settings.ANTHROPIC_API_KEY:
        try:
            import httpx
            prompt = f"""You are VentureForge AI, an elite autonomous venture architect.
Analyze this startup thesis:
"{thesis}"

Decompose it into technical constraints and a squad architecture blueprint.
Output strictly valid JSON with this exact schema:
{{
  "constraints": {{
    "latency": "string",
    "compliance": "string",
    "squadSize": "string",
    "compute": "string"
  }},
  "blueprint": [
    {{
      "title": "string",
      "description": "string",
      "equityPct": number,
      "requirements": ["string", "string"]
    }}
  ]
}}
Do not include any markdown backticks or commentary outside the JSON."""

            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": settings.ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": "claude-3-5-sonnet-20241022",
                        "max_tokens": 1500,
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    content_text = data["content"][0]["text"].strip()
                    # Clean markdown codeblocks if returned
                    if content_text.startswith("```"):
                        content_text = content_text.split("```")[1]
                        if content_text.startswith("json"):
                            content_text = content_text[4:]
                        content_text = content_text.strip()
                    parsed = json.loads(content_text)
                    return {
                        "thesis": thesis,
                        "constraints": parsed.get("constraints", {}),
                        "blueprint": parsed.get("blueprint", [])
                    }
        except Exception as e:
            logger.warning(f"Anthropic API call failed, falling back to deterministic: {e}")

    # Deterministic fallback
    if any(k in thesis_lower for k in ["zk", "crypto", "blockchain", "web3", "token", "ledger"]):
        chosen = DETERMINISTIC_BLUEPRINTS["crypto"]
    else:
        chosen = DETERMINISTIC_BLUEPRINTS["default"]

    return {
        "thesis": thesis,
        "constraints": chosen["constraints"],
        "blueprint": chosen["blueprint"]
    }
