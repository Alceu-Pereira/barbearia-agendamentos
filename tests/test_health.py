def test_health_check(client):
    resposta = client.get("/")
    print(resposta)
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "Ok"}