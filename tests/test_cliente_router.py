def test_criar_cliente(client):
    response = client.post(
        "/api/v1/clientes",
        json={"nome": "Teste", "telefone": "5512345678"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "nome": "Teste",
        "telefone": "5512345678",
        "ativo": True,
    }

def test_buscar_cliente_por_id_inexistente(client):
    response = client.get(
       "/api/v1/clientes/9999"
    )
    assert response.status_code == 404
    assert response.json() == { "detail": "Cliente não encontrado" }

def test_buscar_cliente_por_id_existente(client):
    cliente = client.post(
        "/api/v1/clientes",
        json={"nome": "Teste", "telefone": "5512345678"},
    )
    response = client.get(
        f"/api/v1/clientes/{cliente.json()["id"]}"
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": cliente.json()["id"],
        "nome": "Teste",
        "telefone": "5512345678",
        "ativo": True,
        }