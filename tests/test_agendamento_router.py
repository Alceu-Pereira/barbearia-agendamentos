import pytest

@pytest.fixture
def cenario_base(client):
    cliente = client.post(
        "/api/v1/clientes",
        json = {
            "nome": "Cliente_Teste",
            "telefone": "5512345678",
        },
    )

    barbeiro = client.post(
        "/api/v1/barbeiros",
        json = {
            "nome": "Barbeiro_Teste",
            "telefone": "5587654321",
        },
    )

    servico = client.post(
        "/api/v1/servicos",
        json = {
            "nome": "Barba",
            "duracao_minutos": 30,
            "preco": "35.00",
        },
    )

    return {
        "cliente_id": cliente.json()["id"],
        "barbeiro_id": barbeiro.json()["id"],
        "servico_id": servico.json()["id"],
    }



class TestCriarAgendamento:

    def test_criar_agendamento(self, client, cenario_base):
        cliente = cenario_base["cliente_id"]

        barbeiro = cenario_base["barbeiro_id"]

        servico = cenario_base["servico_id"]

        agendamento = client.post(
            "/api/v1/agendamentos",
            json={
                "cliente_id": cliente,
                "barbeiro_id": barbeiro,
                "servico_id": servico,
                "data_hora_inicio": "2026-09-18 10:00"
            }
        )

        assert agendamento.status_code == 200
        assert agendamento.json()["status"] == "PENDENTE"
        assert agendamento.json()["preco_cobrado"] == "35.00"
        assert agendamento.json()["data_hora_fim"] == "2026-09-18T10:30:00"


    def test_criar_agendamento_recurso_nao_encontrado(self, client):
        agendamento = client.post(
                "/api/v1/agendamentos",
                json={
                    "cliente_id": "9999",
                    "barbeiro_id": "9999",
                    "servico_id": "9999",
                    "data_hora_inicio": "2026-09-18 10:00"
                }
            )

        assert agendamento.status_code == 404


    def test_criar_agendamento_conflito_horario(self, client, cenario_base):
        cliente = cenario_base["cliente_id"]

        barbeiro = cenario_base["barbeiro_id"]

        servico = cenario_base["servico_id"]

        agendamento = client.post(
            "/api/v1/agendamentos",
            json={
                "cliente_id": cliente,
                "barbeiro_id": barbeiro,
                "servico_id": servico,
                "data_hora_inicio": "2026-09-18 10:00"
            }
        )

        agendamento_sobreposto = client.post(
                "/api/v1/agendamentos",
                json={
                    "cliente_id": cliente,
                    "barbeiro_id": barbeiro,
                    "servico_id": servico,
                    "data_hora_inicio": "2026-09-18 10:15"
                }
            )

        assert agendamento_sobreposto.status_code == 409