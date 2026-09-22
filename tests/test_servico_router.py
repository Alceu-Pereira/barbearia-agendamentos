def test_criar_servico(client):
    response = client.post(
        "/api/v1/servicos", 
        json={
            "nome": "servico_teste",
            "duracao_minutos": 15,
            "preco": "15.55"
        }
        )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "nome": "servico_teste",
        "duracao_minutos": 15,
        "preco": "15.55",
        "ativo": True,
    }

def test_buscar_servico_por_id_inexistente(client):
    response = client.get("/api/v1/servicos/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Serviço não encontrado."}


def test_buscar_servico_por_id_existente(client):
    servico = client.post(
        "/api/v1/servicos", 
        json={
            "nome": "servico_teste",
            "duracao_minutos": 15,
            "preco": "15.55"
        }
        )

    response = client.get(f"/api/v1/servicos/{servico.json()["id"]}")
    assert response.status_code == 200
    assert response.json() == {
        "id": servico.json()["id"],
        "nome": "servico_teste",
        "duracao_minutos": 15,
        "preco": "15.55",
        "ativo": True,
    }

def test_listar_servicos_ativos(client):
    servico_1 = client.post(
            "/api/v1/servicos", 
            json={
                "nome": "servico_teste1",
                "duracao_minutos": 15,
                "preco": "15.55"
            }
            )

    servico_2 = client.post(
                "/api/v1/servicos", 
                json={
                    "nome": "servico_teste2",
                    "duracao_minutos": 15,
                    "preco": "15.55"
                }
                )

    servico_3 = client.post(
                "/api/v1/servicos", 
                json={
                    "nome": "servico_teste3",
                    "duracao_minutos": 15,
                    "preco": "15.55"
                }
                )
    response = client.get(
        "api/v1/servicos"
    )

    assert response.status_code == 200
    assert len(response.json()) == 3