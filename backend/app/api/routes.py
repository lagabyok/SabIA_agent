from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.core.config import settings
from app.storage.db import get_latest_run, list_runs, get_run
from app.jobs.pipeline import run_all
from app.llm.openai_provider import OpenAIProvider
from app.llm.gemini_provider import GeminiProvider

router = APIRouter()

class RunRequest(BaseModel):
    periodo: str  # "YYYY-MM"
    llm: Optional[str] = None  # "openai" | "gemini" | None

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/run")
def run(req: RunRequest) -> Dict[str, Any]:
    llm_provider = None
    if req.llm == "openai":
        llm_provider = OpenAIProvider()
    elif req.llm == "gemini":
        llm_provider = GeminiProvider()

    output = run_all(
        data_dir=settings.DATA_DIR,
        db_path=settings.DB_PATH,
        periodo=req.periodo,
        valor_minuto=settings.VALOR_MINUTO,
        margen_critico_pct=settings.MARGEN_CRITICO_PCT,
        margen_objetivo_pct=settings.MARGEN_OBJETIVO_PCT,
        esfuerzo_alto_min=settings.ESFUERZO_ALTO_MIN,
        top_drivers=settings.TOP_DRIVERS,
        llm_provider=llm_provider
    )
    return output

@router.get("/runs/latest")
def latest():
    out = get_latest_run(settings.DB_PATH)
    if not out:
        raise HTTPException(status_code=404, detail="No hay corridas aún. Ejecuta POST /run.")
    return out

@router.get("/runs")
def runs(limit: int = 20):
    return {"runs": list_runs(settings.DB_PATH, limit=limit)}

@router.get("/runs/{run_id}")
def run_by_id(run_id: str):
    out = get_run(settings.DB_PATH, run_id)
    if not out:
        raise HTTPException(status_code=404, detail="run_id no encontrado")
    return out
