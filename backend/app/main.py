from fastapi import FastAPI
import logging
from app.api.routes import router
from app.core.config import settings
from app.storage.db import init_db

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="SabIA Backend", version="0.1.0")
app.include_router(router)

@app.on_event("startup")
def _startup():
    init_db(settings.DB_PATH)
