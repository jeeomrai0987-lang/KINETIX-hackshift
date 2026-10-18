import json
import logging
import pytest
from unittest.mock import MagicMock, patch

from backend.app.config import settings
from backend.app.services.ai import (
    normalize_skill,
    decompose_thesis,
    SKILL_ALIASES,
    AIThesisDecomposition,
    AIConstraints,
    AIRole,
    AISkillRequirement,
)
from backend.app.services.matching_service import (
    gemini_rerank,
    run_matching_for_venture,
)
from backend.app.db import SessionLocal, models


def test_skill_alias_normalization():
    """Verify skill alias map normalizes abbreviations to canonical terms."""
    assert normalize_skill("golang") == "go"
    assert normalize_skill("k8s") == "kubernetes operator"
    assert normalize_skill("kubernetes") == "kubernetes operator"
    assert normalize_skill("low latency") == "zero-copy io"
    assert normalize_skill("low-latency") == "zero-copy io"
    assert normalize_skill("raft") == "raft consensus"
    assert normalize_skill("consensus") == "raft consensus"
    assert normalize_skill("wasm") == "wasm runtime"
    assert normalize_skill("cpp") == "c++"
    assert normalize_skill("  Rust  ") == "rust"


def test_decompose_no_key_falls_back(caplog):
    """When GEMINI_API_KEY is empty, decompose_thesis falls back to deterministic."""
    with patch.object(settings, "GEMINI_API_KEY", ""):
        with caplog.at_level(logging.INFO):
            res = decompose_thesis("High throughput distributed consensus protocol")
            assert res["source"] == "fallback"
            assert res["clarityScore"] >= 0
            assert len(res["roles"]) >= 3
            assert "gemini: fallback (no API key configured)" in caplog.text


def test_decompose_valid_gemini_json():
    """When Gemini returns valid structured JSON, decompose_thesis parses and returns it."""
    mock_payload = {
        "constraints": {
            "sector": "Enterprise FinTech & Distributed Systems",
            "latency_ms": 2,
            "compliance": ["SOC2 Type II", "FedRAMP"],
            "squad_size": 4
        },
        "clarity_score": 94,
        "roles": [
            {
                "title": "Lead Consensus Architect",
                "description": "Architects Raft and zero-copy replication.",
                "equity_pct": 25.0,
                "requirements": [{"skill": "raft consensus", "weight": 1.0}, {"skill": "golang", "weight": 0.8}],
                "min_experience": "founding"
            },
            {
                "title": "Protocol Engineer",
                "description": "Zero-copy I/O pipelines.",
                "equity_pct": 20.0,
                "requirements": [{"skill": "rust", "weight": 1.0}, {"skill": "k8s", "weight": 0.8}],
                "min_experience": "senior"
            },
            {
                "title": "Security Lead",
                "description": "Sandbox isolation.",
                "equity_pct": 15.0,
                "requirements": [{"skill": "microvm sandboxing", "weight": 1.0}],
                "min_experience": "senior"
            }
        ]
    }

    mock_response = MagicMock()
    mock_response.text = json.dumps(mock_payload)

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response

    with patch.object(settings, "GEMINI_API_KEY", "test-key"):
        with patch("google.genai.Client", return_value=mock_client):
            res = decompose_thesis("High throughput distributed consensus protocol")
            assert res["source"] == "gemini"
            assert res["clarityScore"] == 94
            assert res["constraints"]["latencyMs"] == 2
            assert len(res["roles"]) == 3
            # Check skill alias normalization on output
            skills = [req["skill"] for r in res["roles"] for req in r["requirements"]]
            assert "go" in skills  # golang was normalized to go
            assert "kubernetes operator" in skills  # k8s was normalized to kubernetes operator


def test_decompose_invalid_json_falls_back(caplog):
    """When Gemini returns invalid JSON, decompose_thesis falls back deterministically."""
    mock_response = MagicMock()
    mock_response.text = "NOT_VALID_JSON{{"

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response

    with patch.object(settings, "GEMINI_API_KEY", "test-key"):
        with patch("google.genai.Client", return_value=mock_client):
            with caplog.at_level(logging.WARNING):
                res = decompose_thesis("A distributed trading engine")
                assert res["source"] == "fallback"
                assert len(res["roles"]) >= 3
                assert any("gemini: fallback" in msg for msg in caplog.messages)


def test_decompose_timeout_falls_back(caplog):
    """When Gemini call times out, decompose_thesis falls back."""
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = TimeoutError("Request timed out")

    with patch.object(settings, "GEMINI_API_KEY", "test-key"):
        with patch("google.genai.Client", return_value=mock_client):
            with caplog.at_level(logging.WARNING):
                res = decompose_thesis("A distributed trading engine")
                assert res["source"] == "fallback"
                assert any("gemini: fallback (TimeoutError)" in msg for msg in caplog.messages)


