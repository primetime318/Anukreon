import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, sims

app = FastAPI(title="Anukreon Sim API (v2)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(sims.router)
