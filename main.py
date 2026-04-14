
import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Aula 07 - Webhook API")

WEBHOOK_TOKEN = os.getenv("WEBHOOK_TOKEN", "segredo123")


class EventoCadastro(BaseModel):
    evento: str
    usuario: str
    email: str


@app.get("/")
def inicio():
    return {
        "mensagem": "API da aula funcionando",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/webhook")
def receber_webhook(
    dados: EventoCadastro,
    authorization: str | None = Header(default=None),
):
    esperado = f"Bearer {WEBHOOK_TOKEN}"

    if authorization != esperado:
        raise HTTPException(status_code=401, detail="Token inválido")

    acao_executada = f"Cadastro recebido para {dados.usuario} ({dados.email})"

    return {
        "status": "sucesso",
        "evento_recebido": dados.evento,
        "acao": acao_executada,
    }