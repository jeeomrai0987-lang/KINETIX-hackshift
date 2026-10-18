from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"


def test_demo_login_founder():
    res = client.post("/api/v1/auth/demo/founder")
    assert res.status_code == 200
    data = res.json()
    assert "token" in data
    assert data["user"]["role"] == "founder"
    assert data["user"]["email"] == "alex.mercer@synthetix.ai"


def test_demo_login_worker():
    res = client.post("/api/v1/auth/demo/worker")
    assert res.status_code == 200
    data = res.json()
    assert "token" in data
    assert data["user"]["role"] == "worker"
    assert data["user"]["email"] == "elena.vance@startup.io"


def test_demo_login_investor():
    res = client.post("/api/v1/auth/demo/investor")
    assert res.status_code == 200
    data = res.json()
    assert "token" in data
    assert data["user"]["role"] == "investor"
    assert data["user"]["email"] == "marcus.vance@angelsyndicate.vc"


def test_blind_protocol_on_matches():
    # Login as founder
    f_res = client.post("/api/v1/auth/demo/founder")
    token = f_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch matches
    res = client.get("/api/v1/ventures/ven_synthetix/matches", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    for match in data["items"]:
        if match["isCloaked"]:
            # Blind protocol: must NOT leak real name or email or phone
            assert match["avatar"] is None
            assert match["contact"] is None
            assert match["name"].startswith("Candidate #")


def test_founder_financials_and_cap_table():
    f_res = client.post("/api/v1/auth/demo/founder")
    token = f_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/ventures/ven_synthetix/financials", headers=headers)
    assert res.status_code == 200
    fin = res.json()
    assert "monthlyBurnCents" in fin
    assert "snapshots" in fin

    cap_res = client.get("/api/v1/ventures/ven_synthetix/cap-table", headers=headers)
    assert cap_res.status_code == 200
    cap = cap_res.json()
    # Cap table integrity: sum must be 100.0%
    assert abs(cap["totalEquity"] - 100.0) < 0.001


def test_worker_endpoints():
    w_res = client.post("/api/v1/auth/demo/worker")
    token = w_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    dash = client.get("/api/v1/worker/dashboard", headers=headers)
    assert dash.status_code == 200

    invs = client.get("/api/v1/worker/invitations", headers=headers)
    assert invs.status_code == 200
    assert len(invs.json()["items"]) >= 1

    pow_res = client.get("/api/v1/worker/proof-of-work", headers=headers)
    assert pow_res.status_code == 200
    assert "merkleRoot" in pow_res.json()


def test_investor_endpoints():
    i_res = client.post("/api/v1/auth/demo/investor")
    token = i_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    dash = client.get("/api/v1/investor/dashboard", headers=headers)
    assert dash.status_code == 200

    port = client.get("/api/v1/investor/portfolio", headers=headers)
    assert port.status_code == 200
    assert len(port.json()["items"]) >= 1


if __name__ == "__main__":
    print("Running backend tests...")
    test_health()
    print("[PASS] test_health passed")
    test_demo_login_founder()
    print("[PASS] test_demo_login_founder passed")
    test_demo_login_worker()
    print("[PASS] test_demo_login_worker passed")
    test_demo_login_investor()
    print("[PASS] test_demo_login_investor passed")
    test_blind_protocol_on_matches()
    print("[PASS] test_blind_protocol_on_matches passed")
    test_founder_financials_and_cap_table()
    print("[PASS] test_founder_financials_and_cap_table passed")
    test_worker_endpoints()
    print("[PASS] test_worker_endpoints passed")
    test_investor_endpoints()
    print("[PASS] test_investor_endpoints passed")
    print("ALL TESTS PASSED SUCCESSFULLY!")