def test_decompose_429_retries_and_falls_back(caplog):
    """When Gemini returns 429 quota exhausted, system retries once then falls back."""
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception("429 ResourceExhausted: Quota exceeded")

    with patch.object(settings, "GEMINI_API_KEY", "test-key"):
        with patch("google.genai.Client", return_value=mock_client):
            with patch("time.sleep", return_value=None):
                with caplog.at_level(logging.WARNING):
                    res = decompose_thesis("A distributed trading engine")
                    assert res["source"] == "fallback"
                    assert mock_client.models.generate_content.call_count == 2
                    assert any("gemini: fallback" in msg for msg in caplog.messages)


def test_secret_never_logged(caplog):
    """Hard rule: GEMINI_API_KEY must never appear in logs or error messages."""
    secret = "fake-gemini-secret-test-key-never-logged"
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception(f"Failed with key {secret}")

    with patch.object(settings, "GEMINI_API_KEY", secret):
        with patch("google.genai.Client", return_value=mock_client):
            with patch("time.sleep", return_value=None):
                with caplog.at_level(logging.DEBUG):
                    decompose_thesis("Some thesis")
                    # Assert secret is strictly absent from all logged messages
                    assert secret not in caplog.text


def test_matching_scoring_order():
    """Matching engine orders candidates by synergy_score and percentile descending."""
    db = SessionLocal()
    test_ven_id = "ven_test_score_order"
    test_role_id = "rol_test_score_order"
    try:
        # Create an isolated test venture and vacant role
        ven = models.Venture(
            id=test_ven_id,
            founder_id="usr_founder_01",
            name="Score Order Test Venture",
            thesis="Ultra-fast distributed ledger",
            sector="Enterprise AI & Distributed Systems",
            stage="Sprint 3 / Proof-of-Work",
            clarity_score=92,
            raised_cents=0,
            runway_months=18,
            mrr_cents=0,
            status="active"
        )
        db.add(ven)
        db.flush()

        role = models.SquadRole(
            id=test_role_id,
            venture_id=test_ven_id,
            title="Lead Systems Architect",
            description="Core distributed engine",
            equity_pct=15.0,
            status="vacant",
            requirements=[
                {"skill": "rust", "weight": 1.0},
                {"skill": "distributed systems", "weight": 1.0}
            ]
        )
        db.add(role)
        db.commit()

        matches = run_matching_for_venture(test_ven_id, db)
        assert len(matches) > 0

        # Verify matches are ordered by synergy_score descending
        scores = [m.synergy_score for m in matches]
        assert scores == sorted(scores, reverse=True)
    finally:
        db.query(models.Match).filter_by(venture_id=test_ven_id).delete()
        db.query(models.SquadRole).filter_by(venture_id=test_ven_id).delete()
        db.query(models.Venture).filter_by(id=test_ven_id).delete()
        db.commit()
        db.close()


def test_gemini_rerank_payload_is_strictly_blind():
    """Candidate rerank payload never contains candidate name, email, phone, or avatar."""
    candidates = [
        {
            "workerId": "usr_w1",
            "candidateCode": "TX-ALPHA",
            "name": "Alice RealName",
            "email": "alice@secret.com",
            "phone": "+1-555-0199",
            "avatar": "https://avatar.com/alice.png",
            "skills": ["rust", "distributed systems"],
            "experienceLevel": "senior",
            "percentile": 95.0,
            "synergyScore": 90,
            "fitDetails": {"algorithmicReason": "initial"}
        },
        {
            "workerId": "usr_w2",
            "candidateCode": "TX-BETA",
            "name": "Bob RealName",
            "email": "bob@secret.com",
            "phone": "+1-555-0188",
            "avatar": "https://avatar.com/bob.png",
            "skills": ["go", "kubernetes operator"],
            "experienceLevel": "mid",
            "percentile": 88.0,
            "synergyScore": 82,
            "fitDetails": {"algorithmicReason": "initial"}
        }
    ]

    captured_prompt = None

    def fake_generate_content(*args, **kwargs):
        nonlocal captured_prompt
        captured_prompt = kwargs.get("contents", "")
        mock_res = MagicMock()
        mock_res.text = json.dumps({
            "ranked_candidates": [
                {"candidate_code": "TX-BETA", "reason": "Better fit for specific role"},
                {"candidate_code": "TX-ALPHA", "reason": "Great overall experience"}
            ]
        })
        return mock_res

    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = fake_generate_content

    with patch.object(settings, "GEMINI_RERANK", True):
        with patch.object(settings, "GEMINI_API_KEY", "test-key"):
            with patch("google.genai.Client", return_value=mock_client):
                reranked = gemini_rerank(
                    candidates,
                    role_title="Founding Engineer",
                    role_requirements={"rust": 1.0}
                )

                # 1. Assert captured prompt sent to Gemini does NOT contain any private info
                assert captured_prompt is not None
                assert "Alice RealName" not in captured_prompt
                assert "alice@secret.com" not in captured_prompt
                assert "+1-555-0199" not in captured_prompt
                assert "avatar.com" not in captured_prompt
                assert "usr_w1" not in captured_prompt

                # 2. Assert candidate codes were properly passed and re-ordered
                assert reranked[0]["candidateCode"] == "TX-BETA"
                assert reranked[1]["candidateCode"] == "TX-ALPHA"


