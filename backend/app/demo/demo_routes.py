"""
Endpoints demo para las historias de demostración.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, Any
import logging
import uuid

from app.demo.demo_data import (
    STORY_1_DATA,
    STORY_2_DATA,
    STORY_3_DATA,
    STORY_4_DATA,
    STORY_5_DATA,
    STORY_6_DATA
)
from app.demo.real_stories import (
    extract_story_1_ranking,
    extract_story_2_tiempo_margen,
    extract_story_3_alertas,
    extract_story_4_drivers
)
from app.demo.csv_parser import parse_productos_csv, parse_tiempo_csv
from app.core.config import settings
from app.jobs.pipeline import run_all
from app.llm.gemini_provider import GeminiProvider

logger = logging.getLogger(__name__)
demo_router = APIRouter(prefix="/demo", tags=["demo"])

# ===== STORIES SIMULADAS (MOCK) =====

@demo_router.get("/story/1")
def story_1() -> Dict[str, Any]:
    """
    Historia 1: Ranking de productos por margen real (SIMULADO)
    ¿Qué productos realmente me dejan dinero?
    """
    logger.info("=== GET /demo/story/1 (mock) ===")
    return STORY_1_DATA

@demo_router.get("/story/2")
def story_2() -> Dict[str, Any]:
    """
    Historia 2: Tiempo de producción vs Margen (SIMULADO)
    ¿Qué productos me quitan mucho tiempo con poco retorno?
    """
    logger.info("=== GET /demo/story/2 (mock) ===")
    return STORY_2_DATA

@demo_router.get("/story/3")
def story_3() -> Dict[str, Any]:
    """
    Historia 3: Alertas simples (SIMULADO)
    Productos con problemas que requieren acción
    """
    logger.info("=== GET /demo/story/3 (mock) ===")
    return STORY_3_DATA

@demo_router.get("/story/4")
def story_4() -> Dict[str, Any]:
    """
    Historia 4: Drivers de costos (SIMULADO)
    ¿Dónde enfocar ajustes?
    """
    logger.info("=== GET /demo/story/4 (mock) ===")
    return STORY_4_DATA

@demo_router.get("/story/5")
def story_5() -> Dict[str, Any]:
    """
    Historia 5: Sensibilidad de costos (Agente A - SIMULADO)
    Top drivers por insumo + sensibilidad a cambios de precio
    """
    logger.info("=== GET /demo/story/5 (mock) ===")
    return STORY_5_DATA

@demo_router.get("/story/6")
def story_6() -> Dict[str, Any]:
    """
    Historia 6: Recomendaciones de Pricing (Agente 2 - SIMULADO)
    Impacto económico e prioridad de acción
    """
    logger.info("=== GET /demo/story/6 (mock) ===")
    return STORY_6_DATA

# ===== STORIES REALES (usando pipeline) =====

@demo_router.get("/real/story/1")
def real_story_1(periodo: str = "2024-01") -> Dict[str, Any]:
    """
    Historia 1: Ranking por margen (REAL - desde pipeline)
    """
    logger.info(f"=== GET /demo/real/story/1 - periodo: {periodo} ===")
    try:
        output = run_all(
            data_dir=settings.DATA_DIR,
            db_path=settings.DB_PATH,
            periodo=periodo,
            valor_minuto=settings.VALOR_MINUTO,
            margen_critico_pct=settings.MARGEN_CRITICO_PCT,
            margen_objetivo_pct=settings.MARGEN_OBJETIVO_PCT,
            esfuerzo_alto_min=settings.ESFUERZO_ALTO_MIN,
            top_drivers=settings.TOP_DRIVERS,
            llm_provider=None
        )
        return extract_story_1_ranking(output)
    except Exception as e:
        logger.error(f"Error generando H1 real: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@demo_router.get("/real/story/2")
def real_story_2(periodo: str = "2024-01") -> Dict[str, Any]:
    """
    Historia 2: Tiempo vs margen (REAL - desde pipeline)
    """
    logger.info(f"=== GET /demo/real/story/2 - periodo: {periodo} ===")
    try:
        output = run_all(
            data_dir=settings.DATA_DIR,
            db_path=settings.DB_PATH,
            periodo=periodo,
            valor_minuto=settings.VALOR_MINUTO,
            margen_critico_pct=settings.MARGEN_CRITICO_PCT,
            margen_objetivo_pct=settings.MARGEN_OBJETIVO_PCT,
            esfuerzo_alto_min=settings.ESFUERZO_ALTO_MIN,
            top_drivers=settings.TOP_DRIVERS,
            llm_provider=None
        )
        return extract_story_2_tiempo_margen(output)
    except Exception as e:
        logger.error(f"Error generando H2 real: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@demo_router.get("/real/story/3")
def real_story_3(periodo: str = "2024-01") -> Dict[str, Any]:
    """
    Historia 3: Alertas (REAL - desde pipeline)
    """
    logger.info(f"=== GET /demo/real/story/3 - periodo: {periodo} ===")
    try:
        output = run_all(
            data_dir=settings.DATA_DIR,
            db_path=settings.DB_PATH,
            periodo=periodo,
            valor_minuto=settings.VALOR_MINUTO,
            margen_critico_pct=settings.MARGEN_CRITICO_PCT,
            margen_objetivo_pct=settings.MARGEN_OBJETIVO_PCT,
            esfuerzo_alto_min=settings.ESFUERZO_ALTO_MIN,
            top_drivers=settings.TOP_DRIVERS,
            llm_provider=None
        )
        return extract_story_3_alertas(output)
    except Exception as e:
        logger.error(f"Error generando H3 real: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@demo_router.get("/real/story/4")
def real_story_4(periodo: str = "2024-01") -> Dict[str, Any]:
    """
    Historia 4: Drivers de costos (REAL - desde pipeline)
    """
    logger.info(f"=== GET /demo/real/story/4 - periodo: {periodo} ===")
    try:
        output = run_all(
            data_dir=settings.DATA_DIR,
            db_path=settings.DB_PATH,
            periodo=periodo,
            valor_minuto=settings.VALOR_MINUTO,
            margen_critico_pct=settings.MARGEN_CRITICO_PCT,
            margen_objetivo_pct=settings.MARGEN_OBJETIVO_PCT,
            esfuerzo_alto_min=settings.ESFUERZO_ALTO_MIN,
            top_drivers=settings.TOP_DRIVERS,
            llm_provider=None
        )
        return extract_story_4_drivers(output)
    except Exception as e:
        logger.error(f"Error generando H4 real: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ===== UPLOAD CSV ENDPOINTS =====

@demo_router.post("/upload/productos")
async def upload_productos(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Sube un CSV de productos y genera H1 (ranking margen) SIMULADA
    Detecta tipo de negocio por nombre del archivo
    """
    logger.info(f"=== POST /demo/upload/productos - {file.filename} ===")
    try:
        from app.demo.simulated_stories import get_story_by_filename
        story = get_story_by_filename(file.filename, story_id=1)
        if not story:
            raise HTTPException(status_code=400, detail="Error generando simul ación")
        return story
    except Exception as e:
        logger.error(f"Error subiendo productos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@demo_router.post("/upload/tiempos")
async def upload_tiempos(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Sube un CSV con tiempos y márgenes, genera H2 SIMULADA
    Detecta tipo de negocio por nombre del archivo
    """
    logger.info(f"=== POST /demo/upload/tiempos - {file.filename} ===")
    try:
        from app.demo.simulated_stories import get_story_by_filename
        story = get_story_by_filename(file.filename, story_id=2)
        if not story:
            raise HTTPException(status_code=400, detail="Error generando simulación")
        return story
    except Exception as e:
        logger.error(f"Error subiendo tiempos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
