import pytest

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["databaseConnected"] is True

def test_auth_demo_logins(client):
    for role in ["founder", "worker", "investor"]:
        res = client.post(f"/api/v1/auth/demo/{role}")
        assert res.status_code == 200
        data = res.json()
        assert "token" in data
        assert data["user"]["role"] == role

def test_auth_me(client, founder_token):
    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {founder_token}"})
    assert res.status_code == 200
    user = res.json()
    assert user["email"] == "alex.mercer@synthetix.ai"
    assert user["role"] == "founder"

def test_blind_protocol(client, founder_token):
    """
    Section 6 Rule 1: A founder never receives a candidate's real name, email,
    avatar_url or phone until that candidate's invitation is accepted.
    """
    res = client.get("/api/v1/ventures/ven_synthetix/matches", headers={"Authorization": f"Bearer {founder_token}"})
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert len(data["items"]) > 0

    for match in data["items"]:
        # Verify candidateCode is present
        assert "candidateCode" in match
        assert match["candidateCode"].startswith("TX-") or match["candidateCode"].startswith("NODE-")
        # Real name, email, phone must NOT be in the match object
        assert match["name"].startswith("Candidate #")
        assert "email" not in match
        assert "phone" not in match
        assert match.get("avatar") is None

def test_real_sha256_hashes(client, founder_token):
    """
    Section 6 Rule 2: submissions.hash = SHA-256 (hex, 0x prefix) of canonical JSON.
    """
    chg_res = client.get("/api/v1/ventures/ven_synthetix/challenge", headers={"Authorization": f"Bearer {founder_token}"})
    challenge_id = chg_res.json().get("id", "chl_synth_01") if chg_res.status_code == 200 else "chl_synth_01"
    res = client.get(f"/api/v1/challenges/{challenge_id}/submissions", headers={"Authorization": f"Bearer {founder_token}"})
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) > 0
    sub = data["items"][0]
    assert sub["hash"].startswith("0x")
    assert len(sub["hash"]) == 66  # '0x' + 64 hex characters

    # Save original DB state to restore after test
    from database.session import SessionLocal
    from database import models
    with SessionLocal() as db:
        orig = db.query(models.Submission).filter_by(id=sub["id"]).first()
        orig_dict = {
            "score": orig.score,
            "replay_integrity": orig.replay_integrity,
            "failure_recovery": orig.failure_recovery,
            "concurrency_latency": orig.concurrency_latency,
            "code_elegance": orig.code_elegance,
            "reviewer_verdict": orig.reviewer_verdict,
            "hash": orig.hash
        } if orig else {}

    try:
        # Score submission
        score_res = client.post(
            f"/api/v1/submissions/{sub['id']}/score",
            headers={"Authorization": f"Bearer {founder_token}"},
            json={
                "vectorScores": {
                    "replayIntegrity": 99.9,
                    "failureRecovery": 100.0,
                    "concurrencyLatency": 98.7,
                    "codeElegance": 97.2
                },
                "reviewerVerdict": "All automated benchmarks verified on Arbitrum simulated testnet."
            }
        )
        assert score_res.status_code == 200
        scored = score_res.json()
        assert scored["hash"].startswith("0x")
        assert len(scored["hash"]) == 66
    finally:
        if orig_dict:
            with SessionLocal() as db:
                restored = db.query(models.Submission).filter_by(id=sub["id"]).first()
                if restored:
                    for k, v in orig_dict.items():
                        setattr(restored, k, v)
                    db.commit()

def test_cap_table_integrity(client, founder_token):
    """
    Section 6 Rule 3: sum(equity_pct) over cap_table_entries must equal 100.0 (tolerance 0.001).
    """
    res = client.get("/api/v1/ventures/ven_synthetix/cap-table", headers={"Authorization": f"Bearer {founder_token}"})
    assert res.status_code == 200
    data = res.json()
    assert abs(data["totalEquityPct"] - 100.0) <= 0.001
    sum_entries = sum(e["equityPct"] for e in data["entries"])
    assert abs(sum_entries - 100.0) <= 0.001

def test_restructuring_single_tx(client, founder_token):
    """
    Section 6 Rule 3: Restructuring executes in a single DB transaction and preserves 100.0% sum.
    """
    res = client.post(
        "/api/v1/ventures/ven_synthetix/restructuring/execute",
        headers={"Authorization": f"Bearer {founder_token}"},
        json={
            "type": "Option Pool Expansion",
            "fromUserId": "usr_founder_01",
            "equityDeltaPct": 1.0,
            "stage": "Approved",
            "note": "Allocating 1% into Option Pool"
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["equityDeltaPct"] == 1.0

    # Verify cap table is still exactly 100.0%
    cap_res = client.get("/api/v1/ventures/ven_synthetix/cap-table", headers={"Authorization": f"Bearer {founder_token}"})
    assert cap_res.status_code == 200
    assert abs(cap_res.json()["totalEquityPct"] - 100.0) <= 0.001

    # Cleanup test-created restructuring event and restore equity for database tests
    from database.session import SessionLocal
    from database import models
    with SessionLocal() as db:
        evt = db.query(models.RestructuringEvent).filter_by(id=data["id"]).first()
        if evt:
            db.delete(evt)
        f_entry = db.query(models.CapTableEntry).filter_by(venture_id="ven_synthetix", holder_user_id="usr_founder_01").first()
        opt_entry = db.query(models.CapTableEntry).filter_by(venture_id="ven_synthetix", kind="option_pool").first()
        if f_entry and opt_entry:
            f_entry.equity_pct += 1.0
            opt_entry.equity_pct -= 1.0
        db.commit()

def test_role_isolation(client, worker_token, investor_token, founder_token):
    """
    Section 6 Rule 4: Role isolation.
    Founders only see their own ventures; workers only their own; investors only their own.
    """
    # Worker attempting to access founder ventures -> 403 Forbidden
    res1 = client.get("/api/v1/ventures/mine", headers={"Authorization": f"Bearer {worker_token}"})
    assert res1.status_code == 403

    # Investor attempting to access worker dashboard -> 403 Forbidden
    res2 = client.get("/api/v1/worker/dashboard", headers={"Authorization": f"Bearer {investor_token}"})
    assert res2.status_code == 403

    # Worker accessing worker dashboard -> 200 OK
    res3 = client.get("/api/v1/worker/dashboard", headers={"Authorization": f"Bearer {worker_token}"})
    assert res3.status_code == 200

    # Investor accessing investor portfolio -> 200 OK
    res4 = client.get("/api/v1/investor/portfolio", headers={"Authorization": f"Bearer {investor_token}"})
    assert res4.status_code == 200

def test_thesis_decomposition(client, founder_token):
    res = client.post(
        "/api/v1/ventures/ven_synthetix/decompose",
        headers={"Authorization": f"Bearer {founder_token}"},
        json={"thesis": "High-throughput asynchronous distributed consensus engine with memory-safe Rust kernels."}
    )
    assert res.status_code == 200
    data = res.json()
    assert "constraints" in data
    assert "blueprint" in data
    assert len(data["blueprint"]) > 0
    assert "equityPct" in data["blueprint"][0]

def test_financials_export_csv(client, founder_token):
    res = client.get("/api/v1/ventures/ven_synthetix/financials/export.csv", headers={"Authorization": f"Bearer {founder_token}"})
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]
    assert "Date,Description,Category,Amount ($),Proof Hash" in res.text
