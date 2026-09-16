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
