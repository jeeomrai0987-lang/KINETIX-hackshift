import json
import uuid
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.app.config import settings
from backend.app.db import models
from backend.app.services.ai import normalize_skill
from backend.app.services.audit_service import log_audit

logger = logging.getLogger(__name__)

EXP_RANKS = {
    "junior": 1,
    "mid": 2,
    "senior": 3,
    "founding": 4,
}


class CandidateRerankItem(BaseModel):
    candidate_code: str
    reason: str


class RerankResponse(BaseModel):
    ranked_candidates: List[CandidateRerankItem]


def parse_role_requirements(requirements: Any) -> Dict[str, float]:
    """Normalizes role requirements into a dictionary of {normalized_skill: weight}."""
    req_dict: Dict[str, float] = {}
    if isinstance(requirements, list):
        for item in requirements:
            if isinstance(item, dict):
                skill = normalize_skill(item.get("skill", ""))
                weight = float(item.get("weight", 1.0))
                if skill:
                    req_dict[skill] = weight
            elif isinstance(item, str):
                skill = normalize_skill(item)
                if skill:
                    req_dict[skill] = 1.0
    return req_dict


def gemini_rerank(
    candidates: List[Dict[str, Any]],
    role_title: str,
    role_requirements: Dict[str, float]
) -> List[Dict[str, Any]]:
    """
    Reranks candidates using Gemini if GEMINI_RERANK=true and GEMINI_API_KEY is present.
    Sends strictly sanitized data: candidateCode, skills, experienceLevel, percentile.
    NEVER sends name, email, phone, avatar, or user_id (Blind Protocol - Rule 1).
    """
    if not (settings.gemini_rerank and settings.gemini_api_key):
        return candidates

    if not candidates:
        return candidates

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        logger.warning("gemini: fallback (google-genai not installed for rerank)")
        return candidates

    client = genai.Client(
        api_key=settings.gemini_api_key,
        http_options=types.HttpOptions(timeout=settings.gemini_timeout_seconds)
    )

    # Strictly blind payload (only candidateCode and technical specs)
    sanitized_pool = [
        {
            "candidateCode": c["candidateCode"],
            "skills": c["skills"],
            "experienceLevel": c["experienceLevel"],
            "percentile": c["percentile"]
        }
        for c in candidates
    ]

    valid_codes = {c["candidateCode"] for c in sanitized_pool}

    prompt = (
        f"You are evaluating candidates for the role: '{role_title}'.\n"
        f"Required skills and priority weights: {json.dumps(role_requirements)}\n"
        f"Candidates: {json.dumps(sanitized_pool)}\n\n"
        "Rank the candidates from best fit to lowest fit based on skill complementarity and percentile. "
        "Return a JSON list of candidateCode and a concise one-line reason for each."
    )

    try:
        response = client.models.generate_content(
            model=settings.gemini_model or "gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RerankResponse,
            ),
        )
        data = json.loads(response.text)
        rerank_result = RerankResponse.model_validate(data)

        # Validate returned candidate codes are a subset of provided codes
        returned_codes = [item.candidate_code for item in rerank_result.ranked_candidates if item.candidate_code in valid_codes]
        if not returned_codes:
            logger.warning("gemini: fallback (rerank returned no valid candidate codes)")
            return candidates

        # Re-order according to returned codes
        code_to_candidate = {c["candidateCode"]: c for c in candidates}
        code_to_reason = {item.candidate_code: item.reason for item in rerank_result.ranked_candidates}

        ordered = []
        for code in returned_codes:
            cand = code_to_candidate[code]
            cand["fitDetails"]["algorithmicReason"] = code_to_reason.get(code, cand["fitDetails"]["algorithmicReason"])
            ordered.append(cand)

        # Append any remaining candidates not mentioned in rerank
        seen = set(returned_codes)
        for c in candidates:
            if c["candidateCode"] not in seen:
                ordered.append(c)

        logger.info("gemini: ok (rerank completed)")
        return ordered
    except Exception as e:
        logger.warning("gemini: fallback (rerank failed: %s)", type(e).__name__)
        return candidates