def test_gemini_rerank_ignores_unknown_codes():
    """If Gemini returns hallucinated or unknown candidate codes, ignore them and keep candidates safe."""
    candidates = [
        {
            "workerId": "usr_w1",
            "candidateCode": "TX-ALPHA",
            "skills": ["rust"],
            "experienceLevel": "senior",
            "percentile": 95.0,
            "synergyScore": 90,
            "fitDetails": {"algorithmicReason": "initial"}
        }
    ]

    mock_res = MagicMock()
    mock_res.text = json.dumps({
        "ranked_candidates": [
            {"candidate_code": "TX-HALLUCINATED", "reason": "Not a real candidate"},
            {"candidate_code": "TX-ALPHA", "reason": "Legit candidate"}
        ]
    })
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_res

    with patch.object(settings, "GEMINI_RERANK", True):
        with patch.object(settings, "GEMINI_API_KEY", "test-key"):
            with patch("google.genai.Client", return_value=mock_client):
                reranked = gemini_rerank(candidates, "Role", {"rust": 1.0})
                codes = [c["candidateCode"] for c in reranked]
                assert "TX-HALLUCINATED" not in codes
                assert codes == ["TX-ALPHA"]


def test_api_routes_decompose_and_approve(client, founder_token):
    """End-to-end API test: decompose -> approve -> get matches on an isolated test venture."""
    db = SessionLocal()
    test_ven_id = "ven_test_decompose_api"
    try:
        ven = models.Venture(
            id=test_ven_id,
            founder_id="usr_founder_01",
            name="Decompose Test Venture",
            thesis="Ultra-low-latency financial matching engine on bare metal",
            sector="Enterprise AI & Distributed Systems",
            stage="Sprint 3 / Proof-of-Work",
            clarity_score=85,
            raised_cents=0,
            runway_months=18,
            mrr_cents=0,
            status="active"
        )
        db.add(ven)
        db.commit()

        # 1. Decompose
        dec_res = client.post(
            f"/api/v1/ventures/{test_ven_id}/decompose",
            json={"thesis": "Ultra-low-latency financial matching engine on bare metal"},
            headers={"Authorization": f"Bearer {founder_token}"}
        )
        assert dec_res.status_code == 200
        dec_data = dec_res.json()
        assert "blueprint" in dec_data
        assert "clarityScore" in dec_data
        assert "constraints" in dec_data
        assert len(dec_data["blueprint"]) >= 3

        # 2. Approve blueprint
        app_res = client.post(
            f"/api/v1/ventures/{test_ven_id}/blueprint/approve",
            json={"blueprint": dec_data["blueprint"]},
            headers={"Authorization": f"Bearer {founder_token}"}
        )
        assert app_res.status_code == 200
        app_data = app_res.json()
        assert app_data["rolesCount"] == len(dec_data["blueprint"])

        # 3. Get matches - verify blind protocol
        mat_res = client.get(
            f"/api/v1/ventures/{test_ven_id}/matches",
            headers={"Authorization": f"Bearer {founder_token}"}
        )
        assert mat_res.status_code == 200
        mat_data = mat_res.json()
        assert len(mat_data["items"]) > 0

        for match in mat_data["items"]:
            assert match["candidateCode"].startswith("TX-") or match["candidateCode"].startswith("NODE-")
            assert match["name"].startswith("Candidate #")
            assert match.get("contact") is None
            assert match.get("avatar") is None
            assert match["isCloaked"] is True
    finally:
        db.query(models.Match).filter_by(venture_id=test_ven_id).delete()
        db.query(models.SquadRole).filter_by(venture_id=test_ven_id).delete()
        db.query(models.AuditLog).filter_by(entity_id=test_ven_id).delete()
        db.query(models.Venture).filter_by(id=test_ven_id).delete()
        db.commit()
        db.close()
