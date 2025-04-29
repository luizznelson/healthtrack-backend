def test_register_and_login(client):
    # Register
    resp = client.post("/auth/register", json={
        "name": "Teste",
        "email": "t@t.com",
        "password": "abc123",
        "role": "patient"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "t@t.com"

    # Login
    resp = client.post("/auth/login", data={
        "username": "t@t.com",
        "password": "abc123"
    })
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    assert token

    # Protected endpoint
    resp = client.get("/auth/users/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "t@t.com"
