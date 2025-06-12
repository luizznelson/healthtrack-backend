import pytest

def test_register_and_login(client):
    # cadastro
    resp = client.post("/auth/register", json={
        "username": "teste", "password": "pass123", "role": "paciente"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "teste"
    assert data["role"] == "paciente"

    # login
    resp = client.post("/auth/token", data={
        "username": "teste", "password": "pass123"
    })
    assert resp.status_code == 200
    tokens = resp.json()
    assert "access_token" in tokens and "refresh_token" in tokens

    # me
    access = tokens["access_token"]
    resp = client.get("/auth/me", headers={"Authorization": f"Bearer {access}"})
    assert resp.status_code == 200
    assert resp.json()["username"] == "teste"
