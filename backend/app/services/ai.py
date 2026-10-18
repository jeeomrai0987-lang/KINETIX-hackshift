import json
import logging
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from backend.app.config import settings

logger = logging.getLogger(__name__)

CANONICAL_SKILL_VOCAB = [
    "distributed systems", "rust", "go", "c++", "c/c++", "raft consensus",
    "zero-copy io", "p99 latency optimization", "ebpf", "kubernetes operator",
    "microvm sandboxing", "wasm runtime", "wasmtime", "grpc", "distributed state",
    "fintech protocols", "audit attestation", "sandbox isolation", "lsm-trees",
    "memory layouts", "kernel tracing", "system architecture", "enterprise gtm",
    "b2b saas", "security compliance", "cuda", "pytorch", "vllm"
]

SKILL_ALIASES = {
    "golang": "go",
    "k8s": "kubernetes operator",
    "kubernetes": "kubernetes operator",
    "low latency": "zero-copy io",
    "low-latency": "zero-copy io",
    "low latency systems": "zero-copy io",
    "raft": "raft consensus",
    "consensus": "raft consensus",
    "consensus algorithms": "raft consensus",
    "wasm": "wasm runtime",
    "sandboxing": "sandbox isolation",
    "cpp": "c++",
    "c": "c/c++",
    "distributed": "distributed systems",
    "system arch": "system architecture",
    "ebpf tracing": "ebpf",
    "linux tracing": "kernel tracing",
    "distributed state machine": "distributed state",
}

def normalize_skill(skill: str) -> str:
    cleaned = skill.lower().strip()
    return SKILL_ALIASES.get(cleaned, cleaned)


class AISkillRequirement(BaseModel):
    skill: str
    weight: float = Field(default=1.0, ge=0.1, le=1.0)


class AIRole(BaseModel):
    title: str
    description: str
    equity_pct: float = Field(default=15.0, ge=1.0, le=60.0)
    requirements: List[AISkillRequirement]
    min_experience: str = Field(default="senior")


class AIConstraints(BaseModel):
    sector: str = Field(default="Enterprise AI & Distributed Systems")
    latency_ms: int = Field(default=2)
    compliance: List[str] = Field(default_factory=lambda: ["SOC2", "FedRAMP"])
    squad_size: int = Field(default=4)


class AIThesisDecomposition(BaseModel):
    constraints: AIConstraints
    clarity_score: int = Field(default=90, ge=0, le=100)
    roles: List[AIRole] = Field(min_length=3, max_length=5)


def clamp_equity(roles: List[AIRole], max_total: float = 85.0) -> List[AIRole]:
    total = sum(r.equity_pct for r in roles)
    if total > max_total and total > 0:
        scale = max_total / total
        for r in roles:
            r.equity_pct = round(r.equity_pct * scale, 1)
    return roles


def deterministic_clarity_score(thesis: str) -> int:
    score = 65
    length = len(thesis.strip())
    if length > 80:
        score += 10
    if length > 200:
        score += 10

    keywords = [
        "latency", "throughput", "consensus", "distributed", "security",
        "compliance", "enterprise", "pilot", "pipeline", "scale", "gpu", "kernel"
    ]
    t_lower = thesis.lower()
    matches = sum(1 for kw in keywords if kw in t_lower)
    score += min(15, matches * 3)
    return min(98, score)


