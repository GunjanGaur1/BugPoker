from fastapi.testclient import TestClient
from app.main import app

def test_health():
    client = TestClient(app)
    assert client.get("/healthz").json()["status"] == "ok"

def test_create_and_read_game():
    client = TestClient(app)
    created = client.post("/games", json={"seed": 12})
    assert created.status_code == 200
    game_id = created.json()["id"]
    fetched = client.get(f"/games/{game_id}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == game_id
