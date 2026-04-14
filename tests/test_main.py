from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


PAYLOAD = {
    "evento": "novo_cadastro",
    "usuario": "Ana Silva",
    "email": "ana@email.com",
}


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["mensagem"] == "API da aula funcionando"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_webhook_success():
    response = client.post(
        "/webhook",
        headers={"Authorization": "Bearer segredo123"},
        json=PAYLOAD,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "sucesso"
    assert body["evento_recebido"] == "novo_cadastro"


def test_webhook_invalid_token():
    response = client.post(
        "/webhook",
        headers={"Authorization": "Bearer token_errado"},
        json=PAYLOAD,
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Token inválido"}


def test_webhook_missing_field():
    response = client.post(
        "/webhook",
        headers={"Authorization": "Bearer segredo123"},
        json={
            "evento": "novo_cadastro",
            "usuario": "Ana Silva",
        },
    )
    assert response.status_code == 422