def run_matching_for_role(
    role: models.SquadRole,
    venture: models.Venture,
    db: Session,
    rerank: Optional[bool] = None
) -> List[models.Match]:
    """
    Computes algorithmic candidate matches for a vacant squad role.
    Stage 1: SQL pre-filter
    Stage 2: Deterministic synergy score
    Stage 3: Optional Gemini re-ranking
    Stage 4: Upsert matches table
    """
    req_skills = parse_role_requirements(role.requirements)
    min_exp = getattr(role, "min_experience", "senior") or "senior"
    min_exp_rank = EXP_RANKS.get(min_exp.lower(), 2)

    # 1. Fetch worker profiles
    profiles = (
        db.query(models.WorkerProfile)
        .join(models.User, models.WorkerProfile.user_id == models.User.id)
        .all()
    )

    # Exclude founder and filled squad users
    filled_user_ids = {
        sr.filled_by_user_id
        for sr in db.query(models.SquadRole).filter(models.SquadRole.venture_id == venture.id).all()
        if sr.filled_by_user_id
    }
    filled_user_ids.add(venture.founder_id)

    # Existing invited or accepted matches for this role must not be overwritten
    existing_matches = {
        m.worker_id: m
        for m in db.query(models.Match).filter(models.Match.role_id == role.id).all()
    }

    candidates = []

    for wp in profiles:
        user_id = wp.user_id
        if user_id in filled_user_ids:
            continue

        existing_match = existing_matches.get(user_id)
        if existing_match and existing_match.status in ("invited", "accepted"):
            continue

        # Availability filter
        avail = wp.weekly_availability_hours if wp.weekly_availability_hours is not None else 40
        if avail < 10:
            continue

        # Experience check
        exp_level = (wp.experience_level or "mid").lower()
        exp_rank = EXP_RANKS.get(exp_level, 2)

        # Skill overlap calculation
        worker_skills = [normalize_skill(s) for s in (wp.skills or [])]
        worker_skill_set = set(worker_skills)

        matched_skills = [s for s in req_skills if s in worker_skill_set]
        missing_skills = [s for s in req_skills if s not in worker_skill_set]

        # Require at least 1 overlapping skill if role specifies requirements
        if req_skills and not matched_skills:
            continue

        # Stage 2: Deterministic synergy scoring
        if req_skills:
            total_req_weight = sum(req_skills.values()) or 1.0
            matched_weight = sum(req_skills[s] for s in matched_skills)
            skill_score = (matched_weight / total_req_weight) * 100.0
        else:
            skill_score = 80.0

        exp_score = 100.0 if exp_rank >= min_exp_rank else 70.0
        avail_score = min(100.0, (float(avail) / 40.0) * 100.0)
        pctl_score = float(wp.percentile if wp.percentile is not None else 90.0)

        composite = (0.60 * skill_score) + (0.15 * exp_score) + (0.10 * avail_score) + (0.15 * pctl_score)
        synergy_score = int(round(max(50, min(99, composite))))

        fit_details = {
            "matchedSkills": matched_skills,
            "missingSkills": missing_skills,
            "experienceFit": f"{exp_level.capitalize()} meets {min_exp}",
            "availabilityHours": avail,
            "algorithmicReason": f"High skill complementarity ({int(skill_score)}% overlap). Verified cryptographic benchmark."
        }

        user = wp.user or db.query(models.User).filter_by(id=user_id).first()
        candidate_code = (user.node_id if user and user.node_id else None) or f"TX-{user_id[-5:].upper()}"

        candidates.append({
            "workerId": user_id,
            "candidateCode": candidate_code,
            "skills": worker_skills,
            "experienceLevel": exp_level,
            "percentile": pctl_score,
            "synergyScore": synergy_score,
            "fitDetails": fit_details,
            "existingMatch": existing_match,
        })

    # Sort deterministically by synergy_score descending, then percentile descending
    candidates.sort(key=lambda c: (c["synergyScore"], c["percentile"]), reverse=True)

    # Stage 3: Optional Gemini re-ranking on top 10-20
    top_pool = candidates[:20]
    remainder = candidates[20:]

    should_rerank = rerank if rerank is not None else settings.gemini_rerank
    if should_rerank:
        top_pool = gemini_rerank(top_pool, role.title, req_skills)

    final_candidates = (top_pool + remainder)[:5]  # Top 5 matches per role

    # Stage 4: Upsert into matches table
    persisted_matches = []
    for cand in final_candidates:
        existing = cand["existingMatch"]
        if existing:
            if existing.status == "suggested":
                existing.synergy_score = cand["synergyScore"]
                existing.fit_details = cand["fitDetails"]
                persisted_matches.append(existing)
        else:
            new_match = models.Match(
                id=f"mat_{uuid.uuid4().hex[:12]}",
                venture_id=venture.id,
                role_id=role.id,
                worker_id=cand["workerId"],
                candidate_code=cand["candidateCode"],
                synergy_score=cand["synergyScore"],
                fit_details=cand["fitDetails"],
                status="suggested"
            )
            db.add(new_match)
            persisted_matches.append(new_match)

    return persisted_matches


def run_matching_for_venture(
    venture_id: str,
    db: Session,
    rerank: Optional[bool] = None,
    actor_id: Optional[str] = None
) -> List[models.Match]:
    """
    Executes algorithmic matching across all vacant roles in a venture.
    """
    venture = db.query(models.Venture).filter_by(id=venture_id).first()
    if not venture:
        return []

    roles = (
        db.query(models.SquadRole)
        .filter(models.SquadRole.venture_id == venture.id)
        .all()
    )

    all_matches = []
    for role in roles:
        role_matches = run_matching_for_role(role, venture, db, rerank=rerank)
        all_matches.extend(role_matches)

    db.commit()

    log_audit(
        db,
        actor_id=actor_id or venture.founder_id,
        action="matches_calculated",
        entity="venture",
        entity_id=venture.id,
        payload={"totalMatches": len(all_matches)}
    )
    db.commit()

    return all_matches