def deterministic_decomposition(thesis: str) -> AIThesisDecomposition:
    t_lower = thesis.lower()
    clarity = deterministic_clarity_score(thesis)

    if any(k in t_lower for k in ["crypto", "web3", "snark", "zk", "blockchain"]):
        constraints = AIConstraints(
            sector="Cryptographic Infrastructure & Web3",
            latency_ms=5,
            compliance=["Cryptographic Audit", "SOC2"],
            squad_size=4
        )
        roles = [
            AIRole(
                title="Co-Founder & Chief Cryptographer",
                description="Designs circuit architecture, polynomial commitments, and zero-knowledge verification kernels.",
                equity_pct=25.0,
                requirements=[
                    AISkillRequirement(skill="distributed systems", weight=1.0),
                    AISkillRequirement(skill="rust", weight=1.0),
                    AISkillRequirement(skill="audit attestation", weight=0.8),
                ],
                min_experience="founding"
            ),
            AIRole(
                title="Founding Protocol Engineer",
                description="Builds asynchronous networking engine, deterministic Raft consensus, and telemetry pipelines.",
                equity_pct=15.0,
                requirements=[
                    AISkillRequirement(skill="raft consensus", weight=1.0),
                    AISkillRequirement(skill="rust", weight=1.0),
                    AISkillRequirement(skill="zero-copy io", weight=0.9),
                ],
                min_experience="senior"
            ),
            AIRole(
                title="Lead Infrastructure Security Engineer",
                description="Implements microVM isolation, sandbox verification, and FedRAMP compliance test harnesses.",
                equity_pct=15.0,
                requirements=[
                    AISkillRequirement(skill="sandbox isolation", weight=1.0),
                    AISkillRequirement(skill="ebpf", weight=0.9),
                    AISkillRequirement(skill="kubernetes operator", weight=0.7),
                ],
                min_experience="senior"
            ),
            AIRole(
                title="Head of Enterprise Partnerships",
                description="Leads pilot deployments, institutional discovery, and developer ecosystem expansion.",
                equity_pct=15.0,
                requirements=[
                    AISkillRequirement(skill="enterprise gtm", weight=1.0),
                    AISkillRequirement(skill="b2b saas", weight=0.9),
                    AISkillRequirement(skill="security compliance", weight=0.8),
                ],
                min_experience="senior"
            )
        ]
    else:
        constraints = AIConstraints(
            sector="Enterprise FinTech & Autonomous AI",
            latency_ms=2,
            compliance=["SOC2 Type II", "FedRAMP Ready"],
            squad_size=4
        )
        roles = [
            AIRole(
                title="Co-Founder & CTO",
                description="Architects high-throughput consensus mechanisms and memory-safe verifiable kernels.",
                equity_pct=25.0,
                requirements=[
                    AISkillRequirement(skill="distributed systems", weight=1.0),
                    AISkillRequirement(skill="rust", weight=1.0),
                    AISkillRequirement(skill="system architecture", weight=0.9),
                ],
                min_experience="founding"
            ),
            AIRole(
                title="Founding Distributed Systems Engineer",
                description="Builds zero-copy asynchronous networking engines, deterministic Raft clusters, and telemetry pipelines.",
                equity_pct=15.0,
                requirements=[
                    AISkillRequirement(skill="distributed systems", weight=1.0),
                    AISkillRequirement(skill="rust", weight=1.0),
                    AISkillRequirement(skill="go", weight=0.8),
                    AISkillRequirement(skill="zero-copy io", weight=0.9),
                ],
                min_experience="senior"
            ),
            AIRole(
                title="Lead Inference Systems Engineer",
                description="Implements GPU kernel optimizations, CUDA kernels, vLLM parallel serving, and memory tiering.",
                equity_pct=15.0,
                requirements=[
                    AISkillRequirement(skill="cuda", weight=1.0),
                    AISkillRequirement(skill="c++", weight=0.9),
                    AISkillRequirement(skill="p99 latency optimization", weight=0.8),
                ],
                min_experience="senior"
            ),
            AIRole(
                title="Head of Enterprise Growth",
                description="Drives strategic pilot deployments, enterprise customer discovery, and compliance partnership pipelines.",
                equity_pct=15.0,
                requirements=[
                    AISkillRequirement(skill="enterprise gtm", weight=1.0),
                    AISkillRequirement(skill="b2b saas", weight=0.9),
                    AISkillRequirement(skill="security compliance", weight=0.8),
                ],
                min_experience="senior"
            )
        ]

    return AIThesisDecomposition(
        constraints=constraints,
        clarity_score=clarity,
        roles=clamp_equity(roles)
    )


def call_gemini(thesis: str, allowed_skills: List[str]) -> Optional[AIThesisDecomposition]:
    if not settings.gemini_api_key:
        logger.info("gemini: fallback (no API key configured)")
        return None

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        logger.warning("gemini: fallback (google-genai not installed)")
        return None

    model_name = settings.gemini_model or "gemini-2.5-flash"
    client = genai.Client(
        api_key=settings.gemini_api_key,
        http_options=types.HttpOptions(timeout=settings.gemini_timeout_seconds)
    )

    system_instruction = (
        "You are an expert technical venture architect for VentureForge AI. "
        "Decompose a startup thesis into exact technical constraints, clarity score (0-100), "
        "and a founding squad blueprint (3 to 5 roles). "
        f"Allowed skill vocabulary: {', '.join(allowed_skills)}. "
        "For each role, provide 2-4 required skills with normalized lowercase names and weights (0.5 to 1.0), "
        "and minimum experience ('junior', 'mid', 'senior', or 'founding'). "
        "The sum of equityPct across all roles must not exceed 85%."
    )

    prompt = f"Analyze and decompose this startup thesis:\n\n{thesis}"

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=AIThesisDecomposition,
                ),
            )
            raw_text = response.text
            if not raw_text:
                raise ValueError("Empty response from Gemini")
            data = json.loads(raw_text)
            result = AIThesisDecomposition.model_validate(data)
            logger.info("gemini: ok")
            return result
        except Exception as e:
            err_str = str(e)
            is_transient = "429" in err_str or "500" in err_str or "503" in err_str or "quota" in err_str.lower()
            if attempt == 0 and is_transient:
                time.sleep(1.0)
                continue
            logger.warning("gemini: fallback (%s)", type(e).__name__)
            return None


def decompose_thesis(thesis: str, allowed_skills: Optional[List[str]] = None) -> Dict[str, Any]:
    skills = allowed_skills or CANONICAL_SKILL_VOCAB
    start_time = time.perf_counter()

    ai_result = call_gemini(thesis, skills)
    if ai_result:
        source = "gemini"
        decomposition = ai_result
    else:
        source = "fallback"
        decomposition = deterministic_decomposition(thesis)

    elapsed_ms = int((time.perf_counter() - start_time) * 1000)

    # Normalize skills across roles and clamp equity
    roles = clamp_equity(decomposition.roles)
    for r in roles:
        for req in r.requirements:
            req.skill = normalize_skill(req.skill)

    blueprint_list = []
    for r in roles:
        req_list = [{"skill": req.skill, "weight": req.weight} for req in r.requirements]
        blueprint_list.append({
            "title": r.title,
            "description": r.description,
            "equityPct": r.equity_pct,
            "requirements": req_list,
            "requiredSkills": req_list,
            "minExperience": r.min_experience
        })

    return {
        "thesis": thesis,
        "constraints": {
            "sector": decomposition.constraints.sector,
            "latencyMs": decomposition.constraints.latency_ms,
            "compliance": decomposition.constraints.compliance,
            "squadSize": decomposition.constraints.squad_size,
        },
        "clarityScore": decomposition.clarity_score,
        "blueprint": blueprint_list,
        "roles": blueprint_list,
        "source": source,
        "latencyMs": elapsed_ms
    }
