from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    # Paths
    DATA_DIR: str = os.getenv("DATA_DIR", "app/data")
    DB_PATH: str = os.getenv("DB_PATH", "app/data/sabia.sqlite")

    # Business knobs
    MARGEN_OBJETIVO_PCT: float = float(os.getenv("MARGEN_OBJETIVO_PCT", "0.30"))
    MARGEN_CRITICO_PCT: float = float(os.getenv("MARGEN_CRITICO_PCT", "0.10"))

    # Esfuerzo (demo: valorización simple)
    VALOR_MINUTO: float = float(os.getenv("VALOR_MINUTO", "1.0"))

    # Clasificación de esfuerzo
    ESFUERZO_ALTO_MIN: int = int(os.getenv("ESFUERZO_ALTO_MIN", "90"))

    # Drivers
    TOP_DRIVERS: int = int(os.getenv("TOP_DRIVERS", "3"))

settings = Settings()
