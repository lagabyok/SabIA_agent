import os
from typing import Dict, Any
from .base import LLMProvider
from .prompts import executive_report_prompt

class GeminiProvider(LLMProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")

    def generate_executive_report(self, payload: Dict[str, Any]) -> str:
        if not self.api_key:
            return (
                "### Resumen\n"
                "- Se detectaron oportunidades de mejora en margen y eficiencia.\n\n"
                "### Alertas clave\n"
                "- Priorizar productos con margen negativo y precio desactualizado.\n\n"
                "### Próximos pasos\n"
                "- Ajustar precios sugeridos y monitorear impacto.\n"
            )

        prompt = executive_report_prompt(payload)
        return "### Resumen\n- (Integración Gemini pendiente)\n\n```\n" + prompt[:800] + "\n```"
