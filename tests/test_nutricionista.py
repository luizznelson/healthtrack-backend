def test_patient_cannot_create_template(client):
    # cadastra paciente
    client.post("/auth/register", json={
        "username":"p","password":"p123","role":"paciente"
    })
    tok = client.post("/auth/token", data={
        "username":"p","password":"p123"
    }).json()
    # tenta criar template
    r = client.post("/questionarios/templates", json={}, 
                    headers={"Authorization":f"Bearer {tok['access_token']}"})
    assert r.status_code == 403  # proibido

def test_nutri_only_access_dashboard(client):
    # cadastra paciente e nutrit
    client.post("/auth/register", json={"username":"n","password":"n123","role":"nutricionista"})
    nut = client.post("/auth/token", data={"username":"n","password":"n123"}).json()
    client.post("/auth/register", json={"username":"p2","password":"p2123","role":"paciente"})
    pac = client.post("/auth/token", data={"username":"p2","password":"p2123"}).json()
    # paciente não vê painel
    r = client.get("/nutricionistas/1/relatorios", headers={"Authorization":f"Bearer {pac['access_token']}"})
    assert r.status_code == 403
    # nutricionista vê
    r = client.get("/nutricionistas/1/relatorios", headers={"Authorization":f"Bearer {nut['access_token']}"})
    assert r.status_code == 200
