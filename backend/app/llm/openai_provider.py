import os
from typing import Dict, Any
from .base import LLMProvider
from .prompts import executive_report_prompt

class OpenAIProvider(LLMProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")

    def generate_executive_report(self, payload: Dict[str, Any]) -> str:
        # Hackathon-safe: si no hay key, devolvemos template deterministic.
        if not self.api_key:
            return (
                "### Resumen\n"
                "- Se generaron KPIs y alertas explicables.\n"
                "- Revisar alertas de severidad ALTA primero.\n\n"
                "### Acciones recomendadas\n"
                "- Ajustar precios de productos con margen negativo/crítico.\n"
                "- Revisar drivers (insumos dominantes) y tiempos altos.\n"
            )

        # Si después quieren integrar API real, acá se implementa llamada a OpenAI.
        # Para la demo, evitamos dependencias extra y dejamos stub.
        prompt = executive_report_prompt(payload)
        return "### Resumen\n- (Integración OpenAI pendiente)\n\n```\n" + prompt[:800] + "\n```"
