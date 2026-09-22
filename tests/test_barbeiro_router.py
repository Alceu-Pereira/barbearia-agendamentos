def test_criar_barbeiro(client):
    response = client.post("/api/v1/barbeiros", json={"nome": "Teste", "telefone": "5512345678"})
    assert response.status_code == 200
    assert response.json() == {
                               "id": 1, 
                               "nome": "Teste", 
                               "telefone": "5512345678",
                               "ativo": True
                               }



def test_buscar_barbeiro_por_id_inexistente(client):
    response = client.get("/api/v1/barbeiros/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Barbeiro não encontrado."}



def test_buscar_barbeiro_por_id_existente(client):
    barbeiro = client.post(
        "/api/v1/barbeiros/", json={"nome": "Teste", "telefone": "5512345678"}
    )
    response = client.get(f"/api/v1/barbeiros/{barbeiro.json()["id"]}")
    assert response.status_code == 200
    assert response.json() == {
        "id": barbeiro.json()["id"],
        "nome": "Teste",
        "telefone": "5512345678",
        "ativo": True
    }

def test_listar_barbeiros_ativos(client):
    barbeiro_1 = client.post(
        "/api/v1/barbeiros/",
        json={
            "nome": "Teste", 
            "telefone": "5512345678"
        }
    )

    barbeiro_2 = client.post(
            "/api/v1/barbeiros/",
            json={
                "nome": "Teste2", 
                "telefone": "5512345678"
            }
        )

    barbeiro_3 = client.post(
            "/api/v1/barbeiros/",
            json={
                "nome": "Teste3", 
                "telefone": "5512345678"
            }
        )

    response = client.get(
        "/api/v1/barbeiros"
    )

    assert response.status_code == 200
    assert len(response.json()) == 3