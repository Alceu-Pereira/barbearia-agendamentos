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


class TestListarDisponibilidade:
    def test_listar_disponibilidade(self, client, cenario_base):
        barbeiro = cenario_base["barbeiro_id"]

        disponibilidade = client.get(
            "/api/v1/agendamentos/disponibilidade",
            params={
                "barbeiro_id": barbeiro,
                "data": "2026-09-19"
            },
        )

        assert disponibilidade.status_code == 200
        assert len(disponibilidade.json()) == 20
    

    def test_listar_disponibilidade_barbeiro_inexistente(self, client):
        disponibilidade = client.get(
            "/api/v1/agendamentos/disponibilidade",
            params={
                "barbeiro_id": 9999,
                "data": "2026-09-19",
            },
        )

        assert disponibilidade.status_code == 404

class TestCancelarAgendamento:
    def test_cancelar_agendamento(self, client, cenario_base):
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

        response = client.patch(
            f"/api/v1/agendamentos/{agendamento.json()["id"]}/cancelar"
        )

        assert response.status_code == 200
        assert response.json()["status"] == "CANCELADO"
        

    def test_cancelar_agendamento_inexistente(self, client):
        response = client.patch(
                    "/api/v1/agendamentos/999/cancelar"
                )
        
        assert response.status_code == 404

    def test_cancelar_agendamento_ja_cancelado(self, client, cenario_base):
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
        
        cancelamento_1 = client.patch(
            f"/api/v1/agendamentos/{agendamento.json()["id"]}/cancelar"
            )

        cancelamento_2 = client.patch(
            f"/api/v1/agendamentos/{agendamento.json()["id"]}/cancelar"
            )

        assert cancelamento_1.status_code == 200
        assert cancelamento_2.status_code == 400