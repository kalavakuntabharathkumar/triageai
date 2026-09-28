from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_health(): assert client.get("/health").json()["status"]=="ok"

def test_create_and_triage():
    r=client.post("/tickets",json={"customer_id":"CUST-1001","subject":"Cannot login","description":"Password reset email never arrives","channel":"email"})
    assert r.status_code==200
    tid=r.json()["id"]; out=client.post(f"/tickets/{tid}/triage")
    assert out.status_code==200 and out.json()["team"]=="Identity & Access"
    assert len(out.json()["tools_used"])==7
