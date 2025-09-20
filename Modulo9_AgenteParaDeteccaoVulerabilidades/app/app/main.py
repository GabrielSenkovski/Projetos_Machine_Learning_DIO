# app/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from .api import router

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI(
    title="STRIDE Threat Analysis API",
    description="Uma API que usa IA para analisar diagramas de arquitetura e gerar um Threat Model com base na metodologia STRIDE.",
    version="1.0.0"
)

# Inclui o roteador com o endpoint
app.include_router(router, prefix="/v1", tags=["Analysis"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API de Análise de Ameaças STRIDE."}