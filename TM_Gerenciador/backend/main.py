from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import contratos, ordens, notificacoes, usuarios

app = FastAPI(
    title="TM Gerenciador API",
    description="API de Gestão de Ordens de Serviço — TM Sempre Tecnologia",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contratos.router)
app.include_router(ordens.router)
app.include_router(notificacoes.router)
app.include_router(usuarios.router)


@app.get("/health")
def health():
    return {"status": "ok", "app": "TM Gerenciador API", "version": "1.0.0"}


@app.get("/")
def root():
    return {
        "app": "TM Gerenciador API",
        "docs": "/docs",
        "health": "/health",
        "endpoints": [
            "GET  /api/contratos",
            "GET  /api/contratos/{id}",
            "GET  /api/contratos/{id}/items  (proxy AutoRelatório V5)",
            "GET  /api/ordens",
            "GET  /api/ordens/kpis",
            "POST /api/ordens",
            "POST /api/ordens/importar",
            "GET  /api/notificacoes",
            "GET  /api/usuarios",
        ],
    }
