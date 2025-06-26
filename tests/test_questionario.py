import pytest

@pytest.fixture
def auth_header(client):
    # cria um nutricionista para criar templates
    client.post("/auth/register", json={
        "username": "nutri", "password": "nutri123", "role": "nutricionista"
    })
    login = client.post("/auth/token", data={
        "username": "nutri", "password": "nutri123"
    }).json()
    return {"Authorization": f"Bearer {login['access_token']}"}

def test_create_and_list_template(client, auth_header):
    payload = {
      "title":"Diabetes","questions":[
        {"order":1,"text":"Idade","options":[
            {"text":"<45","score":0},{"text":"45–54","score":2}
        ]}
      ]
    }
    # cria
    r = client.post("/questionarios/templates", json=payload, headers=auth_header)
    assert r.status_code == 201
    tpl = r.json()
    assert tpl["title"] == "Diabetes"
    # lista
    r = client.get("/questionarios/templates", headers=auth_header)
    assert r.status_code == 200
    assert len(r.json()) >= 1

def test_score_calculation_and_save_report(client, auth_header):
    # supõe template id=1 já criado
    # registra paciente
    client.post("/auth/register", json={
        "username":"pac","password":"pac123","role":"paciente"
    })
    pac_login = client.post("/auth/token", data={
        "username":"pac","password":"pac123"
    }).json()
    # responde
    answers = [{"question_id":1,"option_id":2}]
    r = client.post("/questionarios/1/respostas", json={"answers":answers},
                    headers={"Authorization":f"Bearer {pac_login['access_token']}"})
    assert r.status_code == 200
    res = r.json()
    assert "total_score" in res and "interpretation" in res
    # nutricionista consulta relatório
    r = client.get("/nutricionistas/1/relatorios", headers=auth_header)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
