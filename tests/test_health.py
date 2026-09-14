def test_health_check(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "Ok"}